"""Authenticated HTTP API, resumable change feed and durable interval worker."""

import asyncio
from contextlib import suppress
from datetime import datetime
import hashlib
import json
from pathlib import Path
import secrets
import time
from aiohttp import web, WSMsgType
from .store import ApiError, Store, canonical, digest, fail, identifier
from .engine import NativeEngine

MAX_NATIVE = 64 * 1024 * 1024
MAX_REQUEST = 1024 * 1024


def integer(value, low, high):
    if isinstance(value, bool) or not isinstance(value, int) or not low <= value <= high:
        fail(400, "invalid_integer", "Integer outside supported range")
    return value


def keys(data, allowed, required=()):
    if not isinstance(data, dict) or set(data) - set(allowed) or set(required) - set(data):
        fail(400, "invalid_fields", "Missing or unknown JSON fields")


async def read_limited(request, limit, timeout=10):
    if request.content_length is not None and request.content_length > limit:
        fail(413, "request_too_large", "Request exceeds size limit")

    async def read():
        chunks = bytearray()
        async for chunk in request.content.iter_chunked(16384):
            chunks.extend(chunk)
            if len(chunks) > limit:
                fail(413, "request_too_large", "Request exceeds size limit")
        return bytes(chunks)

    return await asyncio.wait_for(read(), timeout)


async def body(request, limit=MAX_REQUEST):
    if request.content_type != "application/json":
        fail(415, "json_required", "Use application/json")
    raw = await read_limited(request, limit)
    if len(raw) > limit:
        fail(413, "request_too_large", "Request exceeds size limit")

    def unique(pairs):
        result = {}
        for k, v in pairs:
            if k in result:
                fail(400, "duplicate_field", "Duplicate JSON field")
            result[k] = v
        return result

    try:
        parsed = json.loads(
            raw,
            object_pairs_hook=unique,
            parse_constant=lambda _: fail(400, "invalid_json", "Non-finite JSON number"),
        )
        canonical(parsed).encode("utf-8")
        return parsed
    except (ValueError, UnicodeError, RecursionError):
        fail(400, "invalid_json", "Invalid JSON")


def token_of(request):
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        fail(401, "authentication_required", "Bearer authentication required")
    return header[7:]


@web.middleware
async def errors(request, handler):
    try:
        # No cookie authentication/CORS. Browser requests must originate here.
        import ipaddress

        if not request.secure:
            try:
                loopback = ipaddress.ip_address(request.remote or "").is_loopback
            except ValueError:
                loopback = False
            if not loopback:
                fail(403, "tls_required", "Remote requests require TLS")
        origin = request.headers.get("Origin")
        if origin and origin != request.app["public_origin"]:
            fail(403, "origin_denied", "Cross-origin requests are not accepted")
        response = await handler(request)
    except ApiError as e:
        response = web.json_response(
            {"error": {"code": e.code, "message": str(e)}}, status=e.status
        )
    except web.HTTPException as e:
        response = web.json_response(
            {"error": {"code": "http_error", "message": e.reason}}, status=e.status
        )
    except asyncio.TimeoutError:
        response = web.json_response(
            {
                "error": {
                    "code": "engine_timeout",
                    "message": "Native validation timed out; no project change committed",
                }
            },
            status=503,
        )
    except (ConnectionError, asyncio.CancelledError):
        raise
    except Exception:
        import logging

        logging.getLogger("ppm.server").exception("Request failed")
        response = web.json_response(
            {"error": {"code": "internal_error", "message": "Server operation failed"}}, status=500
        )
    if response.status == 413:
        response.force_close()
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"
    )
    response.headers["Referrer-Policy"] = "no-referrer"
    if request.secure:
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response


