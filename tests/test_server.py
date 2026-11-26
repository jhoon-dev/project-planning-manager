"""HTTP/WebSocket/native engine and durable worker integration."""

import asyncio
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import ssl
import sys
import tempfile
import unittest
from aiohttp import WSMsgType, ClientSession, ClientConnectorCertificateError
from aiohttp.test_utils import TestServer, TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
from ppm_server.store import Store
from ppm_server.engine import NativeEngine
from ppm_server.service import create_app, Service

ENGINE = Path(
    os.environ.get("PPM_TEST_ENGINE", ROOT / "build-governance/PPM-Automation.exe")
).resolve()
NATIVE = (ROOT / "tests/fixtures/server-project.ppm").read_bytes()
PASSWORD = "test-only-Strong-Password-123"


class ServerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.now = 1800000000.0
        self.store = Store(
            Path(self.temp.name) / "server.sqlite", clock=lambda: self.now, scrypt_n=16384
        )
        for user, admin in [
            ("admin", True),
            ("editor", False),
            ("viewer", False),
            ("other", False),
        ]:
            self.store.add_user(user, PASSWORD, admin)
        self.engine = NativeEngine(ENGINE)
        self.app = create_app(self.store, self.engine, scheduler=False)
        self.client = TestClient(TestServer(self.app))
        await self.client.start_server()
        self.tokens = {}
        for user in ("admin", "editor", "viewer", "other"):
            r = await self.client.post(
                "/api/v1/login", json={"username": user, "password": PASSWORD}
            )
            self.assertEqual(r.status, 200, await r.text())
            self.tokens[user] = (await r.json())["token"]
        r = await self.call(
            "POST", "/projects", data=NATIVE, headers={"Content-Type": "application/octet-stream"}
        )
        self.assertEqual(r.status, 201, await r.text())
        for user, role in [("editor", "editor"), ("viewer", "viewer")]:
            r = await self.call(
                "PUT", "/projects/server-fixture/grant", json={"userId": user, "role": role}
            )
            self.assertEqual(r.status, 200)

    async def asyncTearDown(self):
        await self.client.close()
        self.temp.cleanup()

    async def call(self, method, path, user="admin", **kwargs):
        headers = {"Authorization": "Bearer " + self.tokens[user], **kwargs.pop("headers", {})}
        return await self.client.request(method, "/api/v1" + path, headers=headers, **kwargs)

    async def snapshot(self, user="admin"):
        r = await self.call("GET", "/projects/server-fixture", user)
        self.assertEqual(r.status, 200, await r.text())
        return await r.json()

    def batch(self, snapshot, name="Changed", request_id="test-run"):
        return {
            "expectedVersion": snapshot["version"],
            "request": {
                "format": "PPM-AUTOMATION-1",
                "documentId": "server-fixture",
                "revision": snapshot["summary"]["revision"],
                "requestId": request_id,
                "operations": [{"taskId": "A", "name": name, "durationMinutes": 960}],
            },
        }

    async def preview(self, data, user="editor"):
        r = await self.call("POST", "/projects/server-fixture/preview", user, json=data)
        self.assertEqual(r.status, 200, await r.text())
        return await r.json()

    async def apply(self, preview, user="editor"):
        return await self.call(
            "POST", "/projects/server-fixture/apply", user, json={"previewId": preview["previewId"]}
        )

    async def test_password_hash_session_logout_and_reset(self):
        with self.store.connect() as db:
            row = db.execute("SELECT * FROM users WHERE id='editor'").fetchone()
            self.assertNotIn(PASSWORD.encode(), row["verifier"])
            session = db.execute("SELECT hash FROM sessions WHERE user_id='editor'").fetchone()[0]
            self.assertNotEqual(session, self.tokens["editor"])
        r = await self.call("POST", "/logout", "editor")
        self.assertEqual(r.status, 200)
        self.assertEqual((await self.call("GET", "/me", "editor")).status, 401)
        self.store.reset_password("viewer", "new-Strong-password-456")
        self.assertEqual((await self.call("GET", "/me", "viewer")).status, 401)
        r = await self.client.post(
            "/api/v1/login", json={"username": "viewer", "password": PASSWORD}
        )
        self.assertEqual(r.status, 401)

    async def test_throttle_and_expiry(self):
        for _ in range(5):
            r = await self.client.post(
                "/api/v1/login", json={"username": "missing", "password": "wrong"}
            )
            self.assertEqual(r.status, 401)
        r = await self.client.post(
            "/api/v1/login", json={"username": "missing", "password": PASSWORD}
        )
        self.assertEqual(r.status, 429)
        self.now += 1801
        self.assertEqual((await self.call("GET", "/me", "editor")).status, 401)
        r = await self.client.post(
            "/api/v1/login", json={"username": "editor", "password": PASSWORD}
        )
        self.assertEqual(r.status, 200)

    async def test_permissions_and_no_enumeration(self):
        self.assertEqual((await self.client.get("/api/v1/projects")).status, 401)
        r = await self.call("GET", "/projects", "other")
        self.assertEqual((await r.json())["projects"], [])
        self.assertEqual(
            (await self.call("GET", "/projects/server-fixture/native", "other")).status, 403
        )
        data = self.batch(await self.snapshot())
        self.assertEqual(
            (
                await self.call("POST", "/projects/server-fixture/preview", "viewer", json=data)
            ).status,
            403,
        )

    async def test_successful_logins_do_not_consume_peer_failure_budget(self):
        for _ in range(31):
            result = await self.client.post(
                "/api/v1/login", json={"username": "editor", "password": PASSWORD}
            )
            self.assertEqual(result.status, 200, await result.text())
            token = (await result.json())["token"]
            logout = await self.client.post(
                "/api/v1/logout", headers={"Authorization": "Bearer " + token}
            )
            self.assertEqual(logout.status, 200)
        self.assertEqual(
            (
                await self.call(
                    "PUT",
                    "/projects/server-fixture/grant",
                    "editor",
                    json={"userId": "other", "role": "editor"},
                )
            ).status,
            403,
        )
        self.assertEqual(
            (
                await self.call(
                    "POST", "/users", "editor", json={"id": "injected", "password": PASSWORD}
                )
            ).status,
            403,
        )

    async def test_native_atomic_batch_and_receipt(self):
        before = await self.snapshot()
        preview = await self.preview(self.batch(before))
        self.assertEqual((await self.snapshot())["version"], before["version"])
        self.assertEqual(preview["receipt"]["changes"][0]["beforeName"], "Design")
        r = await self.apply(preview)
        self.assertEqual(r.status, 200, await r.text())
        receipt = await r.json()
        self.assertEqual(receipt["requestSha256"], preview["receipt"]["requestSha256"])
        after = await self.snapshot()
        self.assertEqual((after["version"], after["summary"]["revision"]), (2, 2))
        self.assertEqual(after["summary"]["tasks"][0]["name"], "Changed")
        self.assertEqual(receipt["actor"], "editor")
        replay = await self.call("GET", "/projects/server-fixture/receipts/test-run", "editor")
        self.assertEqual(replay.status, 200)
        self.assertEqual((await replay.json())["serverVersion"], 2)
        native = await self.call("GET", "/projects/server-fixture/native")
        decoded, _, _ = await self.engine.evaluate(await native.read())
        self.assertEqual(decoded, after["summary"])
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM receipts").fetchone()[0], 1)
            self.assertEqual(
                db.execute("SELECT count(*) FROM events WHERE kind='project-changed'").fetchone()[
                    0
                ],
                1,
            )

    async def test_last_invalid_change_rolls_back(self):
        before = await self.snapshot()
        data = self.batch(before)
        data["request"]["operations"].append({"taskId": "missing", "name": "No"})
        r = await self.call("POST", "/projects/server-fixture/preview", "editor", json=data)
        self.assertEqual(r.status, 422)
        self.assertEqual(await self.snapshot(), before)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM receipts").fetchone()[0], 0)

    async def test_native_registration_rejects_overwrite_tamper_and_legacy(self):
        original = await self.snapshot()
        duplicate = await self.call(
            "POST", "/projects", data=NATIVE, headers={"Content-Type": "application/octet-stream"}
        )
        self.assertEqual(duplicate.status, 409)
        tampered = json.loads(NATIVE)
        tampered["sha256"] = "incorrect"
        result = await self.call(
            "POST",
            "/projects",
            data=json.dumps(tampered).encode(),
            headers={"Content-Type": "application/octet-stream"},
        )
        self.assertEqual(result.status, 422)
        legacy = json.loads(NATIVE)
        legacy["schemaVersion"] = 8
        result = await self.call(
            "POST",
            "/projects",
            data=json.dumps(legacy).encode(),
            headers={"Content-Type": "application/octet-stream"},
        )
        self.assertEqual(result.status, 422)
        self.assertEqual((await result.json())["error"]["code"], "native_upgrade_required")
        self.assertEqual(await self.snapshot(), original)

    async def test_two_clients_conflict_preserves_winner(self):
        before = await self.snapshot()
        first = await self.preview(self.batch(before, "Client one", "one"))
        second = await self.preview(self.batch(before, "Client two", "two"))
        replies = await asyncio.gather(self.apply(first), self.apply(second))
        self.assertEqual(sorted(r.status for r in replies), [200, 409])
        after = await self.snapshot()
        self.assertEqual(after["version"], 2)
        self.assertIn(after["summary"]["tasks"][0]["name"], ("Client one", "Client two"))
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM receipts").fetchone()[0], 1)

    async def test_idempotent_apply_and_request_reuse(self):
        p = await self.preview(self.batch(await self.snapshot()))
        first, second = await asyncio.gather(self.apply(p), self.apply(p))
        self.assertEqual((first.status, second.status), (200, 200))
        self.assertEqual(await first.json(), await second.json())
        self.assertEqual((await self.snapshot())["version"], 2)
        conflicting = await self.preview(
            self.batch(await self.snapshot(), "Other content", "test-run")
        )
        self.assertEqual((await self.apply(conflicting)).status, 409)

    async def test_role_revocation_and_preview_expiry(self):
        p = await self.preview(self.batch(await self.snapshot()))
        await self.call(
            "PUT", "/projects/server-fixture/grant", json={"userId": "editor", "role": "viewer"}
        )
        self.assertEqual((await self.apply(p)).status, 403)
        await self.call(
            "PUT", "/projects/server-fixture/grant", json={"userId": "editor", "role": "editor"}
        )
        self.now += 601
        self.assertEqual((await self.apply(p)).status, 410)
        self.assertEqual((await self.snapshot())["version"], 1)

    async def test_account_disable_and_stream_revoke(self):
        ws = await self.client.ws_connect("/api/v1/stream")
        await ws.send_json({"token": self.tokens["editor"], "after": 0})
        self.assertEqual((await ws.receive_json())["type"], "connected")
        r = await self.call("PUT", "/users/editor", json={"enabled": False})
        self.assertEqual(r.status, 200)
        self.assertEqual((await self.call("GET", "/me", "editor")).status, 401)
        while True:
            m = await ws.receive(timeout=3)
            if m.type in (WSMsgType.CLOSE, WSMsgType.CLOSED):
                break
        self.assertEqual(ws.close_code, 1008)
        await ws.close()

    async def test_changefeed_reconnect_and_acl(self):
        unauthorized = await self.call("GET", "/events?after=0", "other")
        self.assertEqual((await unauthorized.json())["events"], [])
        ws = await self.client.ws_connect("/api/v1/stream")
        await ws.send_json({"token": self.tokens["viewer"], "after": 0})
        self.assertEqual((await ws.receive_json())["type"], "connected")
        initial = await ws.receive_json()
        cursor = initial["cursor"]
        p = await self.preview(self.batch(await self.snapshot()))
        self.assertEqual((await self.apply(p)).status, 200)
        event = await ws.receive_json(timeout=5)
        self.assertTrue(any(e["kind"] == "project-changed" for e in event["events"]))
        await ws.close()
        replay = await self.call("GET", "/events?after=" + str(cursor), "viewer")
        self.assertTrue(
            any(e["kind"] == "project-changed" for e in (await replay.json())["events"])
        )
        with self.store.connect() as db:
            self.assertNotIn(
                self.tokens["viewer"],
                json.dumps([dict(r) for r in db.execute("SELECT * FROM events")]),
            )

    async def test_long_poll_wakes_on_commit(self):
        # Prepare before starting the bounded poll: this checks commit wake-up,
        # independent of native validation/login time on a loaded regression host.
        p = await self.preview(self.batch(await self.snapshot()))
        response = await self.call("GET", "/events?after=0", "viewer")
        cursor = (await response.json())["cursor"]
        pending = asyncio.create_task(self.call("GET", f"/events?after={cursor}&wait=3", "viewer"))
        await asyncio.sleep(0.05)
        await self.apply(p)
        data = await (await pending).json()
        self.assertGreater(data["cursor"], cursor)
        self.assertTrue(data["events"])

    async def test_http_origin_json_bounds_and_headers(self):
        r = await self.call("GET", "/me", headers={"Origin": "https://attacker.invalid"})
        self.assertEqual(r.status, 403)
        r = await self.call("GET", "/me")
        self.assertEqual(r.headers["Cache-Control"], "no-store")
        self.assertIn("frame-ancestors 'none'", r.headers["Content-Security-Policy"])
        r = await self.client.post(
            "/api/v1/login",
            data='{"username":"admin","username":"editor","password":"x"}',
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(r.status, 400)
        r = await self.client.post(
            "/api/v1/login", data="x" * 5000, headers={"Content-Type": "application/json"}
        )
        self.assertEqual(r.status, 413)
        self.assertEqual((await self.call("GET", "/events?after=-1")).status, 400)
        self.assertEqual((await self.client.get("/assets/../../ppm_server/store.py")).status, 404)

    async def post_job(self, request_id):
        snap = await self.snapshot()
        b = self.batch(snap, "Scheduled", request_id)
        return await self.call(
            "POST",
            "/jobs",
            "editor",
            json={
                "projectId": "server-fixture",
                "intervalSeconds": 60,
                "startAt": int(self.now),
                **b,
            },
        )

    async def make_job(self, request_id="schedule"):
        r = await self.post_job(request_id)
        self.assertEqual(r.status, 201, await r.text())
        return (await r.json())["id"]

    async def test_job_quota_counts_only_active_schedules(self):
        with self.store.connect(True) as db:
            db.executemany(
                "INSERT INTO jobs(id,owner,project_id,interval_seconds,next_at,expected_version,request,enabled,state) "
                "VALUES(?,'editor','server-fixture',60,?,1,'{}',?,?)",
                [
                    (f"{state}-{index}", self.now, int(state == "ready"), state)
                    for state, count in (("cancelled", 50), ("failed", 50), ("ready", 99))
                    for index in range(count)
                ],
            )
        job = await self.make_job("fills-last-slot")
        limited = await self.post_job("exceeds-active-limit")
        self.assertEqual(limited.status, 429, await limited.text())
        self.assertEqual((await limited.json())["error"]["code"], "job_limit")

        cancelled = await self.call("DELETE", f"/jobs/{job}", "editor")
        self.assertEqual(cancelled.status, 200, await cancelled.text())
        await self.make_job("uses-freed-slot")
        listing = await self.call("GET", "/jobs", "editor")
        self.assertEqual(listing.status, 200, await listing.text())
        jobs = (await listing.json())["jobs"]
        self.assertEqual(sum(row["enabled"] for row in jobs), 100)
        self.assertEqual(sum(not row["enabled"] for row in jobs), 101)

    async def test_durable_job_repeats_coalesces_and_cancels(self):
        job = await self.make_job()
        service = self.app["service"]
        self.assertTrue(await service.tick())
        self.assertEqual((await self.snapshot())["version"], 2)
        self.assertFalse(await service.tick())
        restarted = Service(
            Store(self.store.path, clock=lambda: self.now, scrypt_n=16384), self.engine
        )
        self.now += 600
        self.assertTrue(await restarted.tick())
        self.assertEqual((await self.snapshot())["version"], 3)
        self.assertFalse(await restarted.tick())
        self.assertEqual((await self.call("DELETE", "/jobs/" + job, "editor")).status, 200)
        self.now += 600
        self.assertFalse(await restarted.tick())
        runs = await self.call("GET", "/runs", "editor")
        self.assertEqual(
            [r["state"] for r in (await runs.json())["runs"]], ["succeeded", "succeeded"]
        )

    async def test_job_external_conflict_and_revoked_owner(self):
        await self.make_job()
        p = await self.preview(self.batch(await self.snapshot(), "External", "external"))
        await self.apply(p)
        await self.app["service"].tick()
        r = await self.call("GET", "/jobs", "editor")
        self.assertEqual((await r.json())["jobs"][0]["state"], "failed")
        self.assertEqual((await self.snapshot())["version"], 2)
        await self.make_job(request_id="second")
        await self.call(
            "PUT", "/projects/server-fixture/grant", json={"userId": "editor", "role": None}
        )
        await self.app["service"].tick()
        self.assertEqual((await self.snapshot())["version"], 2)

    async def test_worker_crash_recovery_and_single_claim(self):
        job_id = await self.make_job()
        now = self.now
        key = job_id + ":" + str(float(now))
        with self.store.connect(True) as db:
            db.execute(
                "UPDATE jobs SET state='running',lease_until=?,run_key=? WHERE id=?",
                (now + 120, key, job_id),
            )
            db.execute(
                "INSERT INTO runs VALUES(?,?,?,'running',NULL,?,NULL)", (key, job_id, now, now)
            )
        service = self.app["service"]
        self.assertFalse(await service.tick())
        self.now += 121
        other = Service(Store(self.store.path, clock=lambda: self.now, scrypt_n=16384), self.engine)
        claimed = await asyncio.gather(service.tick(), other.tick())
        self.assertEqual(sum(claimed), 1)
        self.assertEqual((await self.snapshot())["version"], 2)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT count(*) FROM runs").fetchone()[0], 1)
            self.assertEqual(db.execute("SELECT state FROM runs").fetchone()[0], "succeeded")

    async def test_job_cancel_while_native_engine_runs(self):
        await self.make_job()
        original = self.engine.evaluate
        started, release = asyncio.Event(), asyncio.Event()

        async def held(*args, **kwargs):
            if kwargs.get("apply"):
                started.set()
                await release.wait()
            return await original(*args, **kwargs)

        self.engine.evaluate = held
        pending = asyncio.create_task(self.app["service"].tick())
        await asyncio.wait_for(started.wait(), 5)
        r = await self.call("GET", "/jobs", "editor")
        job = (await r.json())["jobs"][0]
        await self.call("DELETE", "/jobs/" + job["id"], "editor")
        release.set()
        await pending
        self.assertEqual((await self.snapshot())["version"], 1)
        with self.store.connect() as db:
            self.assertEqual(db.execute("SELECT state FROM runs").fetchone()[0], "cancelled")
            self.assertEqual(db.execute("SELECT count(*) FROM receipts").fetchone()[0], 0)

    async def test_rollback_after_sql_failure_and_backup(self):
        p = await self.preview(self.batch(await self.snapshot()))
        with self.store.connect(True) as db:
            db.execute(
                "CREATE TRIGGER fail_receipt BEFORE INSERT ON receipts BEGIN SELECT RAISE(ABORT,'injected'); END"
            )
        self.assertEqual((await self.apply(p)).status, 500)
        self.assertEqual((await self.snapshot())["version"], 1)
        with self.store.connect() as db:
            self.assertEqual(
                db.execute("SELECT count(*) FROM events WHERE kind='project-changed'").fetchone()[
                    0
                ],
                0,
            )
            with closing(sqlite3.connect(Path(self.temp.name) / "backup.sqlite")) as backup:
                db.backup(backup)
                self.assertEqual(backup.execute("SELECT version FROM projects").fetchone()[0], 1)

    async def test_role_revoked_during_native_validation(self):
        preview = await self.preview(self.batch(await self.snapshot()))
        original = self.engine.evaluate
        started, release = asyncio.Event(), asyncio.Event()

        async def held(*args, **kwargs):
            if kwargs.get("apply"):
                started.set()
                await release.wait()
            return await original(*args, **kwargs)

        self.engine.evaluate = held
        pending = asyncio.create_task(self.apply(preview))
        await asyncio.wait_for(started.wait(), 5)
        await self.call(
            "PUT", "/projects/server-fixture/grant", json={"userId": "editor", "role": None}
        )
        release.set()
        self.assertEqual((await pending).status, 403)
        self.assertEqual((await self.snapshot())["version"], 1)

    async def test_live_worker_executes_without_manual_tick(self):
        await self.make_job()
        running = TestServer(create_app(self.store, self.engine, scheduler=True))
        await running.start_server()
        try:
            async with asyncio.timeout(10):
                while (await self.snapshot())["version"] == 1:
                    await asyncio.sleep(0.1)
            self.assertEqual((await self.snapshot())["summary"]["tasks"][0]["name"], "Scheduled")
        finally:
            await running.close()

    async def test_tls_and_certificate_verification(self):
        fixtures = ROOT / "tests/fixtures/server-tls"
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.load_cert_chain(fixtures / "certificate.pem", fixtures / "test-only-key.pem")
        secure = TestServer(create_app(self.store, self.engine, scheduler=False), scheme="https")
        await secure.start_server(ssl=context)
        try:
            async with ClientSession() as client:
                with self.assertRaises(ClientConnectorCertificateError):
                    await client.get(secure.make_url("/api/v1/me"))
                trust = ssl.create_default_context(cafile=str(fixtures / "certificate.pem"))
                async with client.get(
                    secure.make_url("/api/v1/me"),
                    ssl=trust,
                    headers={"Authorization": "Bearer " + self.tokens["editor"]},
                ) as response:
                    self.assertEqual(response.status, 200)
                    self.assertIn("max-age=", response.headers["Strict-Transport-Security"])
        finally:
            await secure.close()


class ProductionKdfTests(unittest.TestCase):
    def test_default_password_parameters(self):
        with tempfile.TemporaryDirectory() as temp:
            store = Store(Path(temp) / "production.sqlite")
            store.add_user("operator", PASSWORD, True)
            with store.connect() as db:
                row = db.execute("SELECT * FROM users").fetchone()
                self.assertEqual(
                    (row["scrypt_n"], len(row["salt"]), len(row["verifier"])), (131072, 16, 32)
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
