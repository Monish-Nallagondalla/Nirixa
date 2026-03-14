#!/usr/bin/env python3
"""
Nirixa OS Engine - Continuous System Evolver
Audits SQLite performance logs, feedback ratios (+1 vs -1 rating counts), reminder statistics,
and generates an automated System Evolution Audit Report (docs/SYSTEM_EVOLUTION.md).
"""

import os
import sys
import datetime
import sqlite3

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

import db

def generate_evolution_audit(workspace_root=None):
    if not workspace_root:
        workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    db_path = db.get_db_path(workspace_root)
    briefing_data = db.get_proactive_briefing_data(db_path)

    upvotes = briefing_data["upvotes"]
    downvotes = briefing_data["downvotes"]
    total_feedback = upvotes + downvotes
    satisfaction_rate = round((upvotes / total_feedback) * 100, 1) if total_feedback > 0 else 100.0

    active_rules = db.get_active_evolution_rules(db_path)
    pending_reminders = db.get_pending_reminders_summary(db_path)
    otas_summary = db.get_ota_summary(db_path)

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    audit_markdown = f"""# Nirixa OS - System Evolution Audit Report
**Generated On**: {now_str}

---

## 1. System Performance Metrics
* **Total Mobile Captures**: {briefing_data['total_captures']}
* **Original Thought Assets (OTAs)**: {briefing_data['total_otas']}
* **Pending Scheduled Reminders**: {briefing_data['pending_reminders']}
* **User Signal Rating**: {upvotes} High-Signal (+1) | {downvotes} Low-Signal (-1)
* **Satisfaction Rate**: {satisfaction_rate}%

---

## 2. Active Learned Preference Rules (RL Reinforcement)
{active_rules}

---

## 3. Current System State
### Pending Reminders
{pending_reminders}

### Recent OTAs
{otas_summary}

---

## 4. Architectural Next Steps (Pushing to 10/10 JARVIS)
1. **Cloud Sync Bridge**: Maintain 24/7 background execution and auto-sync with GitHub.
2. **Proactive Morning Briefing**: Daily 9:00 AM push to Telegram with hardware health and agenda.
3. **Continuous Reinforcement**: Keep rating responses with `[ 👍 High-Signal ]` and `[ 👎 Low-Signal ]` to auto-tune sparring persona.
"""

    docs_dir = os.path.join(workspace_root, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    report_path = os.path.join(docs_dir, "SYSTEM_EVOLUTION.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(audit_markdown)

    return audit_markdown, report_path

import json

def take_capability_snapshot(workspace_root=None, notes=""):
    """
    Track B: Captures a Day 1 vs Day N capability snapshot in capability_snapshots table.
    """
    if not workspace_root:
        workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    db_path = db.get_db_path(workspace_root)
    db.init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Active Skill Count & Names
    skills_dir = os.path.join(workspace_root, ".agents", "skills")
    skill_names = []
    if os.path.exists(skills_dir):
        skill_names = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
    skill_names_json = json.dumps(sorted(skill_names))
    active_skill_count = len(skill_names)

    # 2. Table Count in SQLite
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
    table_count = cursor.fetchone()[0]

    # 3. Rule Count in AGENTS.md
    agents_md = os.path.join(workspace_root, ".agents", "AGENTS.md")
    rule_count = 0
    if os.path.exists(agents_md):
        with open(agents_md, "r", encoding="utf-8") as f:
            rule_count = sum(1 for line in f if line.strip().startswith("## "))

    # 4. Total OTAs and Captures
    cursor.execute("SELECT COUNT(*) FROM otas")
    total_otas = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM raw_captures")
    total_captures = cursor.fetchone()[0]

    # 5. Eval Pass Rate from eval_results
    eval_pass_rate = 100.0
    try:
        cursor.execute("SELECT status FROM eval_results ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        if rows:
            passes = sum(1 for r in rows if r[0] == "pass")
            eval_pass_rate = round((passes / len(rows)) * 100.0, 1)
    except Exception:
        pass

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO capability_snapshots 
    (snapshot_date, active_skill_count, active_skill_names, table_count, rule_count, eval_pass_rate, total_otas, total_captures, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (now_str, active_skill_count, skill_names_json, table_count, rule_count, eval_pass_rate, total_otas, total_captures, notes))
    
    snapshot_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"[Evolver] Recorded capability snapshot #{snapshot_id}: {active_skill_count} skills, {rule_count} rules, {table_count} tables.")
    return snapshot_id

if __name__ == "__main__":
    if "--snapshot" in sys.argv:
        take_capability_snapshot()
    else:
        report, path = generate_evolution_audit()
        print(f"[Evolver] Generated System Evolution Audit Report at {path}")
        print("\n--- REPORT PREVIEW ---")
        print(report[:400] + "\n...")
        take_capability_snapshot(notes="Automated audit snapshot")