class Service:
    def __init__(self, store, engine):
        self.store, self.engine = store, engine
        self.hash_slots = asyncio.Semaphore(2)
        self.sockets = set()

    def user(self, request, touch=True):
        return self.store.authenticate(token_of(request), touch=touch)

    async def login(self, request):
        data = await body(request, 4096)
        keys(data, {"username", "password"}, {"username", "password"})
        async with self.hash_slots:
            result = await asyncio.to_thread(
                self.store.login, data["username"], data["password"], request.remote or "unknown"
            )
        return web.json_response(result)

    async def logout(self, request):
        self.user(request)
        self.store.logout(token_of(request))
        return web.json_response({"state": "logged-out"})

    async def me(self, request):
        return web.json_response(self.user(request))

    async def users(self, request):
        user = self.user(request)
        with self.store.connect() as db:
            self.store.require_admin(db, user)
            if request.method == "GET":
                return web.json_response(
                    {
                        "users": [
                            dict(r)
                            for r in db.execute("SELECT id,admin,enabled FROM users ORDER BY id")
                        ]
                    }
                )
        data = await body(request, 4096)
        keys(data, {"id", "password"}, {"id", "password"})
        async with self.hash_slots:
            await asyncio.to_thread(
                self.store.add_user, data["id"], data["password"], False, actor=user["id"]
            )
        return web.json_response({"id": data["id"]}, status=201)

    async def disable_user(self, request):
        user = self.user(request)
        target = identifier(request.match_info["user"])
        data = await body(request, 4096)
        keys(data, {"enabled"}, {"enabled"})
        if not isinstance(data["enabled"], bool):
            fail(400, "invalid_boolean", "enabled must be boolean")
        with self.store.connect(True) as db:
            self.store.require_admin(db, user)
            row = db.execute("SELECT * FROM users WHERE id=?", (target,)).fetchone()
            if not row:
                fail(404, "not_found", "User not found")
            if row["admin"] and not data["enabled"]:
                fail(
                    409,
                    "administrator_protected",
                    "Administrator accounts are managed by the server operator",
                )
            db.execute("UPDATE users SET enabled=? WHERE id=?", (int(data["enabled"]), target))
            db.execute("DELETE FROM sessions WHERE user_id=?", (target,))
            self.store.event(
                db,
                None,
                user["id"],
                "account-state",
                None,
                {"user": target, "enabled": data["enabled"]},
            )
        return web.json_response({"state": "updated"})

    async def projects(self, request):
        user = self.user(request)
        if request.method == "GET":
            return web.json_response({"projects": self.store.projects(user)})
        with self.store.connect() as db:
            self.store.require_admin(db, user)
        if request.content_type != "application/octet-stream":
            fail(415, "native_required", "Upload a native .ppm as application/octet-stream")
        native = await read_limited(request, MAX_NATIVE, 30)
        summary, _, _ = await self.engine.evaluate(native)
        source = json.loads(native)
        if source["schemaVersion"] < 9:
            fail(
                422,
                "native_upgrade_required",
                "Save an upgraded native copy in the desktop app before registering this project",
            )
        project_id = identifier(summary["documentId"])
        user = self.user(request)
        with self.store.connect(True) as db:
            self.store.require_admin(db, user)
            if db.execute("SELECT 1 FROM projects WHERE id=?", (project_id,)).fetchone():
                fail(409, "project_exists", "Project already registered; use a versioned batch")
            # Name is validated by the native decoder.
            name = source["payload"]["name"]
            db.execute(
                "INSERT INTO projects VALUES(?,?,?,1,?,?)",
                (project_id, name, summary["revision"], native, canonical(summary)),
            )
            self.store.event(
                db, project_id, user["id"], "project-created", 1, {"revision": summary["revision"]}
            )
        return web.json_response(
            {"id": project_id, "version": 1, "revision": summary["revision"]}, status=201
        )

    async def project(self, request):
        row = self.store.project(self.user(request), request.match_info["project"])
        return web.json_response(
            {
                "id": row["id"],
                "name": row["name"],
                "version": row["version"],
                "summary": json.loads(row["summary"]),
            },
            headers={"ETag": '"' + str(row["version"]) + '"'},
        )

    async def native(self, request):
        row = self.store.project(self.user(request), request.match_info["project"])
        return web.Response(
            body=row["native"],
            content_type="application/octet-stream",
            headers={
                "ETag": '"' + str(row["version"]) + '"',
                "Content-Disposition": 'attachment; filename="project.ppm"',
            },
        )

    async def grant(self, request):
        user = self.user(request)
        data = await body(request, 4096)
        keys(data, {"userId", "role"}, {"userId", "role"})
        target = identifier(data["userId"])
        role = data["role"]
        if role not in ("viewer", "reviewer", "editor", None):
            fail(400, "invalid_role", "Unsupported role")
        project_id = request.match_info["project"]
        with self.store.connect(True) as db:
            self.store.require_admin(db, user)
            if (
                not db.execute("SELECT 1 FROM projects WHERE id=?", (project_id,)).fetchone()
                or not db.execute("SELECT 1 FROM users WHERE id=?", (target,)).fetchone()
            ):
                fail(404, "not_found", "Project or user not found")
            db.execute("DELETE FROM grants WHERE user_id=? AND project_id=?", (target, project_id))
            if role:
                db.execute("INSERT INTO grants VALUES(?,?,?)", (target, project_id, role))
            self.store.event(
                db,
                project_id,
                user["id"],
                "permission-changed",
                None,
                {"user": target, "role": role},
            )
        return web.json_response({"state": "updated"})

    def validate_batch(self, data, row):
        keys(data, {"expectedVersion", "request"}, {"expectedVersion", "request"})
        if integer(data["expectedVersion"], 1, 9007199254740991) != row["version"]:
            fail(409, "version_conflict", "Source changed; reload and review your edits")
        req = data["request"]
        keys(
            req,
            {"format", "documentId", "revision", "requestId", "operations"},
            {"format", "documentId", "revision", "requestId", "operations"},
        )
        identifier(req["requestId"])
        if (
            req["format"] != "PPM-AUTOMATION-1"
            or req["documentId"] != row["id"]
            or req["revision"] != row["revision"]
        ):
            fail(409, "revision_conflict", "Native source ID or revision changed")
        return req

    async def preview(self, request):
        user = self.user(request)
        project_id = request.match_info["project"]
        row = self.store.project(user, project_id)
        with self.store.connect() as db:
            self.store.authorize(db, user, project_id, "edit")
        data = await body(request)
        req = self.validate_batch(data, row)
        receipt, _, _ = await self.engine.evaluate(row["native"], req)
        user = self.user(request)
        ticket = secrets.token_urlsafe(32)
        with self.store.connect(True) as db:
            self.store.authorize(db, user, project_id, "edit")
            current = db.execute(
                "SELECT version FROM projects WHERE id=?", (project_id,)
            ).fetchone()
            if current["version"] != row["version"]:
                fail(409, "version_conflict", "Source changed during preview")
            db.execute("DELETE FROM previews WHERE expires<=?", (self.store.clock(),))
            if (
                db.execute(
                    "SELECT count(*) FROM previews WHERE user_id=?", (user["id"],)
                ).fetchone()[0]
                >= 100
            ):
                fail(429, "preview_limit", "Too many outstanding previews")
            db.execute(
                "INSERT INTO previews VALUES(?,?,?,?,?,?,?,?)",
                (
                    digest(ticket.encode()),
                    user["id"],
                    project_id,
                    row["version"],
                    canonical(req),
                    digest(canonical(req).encode()),
                    self.store.clock() + 600,
                    canonical(receipt),
                ),
            )
        return web.json_response(
            {"previewId": ticket, "version": row["version"], "expiresIn": 600, "receipt": receipt}
        )

    def commit_result(
        self, user, project_id, version, req, native, receipt, summary, *, job_id=None, run_key=None
    ):
        req_hash = digest(canonical(req).encode())
        with self.store.connect(True) as db:
            self.store.authorize(db, user, project_id, "edit")
            previous = db.execute(
                "SELECT * FROM receipts WHERE user_id=? AND project_id=? AND request_id=?",
                (user["id"], project_id, req["requestId"]),
            ).fetchone()
            if previous:
                if previous["hash"] != req_hash:
                    fail(409, "request_id_reused", "Request ID already used for different content")
                return json.loads(previous["receipt"])
            row = db.execute("SELECT * FROM projects WHERE id=?", (project_id,)).fetchone()
            if row["version"] != version:
                fail(409, "version_conflict", "Source changed; nothing applied")
            if job_id:
                job = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
                if (
                    not job
                    or not job["enabled"]
                    or job["run_key"] != run_key
                    or job["state"] != "running"
                ):
                    fail(409, "job_cancelled", "Scheduled run cancelled or superseded")
            if (
                summary["documentId"] != project_id
                or summary["revision"] != receipt["resultRevision"]
                or receipt["requestSha256"] != req_hash
            ):
                fail(422, "native_result_mismatch", "Native result provenance mismatch")
            if version >= 9007199254740991:
                fail(409, "version_limit", "Server version limit reached")
            next_version = version + 1
            receipt = {
                **receipt,
                "serverVersion": next_version,
                "actor": user["id"],
                "committedAt": self.store.clock(),
            }
            db.execute(
                "UPDATE projects SET revision=?,version=?,native=?,summary=? WHERE id=?",
                (summary["revision"], next_version, native, canonical(summary), project_id),
            )
            self.store.event(
                db,
                project_id,
                user["id"],
                "project-changed",
                next_version,
                {"requestId": req["requestId"], "revision": summary["revision"]},
            )
            db.execute(
                "INSERT INTO receipts VALUES(?,?,?,?,?)",
                (user["id"], project_id, req["requestId"], req_hash, canonical(receipt)),
            )
            if job_id:
                job = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
                # Coalesce missed intervals; never replay an unbounded backlog.
                next_at = job["next_at"] + job["interval_seconds"]
                now = self.store.clock()
                if next_at <= now:
                    next_at = now + job["interval_seconds"]
                db.execute(
                    "UPDATE jobs SET expected_version=?,next_at=?,state='ready',lease_until=NULL,run_key=NULL,fail_count=0 WHERE id=?",
                    (next_version, next_at, job_id),
                )
                db.execute(
                    "UPDATE runs SET state='succeeded',receipt=?,finished=? WHERE id=?",
                    (canonical(receipt), now, run_key),
                )
            return receipt

    async def apply(self, request):
        user = self.user(request)
        project_id = request.match_info["project"]
        data = await body(request, 4096)
        keys(data, {"previewId"}, {"previewId"})
        ticket = identifier(data["previewId"])
        with self.store.connect() as db:
            self.store.authorize(db, user, project_id, "edit")
            p = db.execute(
                "SELECT * FROM previews WHERE id=? AND user_id=? AND project_id=?",
                (digest(ticket.encode()), user["id"], project_id),
            ).fetchone()
            if not p:
                fail(404, "preview_not_found", "Preview not found")
            req = json.loads(p["request"])
            previous = db.execute(
                "SELECT * FROM receipts WHERE user_id=? AND project_id=? AND request_id=?",
                (user["id"], project_id, req["requestId"]),
            ).fetchone()
            if previous:
                if previous["hash"] != p["hash"]:
                    fail(409, "request_id_reused", "Request ID content mismatch")
                return web.json_response(json.loads(previous["receipt"]))
            if p["expires"] <= self.store.clock():
                fail(410, "preview_expired", "Preview expired")
        row = self.store.project(user, project_id)
        if row["version"] != p["version"]:
            fail(409, "version_conflict", "Source changed after preview")
        receipt, native, summary = await self.engine.evaluate(row["native"], req, apply=True)
        user = self.user(request)
        receipt = self.commit_result(user, project_id, p["version"], req, native, receipt, summary)
        return web.json_response(receipt)

    async def events(self, request):
        user = self.user(request)
        try:
            after = integer(int(request.query.get("after", "0")), 0, 9007199254740991)
            wait = integer(int(request.query.get("wait", "0")), 0, 25)
        except ValueError:
            fail(400, "invalid_cursor", "Invalid cursor or wait")
        end = time.monotonic() + wait
        while True:
            user = self.user(request, touch=False)
            changes = self.store.changes(user, after)
            if changes["cursor"] != after or time.monotonic() >= end:
                return web.json_response(changes)
            await asyncio.sleep(0.25)

    async def receipt(self, request):
        user = self.user(request)
        project_id = request.match_info["project"]
        request_id = request.match_info["request_id"]
        with self.store.connect() as db:
            self.store.authorize(db, user, project_id)
            row = db.execute(
                "SELECT receipt FROM receipts WHERE user_id=? AND project_id=? AND request_id=?",
                (user["id"], project_id, request_id),
            ).fetchone()
            if not row:
                fail(404, "not_found", "Execution receipt not found")
            return web.json_response(json.loads(row["receipt"]))

    async def websocket(self, request):
        ws = web.WebSocketResponse(heartbeat=20, max_msg_size=4096, compress=False)
        await ws.prepare(request)
        self.sockets.add(ws)
        try:
            first = await asyncio.wait_for(ws.receive_json(), 5)
            keys(first, {"token", "after"}, {"token", "after"})
            token = first["token"]
            user = self.store.authenticate(token)
            after = integer(first["after"], 0, 9007199254740991)
            await ws.send_json({"type": "connected", "user": user["id"]})
            while not ws.closed:
                user = self.store.authenticate(token, touch=False)
                changes = self.store.changes(user, after)
                if changes["cursor"] != after:
                    await ws.send_json({"type": "changes", **changes})
                    after = changes["cursor"]
                try:
                    message = await asyncio.wait_for(ws.receive(), 0.25)
                    if message.type in (WSMsgType.CLOSE, WSMsgType.CLOSED, WSMsgType.ERROR):
                        break
                    if message.type == WSMsgType.TEXT:
                        fail(
                            400,
                            "read_only_stream",
                            "Change stream accepts only the initial authentication message",
                        )
                except asyncio.TimeoutError:
                    pass
        except (ApiError, ValueError, TypeError, asyncio.TimeoutError):
            await ws.close(code=1008, message=b"Authentication expired or invalid stream request")
        finally:
            self.sockets.discard(ws)
        return ws

    async def shutdown(self, app):
        for socket in list(self.sockets):
            with suppress(asyncio.TimeoutError, ConnectionError):
                await asyncio.wait_for(socket.close(code=1001, message=b"Server shutdown"), 5)

    async def jobs(self, request):
        user = self.user(request)
        if request.method == "GET":
            with self.store.connect() as db:
                rows = db.execute(
                    "SELECT * FROM jobs WHERE owner=? ORDER BY next_at,id", (user["id"],)
                ).fetchall()
                return web.json_response(
                    {
                        "jobs": [
                            {
                                k: r[k]
                                for k in (
                                    "id",
                                    "project_id",
                                    "interval_seconds",
                                    "next_at",
                                    "expected_version",
                                    "enabled",
                                    "state",
                                    "fail_count",
                                )
                            }
                            for r in rows
                        ]
                    }
                )
        data = await body(request)
        keys(
            data,
            {"projectId", "intervalSeconds", "startAt", "expectedVersion", "request"},
            {"projectId", "intervalSeconds", "startAt", "expectedVersion", "request"},
        )
        project_id = identifier(data["projectId"])
        row = self.store.project(user, project_id)
        with self.store.connect() as db:
            self.store.authorize(db, user, project_id, "edit")
        interval = integer(data["intervalSeconds"], 60, 2592000)
        start = integer(data["startAt"], 0, 4102444800)
        if start < self.store.clock() - 60:
            fail(400, "invalid_start", "Start time is in the past")
        req = self.validate_batch(
            {"expectedVersion": data["expectedVersion"], "request": data["request"]}, row
        )
        await self.engine.evaluate(row["native"], req)
        user = self.user(request)
        job_id = secrets.token_hex(16)
        with self.store.connect(True) as db:
            self.store.authorize(db, user, project_id, "edit")
            if (
                db.execute("SELECT version FROM projects WHERE id=?", (project_id,)).fetchone()[0]
                != row["version"]
            ):
                fail(409, "version_conflict", "Source changed during schedule validation")
            if (
                db.execute(
                    "SELECT count(*) FROM jobs WHERE owner=? AND enabled=1", (user["id"],)
                ).fetchone()[0]
                >= 100
            ):
                fail(429, "job_limit", "Schedule limit reached")
            db.execute(
                "INSERT INTO jobs(id,owner,project_id,interval_seconds,next_at,expected_version,request) VALUES(?,?,?,?,?,?,?)",
                (job_id, user["id"], project_id, interval, start, row["version"], canonical(req)),
            )
            self.store.event(
                db,
                project_id,
                user["id"],
                "job-created",
                row["version"],
                {"jobId": job_id, "intervalSeconds": interval, "startAt": start},
            )
        return web.json_response({"id": job_id, "state": "ready"}, status=201)

    async def cancel_job(self, request):
        user = self.user(request)
        job_id = request.match_info["job"]
        with self.store.connect(True) as db:
            row = db.execute(
                "SELECT * FROM jobs WHERE id=? AND owner=?", (job_id, user["id"])
            ).fetchone()
            if not row:
                fail(404, "not_found", "Schedule not found")
            db.execute(
                "UPDATE jobs SET enabled=0,state='cancelled',lease_until=NULL WHERE id=?", (job_id,)
            )
            if row["run_key"]:
                db.execute(
                    "UPDATE runs SET state='cancelled',finished=? WHERE id=? AND state='running'",
                    (self.store.clock(), row["run_key"]),
                )
            self.store.event(
                db, row["project_id"], user["id"], "job-cancelled", None, {"jobId": job_id}
            )
        return web.json_response({"state": "cancelled"})

    async def runs(self, request):
        user = self.user(request)
        with self.store.connect() as db:
            rows = db.execute(
                "SELECT r.* FROM runs r JOIN jobs j ON j.id=r.job_id WHERE j.owner=? ORDER BY started DESC LIMIT 200",
                (user["id"],),
            ).fetchall()
            return web.json_response(
                {
                    "runs": [
                        {**dict(r), "receipt": json.loads(r["receipt"]) if r["receipt"] else None}
                        for r in rows
                    ]
                }
            )

    async def tick(self):
        now = self.store.clock()
        with self.store.connect(True) as db:
            job = db.execute(
                "SELECT * FROM jobs WHERE enabled=1 AND next_at<=? AND (state='ready' OR (state='running' AND lease_until<=?)) ORDER BY next_at,id LIMIT 1",
                (now, now),
            ).fetchone()
            if not job:
                return False
            job = dict(job)
            run_key = job["id"] + ":" + str(job["next_at"])
            # Lease renewal is only for abandoned workers; engine timeout is shorter than the lease.
            db.execute(
                "UPDATE jobs SET state='running',lease_until=?,run_key=? WHERE id=?",
                (now + 120, run_key, job["id"]),
            )
            db.execute(
                "INSERT INTO runs VALUES(?,?,?,'running',NULL,?,NULL) ON CONFLICT(id) DO UPDATE SET state='running',started=excluded.started",
                (run_key, job["id"], job["next_at"], now),
            )
        user = {"id": job["owner"]}
        try:
            row = self.store.project(user, job["project_id"])
            if row["version"] != job["expected_version"]:
                fail(409, "version_conflict", "External edit detected; schedule paused")
            req = json.loads(job["request"])
            req["revision"] = row["revision"]
            req["requestId"] = "job:" + run_key
            with self.store.connect() as db:
                self.store.authorize(db, user, job["project_id"], "edit")
            receipt, native, summary = await self.engine.evaluate(row["native"], req, apply=True)
            self.commit_result(
                user,
                job["project_id"],
                row["version"],
                req,
                native,
                receipt,
                summary,
                job_id=job["id"],
                run_key=run_key,
            )
        except asyncio.CancelledError:
            # The uncommitted DB snapshot is unchanged; lease recovery retries this run ID.
            raise
        except Exception as e:
            code = e.code if isinstance(e, ApiError) else "worker_error"
            with self.store.connect(True) as db:
                current = db.execute("SELECT * FROM jobs WHERE id=?", (job["id"],)).fetchone()
                if (
                    current
                    and current["enabled"]
                    and current["run_key"] == run_key
                    and current["state"] == "running"
                ):
                    db.execute(
                        "UPDATE jobs SET enabled=0,state='failed',lease_until=NULL,fail_count=fail_count+1 WHERE id=?",
                        (job["id"],),
                    )
                    db.execute(
                        "UPDATE runs SET state='failed',receipt=?,finished=? WHERE id=?",
                        (canonical({"error": code}), self.store.clock(), run_key),
                    )
                    self.store.event(
                        db,
                        job["project_id"],
                        job["owner"],
                        "job-failed",
                        None,
                        {"jobId": job["id"], "code": code},
                    )
        return True


