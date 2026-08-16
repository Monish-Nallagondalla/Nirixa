import os
import sys
import json
import shutil
import subprocess

# Local imports
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from system.engine import db

def send_status(chat_id="7172048978"):
    db_path = db.get_db_path(workspace_root)
    size_kb = round(os.path.getsize(db_path) / 1024, 1) if os.path.exists(db_path) else 0
    total, used, free = shutil.disk_usage(workspace_root)
    free_gb = round(free / (1024 ** 3), 1)

    battery_str = "Plugged In"
    cpu_str = "Active"
    ram_str = "Normal"

    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery:
            plugged = "Charging" if battery.power_plugged else "Discharging"
            battery_str = f"{battery.percent}% ({plugged})"
        cpu_str = f"{psutil.cpu_percent(interval=0.1)}%"
        mem = psutil.virtual_memory()
        ram_str = f"{round(mem.used / (1024 ** 3), 1)} / {round(mem.total / (1024 ** 3), 1)} GB"
    except Exception:
        pass

    briefing_data = db.get_proactive_briefing_data(db_path)
    total_captures = briefing_data.get("total_captures", 0)
    total_otas = briefing_data.get("total_otas", 0)
    pending_tasks = briefing_data.get("pending_reminders", 0)

    status_text = f"""💻 LAPTOP & OS TELEMETRY DASHBOARD
----------------------------------------
🔋 Battery : {battery_str}
🧠 CPU Load: {cpu_str}
💾 RAM     : {ram_str}
📁 Disk    : {free_gb} GB free on C:\\

⚡ NIRIXA OS HEALTH
----------------------------------------
• SQLite Core  : system/data/nirixa.db ({size_kb} KB)
• Total Captures: {total_captures}
• Active OTAs  : {total_otas}
• Pending Tasks: {pending_tasks}
• Status       : Live & Listening"""

    kb = [
        [
            {"text": "⏰ Check Reminders", "callback_data": "reminders_0"},
            {"text": "📜 List OTAs", "callback_data": "otas_0"}
        ],
        [
            {"text": "🥊 Spar on Priorities", "callback_data": "spar_0"}
        ]
    ]

    sender_script = os.path.join(workspace_root, "system", "scripts", "telegram_sender.py")
    subprocess.run([
        sys.executable, sender_script,
        "--chat_id", str(chat_id),
        "--text", status_text,
        "--keyboard", json.dumps(kb)
    ])

if __name__ == "__main__":
    cid = sys.argv[1] if len(sys.argv) > 1 else "7172048978"
    send_status(cid)
