import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('installer', Path(__file__).resolve().parents[1] / 'scripts/install.py')
i = importlib.util.module_from_spec(spec)
spec.loader.exec_module(i)

class InstallerTests(unittest.TestCase):
    def test_only_authorized_devices(self):
        self.assertEqual(i.devices('List of devices attached\ntv device\nother unauthorized\nsleep offline\n'), ['tv'])

    def test_checksum_failure(self):
        with self.assertRaises(RuntimeError): i.verify(b'tampered', i.SHA256 + '  ' + i.APK)

    def test_checksum_requires_correct_filename_and_pin(self):
        data = b'fixture'
        with patch.object(i, 'SHA256', hashlib.sha256(data).hexdigest()):
            i.verify(data, i.SHA256 + '  ' + i.APK)
            with self.assertRaises(RuntimeError): i.verify(data, i.SHA256 + '  other.apk')
            with self.assertRaises(RuntimeError): i.verify(data, '0' * 64 + '  ' + i.APK)

    def test_cancel_never_installs(self):
        commands = []
        def fake(cmd, **kwargs):
            commands.append(cmd)
            return '28' if 'ro.build.version.sdk' in cmd else 'test-model'
        with patch.object(i, 'run', side_effect=fake), patch.object(i, 'download', return_value=b'x'), patch.object(i, 'verify'), patch.object(i, 'confirm', return_value=False):
            i.install('fake:5555')
        self.assertFalse(any('install' in cmd for cmd in commands))

    def test_missing_existing_apk_aborts_before_install(self):
        commands = []
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'record'; folder.mkdir()
            def fake(cmd, **kwargs):
                commands.append(cmd)
                if 'ro.build.version.sdk' in cmd: return '28'
                if 'list' in cmd: return 'package:' + i.PACKAGE
                if 'path' in cmd: return ''
                return 'test-model'
            with patch.object(i, 'run', side_effect=fake), patch.object(i, 'download', return_value=b'x'), patch.object(i, 'verify'), patch.object(i, 'confirm', return_value=True), patch.object(i.tempfile, 'mkdtemp', return_value=str(folder)):
                with self.assertRaises(RuntimeError): i.install('fake:5555')
        self.assertFalse(any('install' in cmd for cmd in commands))

    def test_explicit_unavailable_device_refused(self):
        with patch.object(i, 'run', return_value='List of devices attached\nother device'):
            with self.assertRaises(RuntimeError): i.choose_device('wanted:5555')

class RecoveryTests(unittest.TestCase):
    def test_unconfirmed_install_cannot_trigger_automatic_removal(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / 'installation.json').write_text(json.dumps({'serial':'fake:5555', 'package':i.PACKAGE, 'status':'preparing', 'previous_apks':[]}))
            with patch.object(i, 'run') as run:
                with self.assertRaises(RuntimeError): i.rollback(folder)
                run.assert_not_called()

    def test_readiness_never_downloads_or_installs(self):
        commands = []
        def fake(cmd, **kwargs):
            commands.append(cmd)
            return '28' if 'ro.build.version.sdk' in cmd else 'test'
        with patch.object(i.sys, 'argv', ['install.py', '--check']), patch.object(i.shutil, 'which', return_value='/fake/adb'), patch.object(i, 'choose_device', return_value='fake:5555'), patch.object(i, 'run', side_effect=fake), patch.object(i, 'download') as download:
            i.main()
            download.assert_not_called()
        self.assertFalse(any('install' in cmd or 'uninstall' in cmd for cmd in commands))

if __name__ == '__main__': unittest.main()
