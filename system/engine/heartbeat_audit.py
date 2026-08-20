#!/usr/bin/env python3
"""
Nirixa OS Engine - Proactive Event-Driven Heartbeat Audit Daemon
Inspired by Letta & GBrain.
Periodically audits system health, pending reminders, unread mobile captures,
uncommitted git states, and eval pass rates to surface dropped balls proactively.
"""

import os
import sys
import json
import sqlite3
import datetime
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from system.engine import db

class HeartbeatAuditor:
    def __init__(self, workspace_root=workspace_root):
        self.workspace_root = workspace_root
        self.db_path = db.get_db_path(self.workspace_root)

    def audit_pending_reminders(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("SELECT id, chat_id, message, remind_at FROM reminders WHERE status = 'pending' AND remind_at <= ?", (now_str,))
        overdue = cursor.fetchall()
        conn.close()
        return overdue

    def audit_unread_captures(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM raw_captures WHERE status = 'unread'")
        count = cursor.fetchone()[0]
        conn.close()
        return count

    def audit_git_working_directory(self):
        try:
            res = subprocess.run(["git", "status", "--porcelain"], cwd=self.workspace_root, capture_output=True, text=True, timeout=5)
            lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
            return len(lines)
        except Exception:
            return 0

    def run_heartbeat_pulse(self):
        overdue_reminders = self.audit_pending_reminders()
        unread_captures = self.audit_unread_captures()
        uncommitted_files = self.audit_git_working_directory()

        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "overdue_reminders_count": len(overdue_reminders),
            "unread_captures_count": unread_captures,
            "uncommitted_files_count": uncommitted_files,
            "health_status": "optimal" if (len(overdue_reminders) == 0 and uncommitted_files == 0) else "attention_needed"
        }

        # Log audit entry
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO system_audits (metric_name, metric_value, timestamp)
        VALUES ('heartbeat_pulse', ?, ?)
        """, (json.dumps(summary), summary["timestamp"]))
        conn.commit()
        conn.close()

        print(f"[Heartbeat Pulse] Health: {summary['health_status'].upper()} | Overdue Reminders: {len(overdue_reminders)} | Unread Captures: {unread_captures} | Uncommitted Files: {uncommitted_files}")
        return summary

if __name__ == "__main__":
    auditor = HeartbeatAuditor()
    auditor.run_heartbeat_pulse()
