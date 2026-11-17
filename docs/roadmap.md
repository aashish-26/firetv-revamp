# Small next enhancements

These are proposed, not released features:

- Physically test the separately packaged public APK and record exact model/firmware outcomes.
- Add a local image picker with persistable read permission, bounded image decoding and a static fallback; avoid broad storage access.
- Consider opt-in muted foreground-only video wallpaper after measuring decoder, memory and navigation costs on low-end TVs.
- Add grid-size / reduced-motion controls and favorites-only filtering if device testing confirms useful behavior.
- Expand Home-policy tests and add automated build checks without exposing release signing keys.

Priority: validate public installation, Settings recovery and Home/standby behavior before adding visual complexity. No promise of true permanent replacement or measured performance gains.
