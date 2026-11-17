import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from audit import adb_args, COMMANDS
from protected import core_packages
class Safety(unittest.TestCase):
 def test_target_required(self):
  for serial in ["", "-e", "a b"]:
   with self.assertRaises(ValueError): adb_args(serial,["getprop"])
 def test_targeted(self): self.assertEqual(adb_args("example:5555",["getprop"]),["adb","-s","example:5555","shell","getprop"])
 def test_no_mutations(self):
  for cmd in COMMANDS.values():
   self.assertFalse(set(cmd)&{"uninstall","disable-user","clear","reboot","put"})
 def test_critical_guard(self):
  names=["android","com.android.systemui","com.android.providers.media","com.mediatek.tv.service"]
  self.assertEqual(core_packages(names),names)
