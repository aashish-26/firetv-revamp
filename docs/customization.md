# Make Revamp yours

Community preview **0.2.0** introduces original project styling controls. These changes are offline and stored only in the launcher. They do not change Android's system font, Amazon Home, system settings or other apps.

## Top controls

| Button | Action |
|---|---|
| Apps | Moves focus to the first application below the favorites dock; if there is no separate grid, returns to the first tile |
| Style | Opens theme, typography, clock and visual-reset controls |
| Inputs | Opens available input choices, subject to firmware support |
| Wi-Fi | Opens the supported network settings flow |
| Settings | Opens launcher / supported Amazon Settings choices, including recovery |

## Choose a theme

Select **Style → Theme & accent**:

- **Nebula:** deep blue and violet with a lavender greeting accent.
- **Ocean:** dark teal with a mint greeting accent.
- **Ember:** plum and warm copper with a peach greeting accent.
- **Midnight:** black wallpaper with a neutral greeting accent. Existing focus glow/cards remain visible.

These are static gradients: no video decoder, downloaded wallpaper or background network request. Focus glow still follows the selected app's artwork. Theme previews in the README illustrate palettes rather than physical-device screenshots.

## Choose typography

Select **Style → Font family**: geometric Outfit, readable Open Sans, or the Android system sans-serif. The chosen family applies to the main screen, app labels and choice panels. Fonts are already bundled or provided by Android; nothing is downloaded. The included fonts retain their SIL OFL licenses.

## Clock and reset

**Style → Clock visibility** toggles the time and AM/PM. The date stays visible. **Reset visual preferences** returns to Nebula, Outfit and a visible clock; it preserves favorites, app hiding, app data and Home redirect preference.

## Favorites and apps

Hold OK on an app to open the existing pin/unpin, move and hide controls. Hidden apps are hidden in this launcher only. Use launcher preferences → Show hidden apps to restore visibility. Settings and recovery remain available.

Use physical DPAD/remote testing on your TV. The new community layout and font choices have build/lint/unit validation, not full device certification. No performance gain is claimed.
