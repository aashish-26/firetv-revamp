# Recovery

1. In launcher settings choose Amazon Home (recovery). This pauses this app's redirect preference.
2. In Fire TV Settings > Accessibility disable the Fire TV Revamp Home screen service. Exact menus vary.
3. To stop the community launcher from ADB:

```sh
adb -s YOUR_TV_IP:5555 shell am force-stop io.github.aashish26.firetvrevamp
adb -s YOUR_TV_IP:5555 shell am start -a android.intent.action.MAIN -c android.intent.category.HOME
```

Disable its accessibility service through Settings before reopening the app. Force-stop alone is temporary, not a persistent service toggle. If necessary remove only this optional community app:

```sh
adb -s YOUR_TV_IP:5555 uninstall io.github.aashish26.firetvrevamp
```

Uninstall removes community launcher preferences. It does not remove Amazon Home. No system packages were modified by installation or the audit tool. Keep previous APKs for upgrades; Android may reject downgrades. Do not clear data or uninstall merely to force a downgrade without accepting preference loss. If ADB is unavailable, use Fire TV Settings > Applications > Manage Installed Applications > Fire TV Revamp > Force stop / Uninstall and disable its Accessibility service.

## Installer backups

If you used the guided installer, see [installation.md](installation.md#roll-back) for recorded APK restoration or first-install removal. Neither method is a firmware restore; downgrade restrictions and preference compatibility still apply.
