"""Admission checks before any release credentials or Apple upload are used."""
import base64
import copy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import plistlib
import stat
import tempfile
import unittest
from unittest.mock import call, patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('mac_store', ROOT / 'scripts/package-mac-store.py')
mac_store = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mac_store)


class MacStorePackagingTests(unittest.TestCase):
    def setUp(self):
        self.profile = {
            'TeamIdentifier': [mac_store.TEAM],
            'ExpirationDate': datetime.now(timezone.utc) + timedelta(days=2),
            'Entitlements': {'com.apple.application-identifier': mac_store.TEAM + '.' + mac_store.BUNDLE,
                             'com.apple.developer.team-identifier': mac_store.TEAM},
            'DeveloperCertificates': [b'distribution certificate'],
        }

    def test_signing_revision_reuses_only_a_direct_parent_with_no_application_changes(self):
        source, signing = 'a' * 40, 'b' * 40
        with patch.object(mac_store, 'run') as command:
            mac_store.validate_release_revision(source, source)
            command.assert_not_called()
        with patch.object(mac_store, 'run', side_effect=[f'{signing} {source}',
                                                        '\n'.join(sorted(mac_store.SIGNING_TOOLING_PATHS))]):
            mac_store.validate_release_revision(source, signing)
        for changed in ('src/main.cpp', 'CMakeLists.txt', 'packaging/mpp-reader/engine-lock.json',
                        'resources/i18n/manifest.json', '.github/workflows/mac-store-preparation.yml'):
            with self.subTest(changed=changed), patch.object(mac_store, 'run', side_effect=[
                    f'{signing} {source}', 'scripts/package-mac-store.py\n' + changed]):
                with self.assertRaisesRegex(ValueError, 'inputs changed'):
                    mac_store.validate_release_revision(source, signing)

    def test_signing_revision_rejects_other_history_and_invalid_commit_ids(self):
        source, signing = 'a' * 40, 'b' * 40
        for history in (f'{signing} ' + 'c' * 40, f'{signing} {source} ' + 'c' * 40):
            with self.subTest(history=history), patch.object(mac_store, 'run', return_value=history):
                with self.assertRaisesRegex(ValueError, 'direct signing-tooling-only parent'):
                    mac_store.validate_release_revision(source, signing)
        with self.assertRaisesRegex(ValueError, 'full source'):
            mac_store.validate_release_revision('HEAD', signing)

    def test_embedded_executables_inherit_only_the_parent_sandbox(self):
        expected = {'com.apple.security.app-sandbox': True, 'com.apple.security.inherit': True}
        with tempfile.TemporaryDirectory() as directory:
            entitlements = Path(directory) / 'helper.plist'
            entitlements.write_bytes(plistlib.dumps(expected))
            binary = Path(directory) / 'java'
            binary.write_bytes(b'unchanged executable contents')
            binary.chmod(0o644)
            for header in ('MH_MAGIC_64 ARM64 ALL EXECUTE',
                           'java (architecture arm64):\nMH_MAGIC_64 ARM64 ALL EXECUTE\n'
                           'java (architecture x86_64):\nMH_MAGIC_64 X86_64 ALL EXECUTE'):
                with self.subTest(header=header), patch.object(mac_store, 'run', side_effect=[
                        header, '', 'Executable=java\n' + plistlib.dumps(expected).decode()]) as command:
                    self.assertTrue(mac_store.sign_nested_macho(['codesign', '--sign', 'identity'],
                                                               binary, entitlements))
                    self.assertIn(call(['codesign', '--sign', 'identity', '--entitlements', entitlements,
                                        binary]), command.call_args_list)
                    self.assertEqual(binary.read_bytes(), b'unchanged executable contents')
                    if os.name != 'nt':
                        self.assertEqual(binary.stat().st_mode & 0o111, 0o111)

    def test_embedded_library_keeps_library_signing_without_helper_entitlements(self):
        with patch.object(mac_store, 'run', side_effect=['MH_MAGIC_64 ARM64 ALL DYLIB', '']) as command:
            self.assertFalse(mac_store.sign_nested_macho(['codesign', '--sign', 'identity'],
                                                        Path('libjvm.dylib'), Path('helper.plist')))
            self.assertEqual(command.call_args_list[-1], call(['codesign', '--sign', 'identity', Path('libjvm.dylib')]))

    def test_helper_signature_with_missing_or_extra_permissions_is_rejected(self):
        expected = {'com.apple.security.app-sandbox': True, 'com.apple.security.inherit': True}
        with tempfile.TemporaryDirectory() as directory:
            entitlements = Path(directory) / 'helper.plist'
            entitlements.write_bytes(plistlib.dumps(expected))
            binary = Path(directory) / 'java'
            binary.write_bytes(b'helper')
            for effective in ({'com.apple.security.app-sandbox': True},
                              {**expected, 'com.apple.security.network.client': True}):
                with self.subTest(effective=effective), patch.object(mac_store, 'run', side_effect=[
                        'MH_MAGIC_64 ARM64 ALL EXECUTE', '', plistlib.dumps(effective).decode()]):
                    with self.assertRaisesRegex(ValueError, 'inherit only'):
                        mac_store.sign_nested_macho(['codesign'], binary, entitlements)

    @unittest.skipIf(os.name == 'nt', 'POSIX permissions are verified on the Mac signing runner')
    def test_embedded_profile_is_public_but_private_signing_material_stays_private(self):
        with tempfile.TemporaryDirectory() as directory, patch.dict(os.environ, {
                'MAC_APP_STORE_PROVISION_PROFILE_BASE64': base64.b64encode(b'signed public profile').decode(),
                'MAC_APP_STORE_CERTIFICATES_P12_BASE64': base64.b64encode(b'private p12').decode(),
                'APP_STORE_CONNECT_API_PRIVATE_KEY': 'private API key'}):
            root = Path(directory)
            profile = root / 'embedded.provisionprofile'
            mac_store.install_embedded_profile(profile)
            p12, key = root / 'identities.p12', root / 'AuthKey.p8'
            mac_store.secret_file('MAC_APP_STORE_CERTIFICATES_P12_BASE64', p12)
            mac_store.secret_file('APP_STORE_CONNECT_API_PRIVATE_KEY', key, encoded=False)
            self.assertEqual(profile.read_bytes(), b'signed public profile')
            self.assertEqual(stat.S_IMODE(profile.stat().st_mode), 0o644)
            self.assertEqual(stat.S_IMODE(p12.stat().st_mode), 0o600)
            self.assertEqual(stat.S_IMODE(key.stat().st_mode), 0o600)

    @unittest.skipIf(os.name == 'nt', 'POSIX permissions are verified on the Mac signing runner')
    def test_payload_rejects_owner_only_files_directories_and_executables(self):
        with tempfile.TemporaryDirectory() as directory:
            app = Path(directory) / 'PPM.app'
            app.mkdir(mode=0o755)
            app.chmod(0o755)
            payload = app / 'Contents'
            payload.mkdir(mode=0o755)
            payload.chmod(0o755)
            profile, binary = payload / 'embedded.provisionprofile', payload / 'PPM'
            profile.write_bytes(b'profile')
            binary.write_bytes(b'executable')
            profile.chmod(0o644)
            binary.chmod(0o755)
            # Real Qt frameworks contain internal directory and file symlinks.
            (payload / 'Current').symlink_to('.', target_is_directory=True)
            (payload / 'PPM-link').symlink_to('PPM')
            mac_store.validate_payload_permissions(app)
            for path, mode, restore in ((profile, 0o600, 0o644), (payload, 0o700, 0o755),
                                        (app, 0o700, 0o755), (binary, 0o744, 0o755)):
                with self.subTest(path=path.name, mode=oct(mode)):
                    path.chmod(mode)
                    try:
                        with self.assertRaisesRegex(ValueError, 'non-owner users'):
                            mac_store.validate_payload_permissions(app)
                    finally:
                        path.chmod(restore)
            mac_store.validate_payload_permissions(app)

    def test_exact_distribution_profile(self):
        self.assertEqual(len(mac_store.validate_profile(self.profile)), 1)
        self.profile['ExpirationDate'] = self.profile['ExpirationDate'].replace(tzinfo=None)
        mac_store.validate_profile(self.profile)

    def test_preparation_uses_app_status_with_separate_sandbox_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            bundle = root / 'dist/mac-store-preparation'
            bundle.mkdir(parents=True)
            archive = bundle / 'PPM-unsigned-universal.app.zip'
            archive.write_bytes(b'archive')
            status = {'source_revision': 'app-revision', 'sandbox_container_verified': True}
            (bundle / 'status.json').write_text(json.dumps(status))
            sandbox = root / 'build-mac-store/sandbox-validation'
            sandbox.mkdir(parents=True)
            (sandbox / 'status.json').write_text(json.dumps({'source_revision': 'probe-revision'}))
            self.assertEqual(mac_store.preparation_inputs(root), (status, archive))

    def test_preparation_rejects_unpaired_status_and_duplicate_app_archives(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'status.json').write_text('{}')
            bundle = root / 'app'
            bundle.mkdir()
            (bundle / 'PPM-unsigned-universal.app.zip').write_bytes(b'archive')
            with self.assertRaisesRegex(ValueError, 'paired status'):
                mac_store.preparation_inputs(root)
            (bundle / 'status.json').write_text('{}')
            (root / 'PPM-unsigned-universal.app.zip').write_bytes(b'another archive')
            with self.assertRaisesRegex(ValueError, 'one verified preparation app archive'):
                mac_store.preparation_inputs(root)

    def test_wrong_team_app_wildcard_and_debug_profiles(self):
        for field, value in [('com.apple.application-identifier', mac_store.TEAM + '.*'),
                             ('com.apple.application-identifier', mac_store.TEAM + '.another.app'),
                             ('com.apple.developer.team-identifier', 'OTHER'),
                             ('get-task-allow', True), ('com.apple.security.get-task-allow', True)]:
            with self.subTest(field=field, value=value):
                bad = copy.deepcopy(self.profile)
                bad['Entitlements'][field] = value
                with self.assertRaises(ValueError):
                    mac_store.validate_profile(bad)
        for field, value in [('TeamIdentifier', ['OTHER']), ('ProvisionedDevices', ['a-device']),
                             ('ProvisionsAllDevices', True), ('DeveloperCertificates', [])]:
            bad = copy.deepcopy(self.profile)
            bad[field] = value
            with self.assertRaises(ValueError):
                mac_store.validate_profile(bad)

    def test_expired_and_ambiguous_profile(self):
        self.profile['ExpirationDate'] = datetime.now(timezone.utc) - timedelta(seconds=1)
        with self.assertRaises(ValueError):
            mac_store.validate_profile(self.profile)
        self.setUp()
        self.profile['Entitlements']['application-identifier'] = mac_store.TEAM + '.other'
        with self.assertRaises(ValueError):
            mac_store.validate_profile(self.profile)

    def test_identity_must_be_the_profile_distribution_certificate(self):
        line = '1) ' + 'A' * 40 + f' "Apple Distribution: Publisher ({mac_store.TEAM})"'
        with self.assertRaises(ValueError):
            mac_store.identity(line, ('Apple Distribution:',), {'B' * 40})
        self.assertIn(mac_store.TEAM, mac_store.identity(line, ('Apple Distribution:',), {'A' * 40}))
        with self.assertRaises(ValueError):
            mac_store.identity(line + '\n' + line, ('Apple Distribution:',), {'A' * 40})

    def test_signing_keychain_preserves_and_restores_search_list_on_failure(self):
        previous = '    "/Users/runner/Library/Keychains/login.keychain-db"\n    "/path with spaces/extra.keychain-db"\n'
        original = ['/Users/runner/Library/Keychains/login.keychain-db', '/path with spaces/extra.keychain-db']
        for fails in (False, True):
            with self.subTest(fails=fails), patch.object(mac_store, 'run', side_effect=[previous, '', '']) as run:
                try:
                    with mac_store.signing_keychain_search('/tmp/signing.keychain-db'):
                        if fails:
                            raise ValueError('Signing failed')
                except ValueError:
                    self.assertTrue(fails)
                self.assertEqual(run.call_args_list, [
                    call(['security', 'list-keychains', '-d', 'user']),
                    call(['security', 'list-keychains', '-d', 'user', '-s', '/tmp/signing.keychain-db', *original]),
                    call(['security', 'list-keychains', '-d', 'user', '-s', *original]),
                ])

    def test_upload_requires_exact_source_runtime_and_external_qa(self):
        good = {'source_revision': 'revision', 'qt_appstore_compliant': True, 'sandbox_container_verified': True,
                'mpp_reader_verified': True}
        mac_store.validate_preparation(good, 'revision', False, False)
        mac_store.validate_preparation(good, 'revision', True, True)
        mac_store.validate_preparation(good, 'revision', True, False, testflight=True)
        with self.assertRaisesRegex(ValueError, 'requires --upload'):
            mac_store.validate_preparation(good, 'revision', False, False, testflight=True)
        with self.assertRaises(ValueError):
            mac_store.validate_preparation(good, 'revision', True, False)
        for key, value in [('source_revision', 'other'), ('qt_appstore_compliant', False),
                           ('sandbox_container_verified', False), ('mpp_reader_verified', False)]:
            bad = {**good, key: value}
            with self.assertRaises(ValueError):
                mac_store.validate_preparation(bad, 'revision', True, True)
            with self.assertRaises(ValueError):
                mac_store.validate_preparation(bad, 'revision', True, False, testflight=True)

    def test_archive_rejects_traversal_and_external_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            for index, name in enumerate(('../outside', '/outside')):
                archive = root / f'bad-{index}.zip'
                with zipfile.ZipFile(archive, 'w') as z:
                    z.writestr(name, b'bad')
                with self.assertRaises(ValueError):
                    mac_store.validate_archive(archive, root)

            for index, target in enumerate(('../../outside', '/outside')):
                archive = root / f'link-{index}.zip'
                link = zipfile.ZipInfo('PPM.app/Contents/link')
                link.create_system = 3
                link.external_attr = (stat.S_IFLNK | 0o777) << 16
                with zipfile.ZipFile(archive, 'w') as z:
                    z.writestr(link, target)
                with self.assertRaises(ValueError):
                    mac_store.validate_archive(archive, root)

    def test_archive_accepts_internal_framework_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            archive = root / 'framework.zip'
            link = zipfile.ZipInfo('PPM.app/Contents/Frameworks/QtCore.framework/Versions/Current')
            link.create_system = 3
            link.external_attr = (stat.S_IFLNK | 0o777) << 16
            with zipfile.ZipFile(archive, 'w') as z:
                z.writestr('PPM.app/Contents/Frameworks/QtCore.framework/Versions/A/QtCore', b'library')
                z.writestr(link, 'A')
            mac_store.validate_archive(archive, root)


if __name__ == '__main__':
    unittest.main()
