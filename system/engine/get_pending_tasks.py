import sqlite3
import os
import sys
import subprocess

db_path = os.path.join("system", "data", "nirixa.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get pending reminders
cursor.execute("SELECT id, message, remind_at FROM reminders WHERE status = 'pending'")
reminders = cursor.fetchall()

# Format pending tasks message
tasks_text = "PENDING TASKS & DECISIONS FOR MONISH:\n\n"

tasks_text += "1. CONTENT & THOUGHT LEADERSHIP (Pick 1 for Today):\n"
tasks_text += "   - Draft 1: In-Situ UX Teardown (PhonePe Calculator + Screenshot)\n"
tasks_text += "   - Draft 2: Machine-Input Inversion Paradox (Don Norman quote)\n"
tasks_text += "   - Draft 3: What if LLM Development Stopped Today? (50x-100x prototyping speedup)\n\n"

tasks_text += "2. PENDING SYSTEM REMINDERS:\n"
if reminders:
    for r in reminders:
        tasks_text += f"   - [Reminder #{r[0]}] {r[1]} (Scheduled: {r[2]})\n"
else:
    tasks_text += "   - None (All reminders up to date)\n"

tasks_text += "\n3. AGENTIC WORKSPACE ITEMS:\n"
tasks_text += "   - Test Reddit Intelligence Radar (python system/engine/reddit_radar.py)\n"
tasks_text += "   - Review & verify 44 Original Thought Assets in knowledge graph\n"

# Send to Telegram
sys_script = os.path.join("system", "scripts", "telegram_sender.py")
subprocess.run([sys.executable, sys_script, "--chat_id", "7172048978", "--text", tasks_text])
print("Pending tasks dispatched successfully to Telegram!")
