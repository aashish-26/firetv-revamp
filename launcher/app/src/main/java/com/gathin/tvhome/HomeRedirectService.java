package com.gathin.tvhome;

import android.accessibilityservice.AccessibilityService;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
import android.os.Looper;
import android.os.SystemClock;
import android.content.BroadcastReceiver;
import android.content.IntentFilter;
import android.util.Log;
import android.view.accessibility.AccessibilityEvent;

/** Optional system-bound window observer; no key filtering, screen content, or settings writes. */
public class HomeRedirectService extends AccessibilityService {
    private static final String PREFS = "home_redirect";
    private static long settingsGraceUntil;
    private String lastPackage = "", lastClass = "";
    private boolean settingsSession;
    private boolean receiverRegistered;
    private final BroadcastReceiver screenState = new BroadcastReceiver() {
        @Override public void onReceive(Context context, Intent intent) {
            cancel();
            Log.i("CleanTV", Intent.ACTION_SCREEN_ON.equals(intent.getAction()) ? "screen_on" : "screen_off");
            if (Intent.ACTION_SCREEN_ON.equals(intent.getAction()) && !settingsSession
                    && HomePolicy.isHome(lastPackage, lastClass) && allowed()) {
                policy.event(lastPackage, lastClass, SystemClock.uptimeMillis(), true);
                schedule();
            }
        }
    };
    private final Handler handler = new Handler(Looper.getMainLooper());
    private final HomePolicy policy = new HomePolicy();
    private final Runnable redirect = new Runnable() {
        @Override public void run() {
            long now = SystemClock.uptimeMillis();
            if (policy.dispatch(now, allowed())) {
                Log.i("CleanTV", "redirect_dispatch uptime=" + now);
                openLauncher();
            }
            schedule();
        }
    };
    private boolean allowed() {
        return isEnabled(this) && SystemClock.uptimeMillis() >= settingsGraceUntil && !MainActivity.isForeground;
    }
    private void schedule() {
        handler.removeCallbacks(redirect);
        long delay = policy.delay(SystemClock.uptimeMillis());
        if (delay >= 0) handler.postDelayed(redirect, delay);
    }
    private void cancel() { handler.removeCallbacks(redirect); policy.cancel(); }
    @Override protected void onServiceConnected() {
        super.onServiceConnected(); cancel();
        Log.i("CleanTV", "redirect_connected");
        IntentFilter screenFilter = new IntentFilter(Intent.ACTION_SCREEN_ON);
        screenFilter.addAction(Intent.ACTION_SCREEN_OFF);
        if (!receiverRegistered) { registerReceiver(screenState, screenFilter); receiverRegistered = true; }
        if (SystemClock.elapsedRealtime() < 180_000 && allowed()) openLauncher();
    }
    @Override public void onAccessibilityEvent(AccessibilityEvent event) {
        if (event.getEventType() != AccessibilityEvent.TYPE_WINDOW_STATE_CHANGED
                || event.getPackageName() == null || event.getClassName() == null) return;
        String pkg = event.getPackageName().toString(), cls = event.getClassName().toString();
        lastPackage = pkg; lastClass = cls;
        if (pkg.startsWith("com.amazon.tv.settings") || pkg.startsWith("com.amazon.tv.quicksettings")) {
            settingsSession = true; // Dedicated sections never suppress a real Home press.
        } else if (pkg.equals("com.amazon.tv.launcher") && cls.contains("SettingsActivity")) {
            settingsSession = true;
            if (SystemClock.uptimeMillis() >= settingsGraceUntil) pauseForSettings(this);
        }
        if (HomePolicy.isHome(pkg, cls) && SystemClock.uptimeMillis() >= settingsGraceUntil) settingsSession = false;
        boolean fresh = policy.event(pkg, cls, SystemClock.uptimeMillis(), HomePolicy.isHome(pkg, cls) && allowed());
        if (fresh) Log.i("CleanTV", "amazon_home_event uptime=" + SystemClock.uptimeMillis());
        schedule();
    }
    @Override public void onInterrupt() { cancel(); }
    private void disconnect() {
        cancel();
        if (receiverRegistered) { unregisterReceiver(screenState); receiverRegistered = false; }
    }
    @Override public boolean onUnbind(Intent intent) { disconnect(); return super.onUnbind(intent); }
    @Override public void onDestroy() { disconnect(); super.onDestroy(); }
    private void openLauncher() {
        try { startActivity(new Intent(this, MainActivity.class)
                .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_NO_ANIMATION)); }
        catch (RuntimeException error) { Log.w("CleanTV", "Redirect rejected; Amazon remains accessible"); }
    }
    static boolean isEnabled(Context ctx) {
        return ctx.getSharedPreferences(PREFS, MODE_PRIVATE).getBoolean("enabled", true);
    }
    static boolean setEnabled(Context ctx, boolean on) {
        ctx.getSharedPreferences(PREFS, MODE_PRIVATE).edit()
                .putBoolean("enabled", on).remove("paused").remove("pause_boot").apply();
        return true;
    }
    // A short transition guard, not a persisted "stay on Amazon" mode.
    static void pauseForSettings(Context ctx) {
        settingsGraceUntil = SystemClock.uptimeMillis() + 2000;
    }
    static void resumeFromLauncher(Context ctx) {
        settingsGraceUntil = 0;
        android.content.SharedPreferences p = ctx.getSharedPreferences(PREFS, MODE_PRIVATE);
        if (p.contains("paused") || p.contains("pause_boot")) {
            p.edit().remove("paused").remove("pause_boot").apply();
        }
    }
}
