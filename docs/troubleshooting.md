# Troubleshooting

Start with `bash scripts/install.sh --check` (macOS/Linux). It checks dependencies, allows device selection and reads model, Android API and installed community package status. It does not download or install an APK or alter TV settings. ADB may start its local server or connect to the device during selection.

| Symptom | What to do |
|---|---|
| `adb` / Python missing | Follow [dependency instructions](installation.md#requirements); rerun after the tools are on PATH |
| Device is unauthorized | Accept the ADB prompt on your TV; rerun `adb devices` |
| Device is offline or absent | Check the TV is awake and reachable; check its current address and ADB setting; connect manually with `adb connect YOUR_TV_IP:5555` |
| Multiple devices listed | Select the correct displayed model/serial or pass `--serial`; never guess |
| Hash mismatch or download error | Stop. Download a fresh copy of this repository and retry once; do not bypass verification |
| Insufficient storage | Inspect TV storage using normal Settings. Do not clear streaming app data as a shortcut |
| Signature mismatch | Stop. Community and personal apps have different identities. Do not uninstall an existing app to force an update without understanding data loss |
| Home opens Amazon | Installation alone does not enable redirect. Check the optional service in normal Accessibility Settings, if available; standalone use is supported |
| Accessibility menu is unavailable | Keep standalone use. Do not write protected settings or disable stock Home |
| Settings or input intent unavailable | Open original Fire TV Settings. Support varies by firmware |
| No Style button | Confirm you installed community v0.2.0, not the older preview or personal build |
| Rollback says install was not confirmed | Inspect the local record and use [manual recovery](recovery.md). Automatic removal is blocked for incomplete installs |
| Downgrade rejected | Keep the current app or use normal recovery; the installer does not clear data to bypass Android restrictions |

When reporting an issue include model, OS/build, app version and exact steps. Redact diagnostics and screenshots; do not upload local backup folders or identifiers. Start with [the issue templates](https://github.com/aashish-26/firetv-revamp/issues/new/choose).
