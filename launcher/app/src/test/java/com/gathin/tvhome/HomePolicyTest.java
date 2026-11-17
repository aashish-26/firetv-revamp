package com.gathin.tvhome;
import org.junit.Test;
import static org.junit.Assert.*;
public class HomePolicyTest {
    private static final String P="com.amazon.tv.launcher", H=P+".ui.HomeActivity_vNext";
    @Test public void unrelatedAndSettingsNeverRedirect() {
        HomePolicy p=new HomePolicy();
        assertFalse(p.event("com.netflix.ninja", H, 0,true));
        assertFalse(p.event(P,P+".ui.SettingsActivity",0,true));assertEquals(-1,p.delay(9000));
    }
    @Test public void duplicateEventsDoNotPostponeDebounce() {
        HomePolicy p=new HomePolicy();assertTrue(p.event(P,H,100,true));
        assertFalse(p.event(P,H,300,true));assertEquals(150,p.delay(300));
        assertTrue(p.dispatch(450,true));
    }
    @Test public void boundedFallbackDoesNotLoop() {
        HomePolicy p=new HomePolicy();p.event(P,H,100,true);
        assertFalse(p.dispatch(449,true));assertTrue(p.dispatch(450,true));
        assertEquals(5150,p.delay(450));assertTrue(p.dispatch(5600,true));
        assertEquals(-1,p.delay(5600));assertFalse(p.dispatch(10000,true));
        assertFalse(p.event(P,H,11000,true));assertEquals(-1,p.delay(12000));
    }
    @Test public void newForegroundCancelsQueuedAttempt() {
        HomePolicy p=new HomePolicy();p.event(P,H,0,true);
        p.event("com.gathin.tvhome","com.gathin.tvhome.MainActivity",100,true);
        assertFalse(p.dispatch(350,true));assertEquals(-1,p.delay(6000));
    }
    @Test public void pauseOrOwnForegroundCancelsAtDispatch() {
        HomePolicy p=new HomePolicy();p.event(P,H,0,true);assertFalse(p.dispatch(350,false));
        assertEquals(-1,p.delay(6000));
    }
    @Test public void laterRealHomeTransitionCanRedirect() {
        HomePolicy p=new HomePolicy();p.event(P,H,0,true);p.dispatch(350,true);
        p.event("com.netflix.ninja","Movie",500,true);
        assertTrue(p.event(P,H,5000,true));assertTrue(p.dispatch(5350,true));
    }
    @Test public void lifecycleCancellationDropsAllWork() {
        HomePolicy p=new HomePolicy();p.event(P,H,0,true);p.cancel();assertEquals(-1,p.delay(350));
        assertTrue(p.event(P,H,1000,true));assertEquals(350,p.delay(1000));
    }
    @Test public void wakeResetAllowsAnotherHomeAfterExhaustedAttempts() {
        HomePolicy p=new HomePolicy();p.event(P,H,0,true);p.dispatch(350,true);p.dispatch(5500,true);
        p.cancel(); // screen off/on cancels stale callbacks, does not restart arbitrary apps
        assertTrue(p.event(P,H,10000,true));assertTrue(p.dispatch(10350,true));
    }
    @Test public void directSettingsThenImmediateHomeWorks() {
        HomePolicy p=new HomePolicy();
        assertFalse(p.event("com.amazon.tv.settings.v2", "NetworkActivity", 0, true));
        assertTrue(p.event(P,H,10,true));assertTrue(p.dispatch(360,true));
    }
    @Test public void disabledPolicyDoesNotSchedule() {
        HomePolicy p=new HomePolicy();assertFalse(p.event(P,H,0,false));assertEquals(-1,p.delay(350));
    }
}
