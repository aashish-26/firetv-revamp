package com.gathin.tvhome;
import android.content.Context;
import android.util.AttributeSet;
import android.view.View;
/** Public build uses static original artwork; no video decoder or background service. */
public final class LiveBackdrop extends View {
 public LiveBackdrop(Context c, AttributeSet a) { super(c,a); setVisibility(GONE); }
 void onFailure(Runnable callback) { }
 void setRunning(boolean on) { setVisibility(GONE); }
}
