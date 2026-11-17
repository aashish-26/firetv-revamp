package com.gathin.tvhome;
import android.content.Context;
import android.graphics.Typeface;
/** Local-only visual choices. Never changes system settings or Home behavior. */
final class Appearance {
    static final String[] THEMES = {"Nebula", "Ocean", "Ember", "Midnight"};
    static final String[] FONTS = {"Outfit — geometric", "Open Sans — readable", "System — familiar"};
    static int selected(Context c, String key, int count) {
        return VisualOptions.bounded(c.getSharedPreferences("ui", Context.MODE_PRIVATE).getInt(key, 0), count);
    }
    static Typeface font(Context c) {
        switch (selected(c, "font", FONTS.length)) {
            case 1: return c.getResources().getFont(R.font.open_sans);
            case 2: return Typeface.create("sans-serif", Typeface.NORMAL);
            default: return c.getResources().getFont(R.font.outfit);
        }
    }
    static int background(Context c) {
        switch (selected(c, "theme", THEMES.length)) {
            case 1: return R.drawable.ocean;
            case 2: return R.drawable.ember;
            default: return R.drawable.nebula;
        }
    }
    static int accent(Context c) {
        switch (selected(c, "theme", THEMES.length)) {
            case 1: return 0xFF8DE8DC;
            case 2: return 0xFFFFBD9B;
            case 3: return 0xFFD3DCEC;
            default: return 0xFFCAB5FF;
        }
    }
}
