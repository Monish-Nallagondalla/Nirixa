#!/usr/bin/env python3
"""
Nirixa OS Engine - Acceptance Test Suite for Additions 1 & 2
Verifies Pluggable Reasoning Backend & Staleness/Accountability Nudge Engine.
"""

import os
import sys
import sqlite3
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
engine_dir = os.path.abspath(os.path.join(script_dir, ".."))
workspace_root = os.path.abspath(os.path.join(engine_dir, "..", ".."))

sys.path.insert(0, engine_dir)

import db
import reasoning_backend
import accountability
import evals.run_system_evals as run_system_evals

def test_addition_1_reasoning_backend():
    print("--- Testing Addition 1: Reasoning Backend & Fallback Boundary ---")
    db_path = db.get_db_path(workspace_root)
    db.init_db(db_path)

    dispatcher = reasoning_backend.ReasoningDispatcher(workspace_root=workspace_root)
    
    # 1. Ingest test capture with forced fallback
    test_text = "Acceptance Test Capture: Antigravity Pluggable Reasoning Architecture"
    c_id = db.save_capture(888888, "test_chat", test_text, test_text, source="acceptance_test")
    
    ota_id, result, used_backend = dispatcher.reason_over_capture(c_id, test_text, force_fallback=True)
    assert used_backend == "local_fallback", f"Expected 'local_fallback', got '{used_backend}'"

    # 2. Verify status is 'draft' in otas (Human boundary enforcement)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT status, refined_thesis FROM otas WHERE id = ?", (ota_id,))
    row = cursor.fetchone()
    conn.close()

    assert row is not None, "OTA draft was not saved in database"
    assert row[0] == "draft", f"Expected OTA status 'draft', got '{row[0]}'"
    print(f"[PASS] Reasoning Backend Test Passed! Saved Draft OTA #{ota_id} with status='draft' via {used_backend}.")

def test_addition_2_accountability_nudges():
    print("--- Testing Addition 2: Accountability & Engagement Nudges ---")
    db_path = db.get_db_path(workspace_root)
    db.init_db(db_path)

    acct = accountability.AccountabilityEngine(workspace_root=workspace_root)

    # 1. Save a test OTA and publish it
    c_id = db.save_capture(777777, "test_chat", "Test Published Article", "Test Published Article", source="acceptance_test")
    ota_id = db.save_ota(c_id, "Test Published Article Title", "Raw content", "Refined content", db_path=db_path)
    
    # Update status to 'published' -> Auto-triggers 24h engagement check
    db.update_ota_status(ota_id, "published", db_path=db_path)

    # 2. Verify 24h engagement reminder was created in reminders table
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT reminder_text, status FROM reminders WHERE capture_id = ?", (ota_id,))
    rem_row = cursor.fetchone()
    conn.close()

    assert rem_row is not None, "24h engagement follow-up reminder was not created"
    assert "24h Engagement Follow-Up" in rem_row[0], f"Unexpected reminder text: {rem_row[0]}"
    print(f"[PASS] 24h Engagement Follow-Up Reminder verified for Published OTA #{ota_id}: '{rem_row[0]}'")

    # 3. Fast-forward reminder time and run daily accountability audit
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    past_due = (datetime.datetime.now() - datetime.timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE reminders SET remind_at = ? WHERE capture_id = ?", (past_due, ota_id))
    conn.commit()
    conn.close()

    audit_res = acct.run_daily_accountability_audit()
    assert audit_res["total_stale"] > 0, "Accountability engine failed to detect overdue reminder/stale draft"
    assert audit_res["pushed_today"] <= audit_res["daily_cap"], "Nudge dispatch exceeded daily cap"
    print(f"[PASS] Daily Accountability Audit verified! Detected {audit_res['total_stale']} staleness items within daily cap ({audit_res['pushed_today']}/{audit_res['daily_cap']}).")

def run_all_addition_tests():
    print("==================================================")
    print("  NIRIXA OS - ADDITIONS 1 & 2 ACCEPTANCE TEST SUITE")
    print("==================================================")
    test_addition_1_reasoning_backend()
    test_addition_2_accountability_nudges()
    
    print("\n--- Running System Health Evals Suite (Track A) ---")
    evaluator = run_system_evals.SystemHealthEvaluator(workspace_root=workspace_root)
    pass_rate, passed, total = evaluator.run_all_evals()
    assert pass_rate >= 80.0, f"System health pass rate too low: {pass_rate}%"
    print("\n[PASS] ALL ACCEPTANCE TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_all_addition_tests()