async def worker(app):
    async def loop():
        while True:
            try:
                await app["service"].tick()
            except Exception:
                import logging

                logging.getLogger("ppm.server").exception("Worker iteration failed; retrying")
            await asyncio.sleep(0.5)

    task = asyncio.create_task(loop())
    yield
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task


def create_app(store, engine, *, public_origin="http://127.0.0.1:8765", scheduler=True):
    app = web.Application(client_max_size=MAX_NATIVE, middlewares=[errors])
    service = Service(store, engine)
    app.on_shutdown.append(service.shutdown)
    app["service"] = service
    app["public_origin"] = public_origin.rstrip("/")
    app.add_routes(
        [
            web.post("/api/v1/login", service.login),
            web.post("/api/v1/logout", service.logout),
            web.get("/api/v1/me", service.me),
            web.get("/api/v1/users", service.users),
            web.post("/api/v1/users", service.users),
            web.put("/api/v1/users/{user}", service.disable_user),
            web.get("/api/v1/projects", service.projects),
            web.post("/api/v1/projects", service.projects),
            web.get("/api/v1/projects/{project}", service.project),
            web.get("/api/v1/projects/{project}/native", service.native),
            web.put("/api/v1/projects/{project}/grant", service.grant),
            web.post("/api/v1/projects/{project}/preview", service.preview),
            web.post("/api/v1/projects/{project}/apply", service.apply),
            web.get("/api/v1/events", service.events),
            web.get("/api/v1/projects/{project}/receipts/{request_id}", service.receipt),
            web.get("/api/v1/stream", service.websocket),
            web.get("/api/v1/jobs", service.jobs),
            web.post("/api/v1/jobs", service.jobs),
            web.delete("/api/v1/jobs/{job}", service.cancel_job),
            web.get("/api/v1/runs", service.runs),
        ]
    )
    static = Path(__file__).parent / "static"

    async def asset(request):
        name = request.match_info.get("asset", "index.html")
        if name not in ("index.html", "app.js", "style.css", "favicon.svg"):
            raise web.HTTPNotFound()
        return web.FileResponse(static / name)

    app.router.add_get("/", asset)
    app.router.add_get("/assets/{asset}", asset)
    if scheduler:
        app.cleanup_ctx.append(worker)
    return app
