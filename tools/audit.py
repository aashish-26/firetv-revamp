#!/usr/bin/env python3
"""Read-only ADB snapshot. Explicit device serial; no shell=True or device mutations."""
import argparse, json, subprocess
from pathlib import Path
from datetime import datetime, timezone
COMMANDS = {
 "identity": ["getprop"], "packages": ["pm", "list", "packages", "-f"],
 "disabled": ["pm", "list", "packages", "-d"], "enabled": ["pm", "list", "packages", "-e"],
 "third-party": ["pm", "list", "packages", "-3"], "memory": ["dumpsys", "meminfo"],
 "storage": ["df", "-h"], "processes": ["dumpsys", "activity", "processes"],
 "home": ["cmd", "package", "resolve-activity", "--brief", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.HOME"]}
def adb_args(serial, command):
 if not serial or serial.startswith("-") or any(c.isspace() for c in serial):
  raise ValueError("Invalid serial")
 return ["adb", "-s", serial, "shell", *command]
def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument("--serial", required=True); parser.add_argument("--out", type=Path, required=True)
 args=parser.parse_args(); adb_args(args.serial, [])
 # Refuse overwriting prior snapshots.
 args.out.mkdir(parents=True, exist_ok=False)
 results={"timestamp": datetime.now(timezone.utc).isoformat(), "commands": {}}
 for name,command in COMMANDS.items():
  cmd=adb_args(args.serial,command)
  try:
   result=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
   (args.out/(name+".txt")).write_text(result.stdout+result.stderr)
   results["commands"][name]={"argv": cmd,"exit": result.returncode}
  except subprocess.TimeoutExpired:
   results["commands"][name]={"argv":cmd,"error":"timeout"}
 (args.out/"manifest.json").write_text(json.dumps(results,indent=2))
 print("Saved local diagnostics. Some commands may be unsupported; inspect manifest.json. Never publish these files.")
if __name__ == "__main__": main()
