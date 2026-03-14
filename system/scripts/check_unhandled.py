#!/usr/bin/env python3
"""
My-OS Unhandled Telegram Message Detector
Checks if new mobile messages have arrived in the inbox log since the last agent turn.
"""

import os
import sys
import json
import re
import datetime

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def check_unhandled(workspace_root):
    inbox_dir = os.path.join(workspace_root, "inbox")
    now = datetime.datetime.now()
    month_file = os.path.join(inbox_dir, f"{now.strftime('%Y-%m')}-mobile-inbox.md")
    
    if not os.path.exists(month_file):
        return []

    state_file = os.path.join(workspace_root, "system", "data", "last_handled_timestamp.json")
    last_handled_str = "1970-01-01 00:00:00"
    if os.path.exists(state_file):
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                last_handled_str = json.load(f).get("last_handled", "1970-01-01 00:00:00")
        except Exception:
            pass

    try:
        last_handled_dt = datetime.datetime.strptime(last_handled_str, "%Y-%m-%d %H:%M:%S")
    except Exception:
        last_handled_dt = datetime.datetime(1970, 1, 1)

    with open(month_file, "r", encoding="utf-8") as f:
        content = f.read()

    entries = content.split("---")
    new_entries = []
    
    for entry in entries:
        if "### 📌" in entry:
            match = re.search(r"\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]", entry)
            if match:
                entry_ts_str = match.group(1)
                try:
                    entry_dt = datetime.datetime.strptime(entry_ts_str, "%Y-%m-%d %H:%M:%S")
                    if entry_dt > last_handled_dt:
                        new_entries.append((entry_ts_str, entry.strip()))
                except Exception:
                    pass

    return new_entries

def update_last_handled(workspace_root, timestamp_str):
    state_file = os.path.join(workspace_root, "system", "data", "last_handled_timestamp.json")
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump({"last_handled": timestamp_str}, f, indent=2)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    
    if "--mark-all-read" in sys.argv:
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_last_handled(workspace_root, now_str)
        print(f"[Marked All Read]: {now_str}")
        sys.exit(0)

    unhandled = check_unhandled(workspace_root)
    if unhandled:
        print(f"[Unhandled Messages Found]: {len(unhandled)}")
        for ts, item in unhandled:
            print(item)
    else:
        print("[No New Messages]")
