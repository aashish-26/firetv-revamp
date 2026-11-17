package com.gathin.tvhome;

/** Pure state machine: one Home transition, at most two bounded dispatches. */
final class HomePolicy {
    static final long DEBOUNCE_MS = 350, FALLBACK_MS = 5500;
    private boolean home;
    private long since;
    private int attempts;
    static boolean isHome(String pkg, String cls) {
        return "com.amazon.tv.launcher".equals(pkg)
                && "com.amazon.tv.launcher.ui.HomeActivity_vNext".equals(cls);
    }
    boolean event(String pkg, String cls, long now, boolean allowed) {
        boolean next = allowed && isHome(pkg, cls);
        if (!next) { cancel(); return false; }
        if (home) return false; // Duplicate events must not postpone or multiply work.
        home = true; since = now; attempts = 0; return true;
    }
    long delay(long now) {
        if (!home || attempts >= 2) return -1;
        return Math.max(0, since + (attempts == 0 ? DEBOUNCE_MS : FALLBACK_MS) - now);
    }
    boolean dispatch(long now, boolean allowed) {
        if (!allowed) { cancel(); return false; }
        if (delay(now) != 0) return false;
        attempts++; return true;
    }
    void cancel() { home = false; attempts = 0; }
}
