package com.gathin.tvhome;
import org.junit.Test;
import static org.junit.Assert.assertEquals;
public class VisualOptionsTest {
 @Test public void invalidPersistedOptionsUseDefault() {
  assertEquals(0, VisualOptions.bounded(-1,4));
  assertEquals(0, VisualOptions.bounded(Integer.MAX_VALUE,4));
  assertEquals(0, VisualOptions.bounded(4,4));
 }
 @Test public void validOptionsSurvive() {
  for(int i=0;i<4;i++) assertEquals(i,VisualOptions.bounded(i,4));
 }
}
