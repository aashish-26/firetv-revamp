package com.gathin.tvhome;
import android.content.Context;
import android.util.DisplayMetrics;
import androidx.recyclerview.widget.GridLayoutManager;
import androidx.recyclerview.widget.LinearSmoothScroller;
import androidx.recyclerview.widget.RecyclerView;
/** Bounds programmed focus-scroll segments; no timers, polling or background work. */
final class MotionGridLayoutManager extends GridLayoutManager {
    MotionGridLayoutManager(Context context, int spans) { super(context, spans); }
    @Override public void smoothScrollToPosition(RecyclerView view, RecyclerView.State state, int position) {
        LinearSmoothScroller motion = new LinearSmoothScroller(view.getContext()) {
            @Override protected float calculateSpeedPerPixel(DisplayMetrics metrics) {
                return 60f / metrics.densityDpi;
            }
            @Override protected int calculateTimeForScrolling(int distance) {
                return Math.min(240, super.calculateTimeForScrolling(distance));
            }
        };
        motion.setTargetPosition(position);
        startSmoothScroll(motion);
    }
}
