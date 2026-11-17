package com.gathin.tvhome;
/** Defensive normalization of persisted visual options, independent of Android. */
final class VisualOptions {
    static int bounded(int value, int count) { return value >= 0 && value < count ? value : 0; }
}
