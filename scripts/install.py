#!/usr/bin/env python3
"""Guided macOS/Linux standalone installation. No debloat or accessibility writes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from urllib.request import urlopen

PACKAGE = 'io.github.aashish26.firetvrevamp'
COMPONENT = PACKAGE + '/com.gathin.tvhome.MainActivity'
VERSION = '0.2.0'
APK = 'firetv-revamp-' + VERSION + '.apk'
BASE = 'https://github.com/aashish-26/firetv-revamp/releases/download/v' + VERSION + '/'
# Pinned to the verified, signed public preview. Changing releases requires review.
SHA256 = '18835b68c36650bdee34d5ad74e1cae0c3a983871256231a11801344aabea1c7'


def run(args, timeout=60):
    result = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    if result.returncode:
        raise RuntimeError('Command failed: ' + ' '.join(args) + '\n' + result.stdout + result.stderr)
    return result.stdout.strip()


def adb(serial, *args):
    return ['adb', '-s', serial, *args]


def devices(output):
    rows = []
    for line in output.splitlines():
        fields = line.split()
        if len(fields) >= 2 and fields[1] == 'device':
            rows.append(fields[0])
    return rows


def verify(data, sums):
    entries = [line.split() for line in sums.splitlines() if line.strip()]
    matching = [row[0].lower() for row in entries if len(row) == 2 and row[1].lstrip('*') == APK]
    if matching != [SHA256] or hashlib.sha256(data).hexdigest() != SHA256:
        raise RuntimeError('Checksum verification failed. Nothing will be installed.')


def download(url, limit):
    with urlopen(url, timeout=45) as response:
        if not response.geturl().startswith('https://'):
            raise RuntimeError('Refusing non-HTTPS download')
        data = response.read(limit + 1)
    if len(data) > limit:
        raise RuntimeError('Download exceeds expected size limit')
    return data


def confirm(message):
    return input(message + ' [y/N] ').strip().lower() == 'y'


def choose_device(serial):
    run(['adb', 'start-server'])
    available = devices(run(['adb', 'devices']))
    if not available and not serial:
        address = input('No authorized device found. Enter TV IP:port (or Enter to exit): ').strip()
        if not address:
            raise RuntimeError('No device selected')
        if not re.fullmatch(r'[A-Za-z0-9.-]+:[0-9]{1,5}', address):
            raise RuntimeError('Use a host/IP and port, for example TV_IP:5555')
        print(run(['adb', 'connect', address]))
        print('Accept the authorization prompt on your TV, if shown.')
        input('Press Enter when authorized: ')
        available = devices(run(['adb', 'devices']))
    if serial:
        if serial not in available:
            raise RuntimeError('Requested serial is not connected and authorized. Run adb connect first.')
        return serial
    if not available:
        raise RuntimeError('No authorized device. Check TV ADB settings and the authorization prompt.')
    for i, item in enumerate(available, 1):
        model = run(adb(item, 'shell', 'getprop', 'ro.product.model'))
        print(f'{i}. {item}  ({model})')
    choice = input('Select device number: ').strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(available):
        raise RuntimeError('Invalid device selection')
    return available[int(choice) - 1]


def rollback(folder):
    """Only reverse this install; never modify another package or secure settings."""
    state = json.loads((folder / 'installation.json').read_text())
    serial = state['serial']
    if state.get('package') != PACKAGE:
        raise RuntimeError('This is not a Fire TV Revamp installation record')
    if state.get('status') != 'installed':
        raise RuntimeError('Install was not confirmed successful; inspect the record and use manual recovery instead of automatic uninstall.')
    if run(adb(serial, 'get-state')) != 'device':
        raise RuntimeError('Original device is unavailable')
    print('First disable Fire TV Revamp in TV Settings > Accessibility, if enabled.')
    if state['previous_apks']:
        print('Restore the backed-up community APK(s), preserving data where Android permits.')
        if not confirm('Restore previous APK(s) on ' + serial + '?'):
            return
        paths = []
        for entry in state['previous_apks']:
            path = folder / entry['name']
            if path.parent != folder or hashlib.sha256(path.read_bytes()).hexdigest() != entry['sha256']:
                raise RuntimeError('Backup integrity check failed')
            paths.append(str(path))
        command = 'install' if len(paths) == 1 else 'install-multiple'
        print(run(adb(serial, command, '-r', '-d', *paths), timeout=180))
        print('If Android rejects a downgrade, stop and use the recovery guide; do not clear data.')
    else:
        print('This was a new installation. Uninstall removes this app and its preferences only.')
        if not confirm('Uninstall Fire TV Revamp from ' + serial + '?'):
            return
        print(run(adb(serial, 'uninstall', PACKAGE)))
    print('Press Home to return to Amazon Home. No system packages were changed.')


def install(serial):
    model = run(adb(serial, 'shell', 'getprop', 'ro.product.model'))
    sdk = run(adb(serial, 'shell', 'getprop', 'ro.build.version.sdk'))
    if not sdk.isdigit() or int(sdk) < 26:
        raise RuntimeError('Android API 26 or newer is required')
    print(f'Target: {serial} / {model} / Android API {sdk}')
    print('Standalone install only. Amazon Home and accessibility settings will not change.')
    print('Downloading pinned v' + VERSION + ' from the project GitHub release...')
    sums = download(BASE + 'SHA256SUMS', 16384).decode('utf-8')
    data = download(BASE + APK, 16 * 1024 * 1024)
    verify(data, sums)
    print('SHA-256 verified against published checksum AND installer pin.')
    if not confirm('Install on this device?'):
        print('Cancelled. No TV changes made.')
        return
    root = Path(__file__).resolve().parents[1] / 'backups'
    root.mkdir(exist_ok=True)
    folder = Path(tempfile.mkdtemp(prefix='install-', dir=root))
    folder.chmod(0o700)
    state = {'serial': serial, 'model': model, 'sdk': sdk, 'package': PACKAGE,
             'version': VERSION, 'timestamp': datetime.now(timezone.utc).isoformat(),
             'previous_apks': [], 'status': 'preparing', 'commands': []}
    record = folder / 'installation.json'

    def save():
        record.write_text(json.dumps(state, indent=2))
        record.chmod(0o600)

    save()
    # Check existence separately so an error cannot be mistaken for a fresh install.
    installed = run(adb(serial, 'shell', 'pm', 'list', 'packages', PACKAGE)).splitlines()
    if 'package:' + PACKAGE in installed:
        output = run(adb(serial, 'shell', 'pm', 'path', PACKAGE))
        remote = [line[len('package:'):] for line in output.splitlines() if line.startswith('package:')]
        if not remote:
            raise RuntimeError('Existing package found but APK paths are unavailable; refusing upgrade')
        for i, path in enumerate(remote):
            if not path.startswith('/') or any(c.isspace() for c in path):
                raise RuntimeError('Unexpected APK path; refusing upgrade')
            backup = folder / f'previous-{i}.apk'
            run(adb(serial, 'pull', path, str(backup)))
            if not backup.is_file() or not backup.stat().st_size:
                raise RuntimeError('Existing APK backup failed; refusing upgrade')
            state['previous_apks'].append({'name': backup.name, 'sha256': hashlib.sha256(backup.read_bytes()).hexdigest()})
    apk = folder / APK
    apk.write_bytes(data)
    command = adb(serial, 'install', '-r', str(apk))
    state['status'] = 'install-pending'
    state['commands'].append({'argv': command})
    save()
    try:
        result = run(command, timeout=180)
        if 'Success' not in result:
            raise RuntimeError('ADB did not confirm successful installation: ' + result)
        state['status'] = 'installed'
        state['commands'][-1]['result'] = result
        save()
    except Exception as error:
        state['status'] = 'install-error'
        state['commands'][-1]['error'] = str(error)
        save()
        raise
    print('Installed. Local recovery record: ' + str(folder))
    print('Rollback: python3 scripts/install.py --rollback ' + repr(str(folder)))
    print('Test Home, Settings, remote, HDMI, audio and streaming. Home redirect is not enabled automatically.')
    if confirm('Open the standalone launcher now?'):
        print(run(adb(serial, 'shell', 'am', 'start', '-n', COMPONENT)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--serial', help='Explicit connected, authorized ADB device serial')
    parser.add_argument('--check', action='store_true', help='Check device readiness without downloading or installing')
    parser.add_argument('--rollback', type=Path, help='Local install backup directory to restore')
    args = parser.parse_args()
    if sys.platform not in ('darwin', 'linux'):
        raise RuntimeError('This guided installer supports macOS and Linux; use manual ADB instructions on other systems.')
    if not shutil.which('adb'):
        raise RuntimeError('ADB is missing. macOS: brew install --cask android-platform-tools; Linux: install your distro android-tools-adb/adb package, or Google Platform Tools. Nothing is installed automatically.')
    if args.rollback and args.check:
        raise RuntimeError('--check and --rollback cannot be combined')
    if args.rollback:
        rollback(args.rollback.resolve())
    elif args.check:
        serial = choose_device(args.serial)
        print('Model: ' + run(adb(serial, 'shell', 'getprop', 'ro.product.model')))
        print('Android API: ' + run(adb(serial, 'shell', 'getprop', 'ro.build.version.sdk')))
        print('Community app: ' + (run(adb(serial, 'shell', 'pm', 'list', 'packages', PACKAGE)) or 'not installed'))
        print('Readiness inspection complete; no download or TV settings/package changes.')
    else:
        install(choose_device(args.serial))


if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, subprocess.TimeoutExpired, KeyboardInterrupt) as error:
        print('Stopped: ' + str(error), file=sys.stderr)
        sys.exit(1)
