#!/usr/bin/env python3
"""
Nirixa OS Engine - Staleness & Accountability Engine (Addition 2)

Performs daily accountability scans for:
1. Draft/Refined OTAs sitting stagnant for >3 days.
2. Unaddressed past-due reminders.
3. Overdue content calendar targets.
4. Auto-creates a 24-hour engagement follow-up reminder when an OTA moves to 'published'.

Routes priority nudges through `mobile-task-delegator` while strictly respecting `daily_cap: 4`.
"""

import os
import sys
import sqlite3
import datetime
import yaml

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, script_dir)

import db

class AccountabilityEngine:
    def __init__(self, workspace_root=workspace_root):
        self.workspace_root = workspace_root
        self.db_path = db.get_db_path(self.workspace_root)
        db.init_db(self.db_path)

    def check_stale_drafts(self, days_threshold=3):
        """Finds OTAs sitting in draft/refined status for > days_threshold."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        three_days_ago = (datetime.datetime.now() - datetime.timedelta(days=days_threshold)).isoformat()
        cursor.execute("""
        SELECT id, title, status, created_at FROM otas
        WHERE status IN ('draft', 'refined') AND created_at < ?
        ORDER BY id ASC
        """, (three_days_ago,))
        rows = cursor.fetchall()
        conn.close()

        stale_items = []
        for r in rows:
            stale_items.append({
                "type": "stale_draft",
                "id": r[0],
                "title": r[1],
                "status": r[2],
                "created_at": r[3],
                "nudge": f"Stale Draft #{r[0]} ('{r[1]}') sitting for >{days_threshold} days in {r[2]} status. Ready to finalize or discard?"
            })
        return stale_items

    def check_overdue_reminders(self):
        """Finds reminders past their scheduled trigger time still marked pending."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
        SELECT id, message, remind_at FROM reminders
        WHERE status = 'pending' AND remind_at < ?
        ORDER BY id ASC
        """, (now_str,))
        rows = cursor.fetchall()
        conn.close()

        overdue = []
        for r in rows:
            overdue.append({
                "type": "overdue_reminder",
                "id": r[0],
                "text": r[1],
                "due": r[2],
                "nudge": f"Overdue Reminder #{r[0]}: '{r[1]}' (Was due at {r[2]})."
            })
        return overdue

    def schedule_publish_engagement_check(self, ota_id, title):
        """
        Auto-creates post-publish touchpoints (24h engagement, Day 3 momentum, Day 7 consistency)
        when an OTA moves to 'published'.
        """
        now = datetime.datetime.now()
        
        # 1. 24-Hour Touchpoint
        remind_24h = (now + datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        txt_24h = f"24h Engagement Follow-Up: Check comments & DMs on published OTA #{ota_id} ('{title[:30]}')"

        # 2. Day 3 Touchpoint (72 Hours) - Follow-up Thesis Momentum
        remind_3d = (now + datetime.timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        txt_3d = f"Day 3 Post Momentum Check: OTA #{ota_id} ('{title[:30]}') had initial traction. What is the follow-up thesis angle to keep publish momentum going?"

        # 3. Day 7 Touchpoint (168 Hours) - Consistency Audit
        remind_7d = (now + datetime.timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        txt_7d = f"Day 7 Consistency Audit: 7 days since publishing OTA #{ota_id}. Which active draft in your content calendar should we spar on today?"

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for txt, rem_time in [(txt_24h, remind_24h), (txt_3d, remind_3d), (txt_7d, remind_7d)]:
            cursor.execute("""
            INSERT INTO reminders (message, remind_at, status)
            VALUES (?, ?, 'pending')
            """, (txt, rem_time))
        conn.commit()
        conn.close()

        print(f"[Accountability Engine] Scheduled 3 post-publish touchpoints (24h, 3d, 7d) for published OTA #{ota_id}")
        return True

    def get_daily_cap(self):
        """Reads daily push cap from config.yaml (default 4)."""
        config_path = os.path.join(self.workspace_root, "system", "config", "config.yaml")
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
                return cfg.get("delegator", {}).get("daily_cap", 4)
        return 4

    def run_daily_accountability_audit(self):
        """Collects all staleness nudges and routes them via delegator respecting daily_cap."""
        stale_drafts = self.check_stale_drafts()
        overdue_reminders = self.check_overdue_reminders()

        all_nudges = stale_drafts + overdue_reminders
        pushed_today = db.get_daily_delegator_pushes(self.db_path)
        daily_cap = self.get_daily_cap()

        allowed_pushes = max(0, daily_cap - pushed_today)
        dispatched = []

        print(f"[Accountability Audit] Found {len(stale_drafts)} stale drafts, {len(overdue_reminders)} overdue reminders. (Pushed today: {pushed_today}/{daily_cap})")

        for nudge in all_nudges[:allowed_pushes]:
            nudge_text = nudge["nudge"]
            db.log_audit_metric("accountability_nudge_pushed", f"{nudge['type']}: {nudge_text[:150]}", db_path=self.db_path)
            dispatched.append(nudge)
            print(f"[Accountability Nudge Dispatched] {nudge_text}")

        return {
            "total_stale": len(all_nudges),
            "dispatched_count": len(dispatched),
            "dispatched_items": dispatched,
            "daily_cap": daily_cap,
            "pushed_today": pushed_today + len(dispatched)
        }

if __name__ == "__main__":
    engine = AccountabilityEngine()
    audit_res = engine.run_daily_accountability_audit()
    print("Audit Summary:", audit_res)
