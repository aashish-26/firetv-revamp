# Guided installation and rollback (macOS / Linux)

## Requirements

- Python 3 and ADB in PATH. No Python packages, curl, Java or Android SDK required to install the release.
- macOS: install Python from python.org if missing. If you already use Homebrew, ADB can be installed with `brew install --cask android-platform-tools`.
- Linux: install Python 3 and your distribution's `adb` / `android-tools-adb` package, or use Google's official Platform Tools. The script does not invoke sudo, install packages or accept SDK licenses.
- TV: ADB debugging enabled and computer authorized. Exact menus vary. If the device is unauthorized/offline, authorize it on the TV and rerun. It must appear as `device` in `adb devices`.

## Run

Download/extract the repository ZIP, or clone the repository, then run from its root:

```sh
bash scripts/install.sh
```

Select a device number even if only one is listed. If none is authorized, the script offers to connect to an IP/hostname and port. You can also connect manually with `adb connect YOUR_TV_IP:5555` then rerun. To explicitly target an authorized device, use `bash scripts/install.sh --serial YOUR_TV_IP:5555`.

The installer targets release v0.3.0, not an unverified latest download. It verifies the downloaded APK against SHA256SUMS and the pinned hash in the installer. GitHub HTTPS is required. Checksum mismatch, incompatible Android version, failed prior-APK backup or unavailable selected device stops installation. Select only your own TV.

Confirm the displayed model/serial before installation. `adb install -r` preserves existing app data on a compatible update. Android enforces signing compatibility; the script does not bypass signature errors or automatically uninstall to fix them. The personal `com.gathin.tvhome` app is a different app and is left untouched.

After installation, the launcher can be opened manually or using the script's final prompt. Physically test remote, Home, Settings, Wi-Fi, HDMI, audio and streaming. Optional accessibility redirection remains a separate manual Settings step. No system packages are disabled; there is no implicit debloat step.

## Local backup

Each approved install creates a private `backups/install-*/` folder containing:

- `installation.json`: selected device, app version, prior APK hashes and install command/result.
- The verified release APK.
- Any existing community APK and split APKs, pulled before replacing them.

Keep this folder locally. It contains device identifiers; it is gitignored. It is not an app-data or firmware backup. Existing launcher preferences are preserved by normal compatible updates, not exported by this tool.

## Roll back

First use TV Settings > Accessibility to disable the community Home redirect if enabled. The script never overwrites the complete enabled-accessibility-services setting.

Use the exact folder printed after installation:

```sh
python3 scripts/install.py --rollback '/path/to/firetv-revamp/backups/install-EXAMPLE'
```

The script checks the original device is available, verifies prior APK hashes and asks for confirmation. For an upgrade it attempts to reinstall the backed-up APK(s) using `-r -d`; Android may reject release downgrades. If rejected, stop and consult [recovery](recovery.md). It will not clear data or uninstall to force a downgrade. Backward app-data compatibility is not guaranteed across future versions.

For a first installation, rollback offers to uninstall **only** `io.github.aashish26.firetvrevamp`; that removes this app's preferences. Amazon Home and the personal Clean TV app are unaffected. You may instead keep the community app installed and leave its accessibility service disabled.

If install fails or is interrupted, inspect the installation record. No retry, uninstall, reboot or data clearing happens automatically. If ADB is unavailable use the TV Settings recovery steps in [recovery.md](recovery.md).

## System debloating

Intentionally separate. `tools/audit.py` is read-only and opt-in. This installer does not run it or any package disabling. Do not copy another TV model's disable list. Review dependencies and keep individual, reversible change records before any separately approved cleanup.

## Inspect before installing

Run `bash scripts/install.sh --check` to select an authorized device and read its model, Android API and community package state. No release download or APK install occurs. It may start the local ADB server or offer a device connection prompt.
