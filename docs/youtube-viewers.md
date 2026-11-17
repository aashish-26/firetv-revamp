# Coming from the YouTube video?

Fire TV Revamp changes the home-screen experience using an Android launcher. It does **not** replace Fire OS, flash firmware, or turn a Fire TV into Apple TV hardware/software. Streaming apps and Amazon services still run on Fire OS.

## What the video and download have in common

- Glass-style app cards and a customizable dock.
- Hidden applications without uninstalling them.
- Clock controls, Settings and recovery shortcuts.
- Optional accessibility-based return to the launcher when Amazon Home opens.

## Important differences

The video shows the creator's personal Clean TV build. The public 0.1.0 preview is a separate app with its own package/signing identity and original static Nebula artwork. It does not include the personal Goku image or Asta video, a media import picker, or live-video playback. Installing the public APK will not recreate that exact wallpaper appearance. Existing personal-build preferences do not migrate.

The previous personal setup was used on Redmi AFTMV00 / dahlia, Fire OS 7.7.1.7. The separately packaged community preview has build, lint and unit validation; it has not yet received full physical-device validation. Other firmware/models are unverified.

## Start safely

1. Download the APK and SHA256SUMS from this repository's Releases page. Avoid APKs reuploaded elsewhere.
2. Enable developer options / ADB using your device's supported setup and authorize your own computer.
3. Substitute your TV's address for `YOUR_TV_IP:5555` in the README commands. Java/Android SDK are only needed to build from source, not to install the published APK. ADB is needed for these installation instructions.
4. Install and open the standalone launcher first. Check remote navigation, app launching, Settings, Wi-Fi, HDMI, audio and playback in your own streaming apps.
5. Only then consider the optional accessibility service if normal Settings exposes it. If it is unavailable, keep the standalone launcher. Never disable Amazon Home to force it.
6. Keep [recovery instructions](recovery.md) accessible on your phone/computer.

No reboot is required by these installation instructions. No debloat or privacy changes run automatically. Home redirection is not an unbreakable system default and may need recovery after updates or service interruptions.

## Verify your download

From the directory containing both release files:

```sh
# macOS
shasum -a 256 -c SHA256SUMS
# Linux
sha256sum -c SHA256SUMS
```

On Windows PowerShell use `Get-FileHash .\firetv-revamp-0.3.0.apk -Algorithm SHA256` and compare with SHA256SUMS. A matching hash checks the downloaded file against the published checksum; it is not a compatibility guarantee.

## Report a problem

Use the repository issue template. Include model, Fire OS/build, app version, exact reproduction and whether Amazon Home/Settings still work. Do not share account details, full diagnostics, private IP addresses, serial numbers or signing keys. State whether you tested the public APK or the personal video build.

## Suggested video-description clarification

> I customized my Fire TV home screen using a launcher; Fire OS is still installed. The public Fire TV Revamp preview includes an original static theme. My personal anime wallpapers and live-video setup are not included. Home redirect support varies by firmware; keep Amazon Home enabled and read the recovery guide before trying it.
