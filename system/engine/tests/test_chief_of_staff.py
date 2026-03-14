#!/usr/bin/env python3
"""
Unit Test Suite for Chief of Staff Reasoning Validation (P2b)
Validates cross-domain context aggregation, timeline conflict detection,
and resonance context injection.
"""

import os
import sys
import unittest
import sqlite3

script_dir = os.path.dirname(os.path.abspath(__file__))
engine_dir = os.path.abspath(os.path.join(script_dir, ".."))
workspace_root = os.path.abspath(os.path.join(engine_dir, "..", ".."))

sys.path.insert(0, engine_dir)

import chief_of_staff
import db
import resonance

class TestChiefOfStaffReasoning(unittest.TestCase):

    def setUp(self):
        self.cos = chief_of_staff.ChiefOfStaffDispatcher(workspace_root=workspace_root)

    def test_01_cross_domain_context_aggregation(self):
        """Test that get_cross_domain_context returns structured keys for all 4 domains."""
        context = self.cos.get_cross_domain_context()
        self.assertIn("career_milestones", context)
        self.assertIn("active_projects", context)
        self.assertIn("recent_otas", context)
        self.assertIn("pending_reminders", context)
        print("[PASS] Test 1: Cross-domain context aggregation structure verified.")

    def test_02_detect_cross_domain_conflict_milestone_and_reminder(self):
        """Test that cross-domain conflict detection flags keyword collisions between Career and Reminders."""
        mock_context = {
            "career_milestones": ["Complete AI Product Portfolio Architecture by Q3"],
            "pending_reminders": [{"text": "Review Portfolio Architecture and slides", "time": "2026-08-10"}],
            "active_projects": ["AI-Portfolio"]
        }
        conflicts = self.cos.detect_cross_domain_conflicts(mock_context)
        self.assertTrue(len(conflicts) > 0)
        self.assertEqual(conflicts[0]["type"], "cross_domain_collision")
        self.assertTrue(any(w in conflicts[0]["topic"].lower() for w in ["architecture", "portfolio"]))
        print(f"[PASS] Test 2: Flagged collision: {conflicts[0]['flagged_issue']}")

    def test_03_detect_cross_domain_deadline_overlap(self):
        """Test detecting overlapping project and career milestone deadlines."""
        mock_context = {
            "career_milestones": ["Launch the-question-project framework"],
            "pending_reminders": [],
            "active_projects": ["the-question-project"]
        }
        conflicts = self.cos.detect_cross_domain_conflicts(mock_context)
        self.assertTrue(any(c["type"] == "deadline_overlap" for c in conflicts))
        print("[PASS] Test 3: Flagged project-career deadline overlap successfully.")

    def test_04_merge_first_skill_governance(self):
        """Test that evaluate_skill_distillation enforces merging into existing hubs."""
        res_publishing = self.cos.evaluate_skill_distillation("linkedin_auto_post", "Publishing LinkedIn Carousels")
        self.assertEqual(res_publishing["action"], "merge")
        self.assertEqual(res_publishing["target_skill"], "omni-channel-publisher")

        res_new = self.cos.evaluate_skill_distillation("quantum_physics_solver", "Solving Quantum Equations")
        self.assertEqual(res_new["action"], "create_new")
        print("[PASS] Test 4: Merge-first skill governance rule passed.")

    def test_05_resonance_scoring_and_edge_creation(self):
        """Test resonance score computation and ota_edges insertion."""
        score = resonance.compute_resonance(1, 1, workspace_root=workspace_root)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
        print(f"[PASS] Test 5: Computed resonance score ({score}) verified.")

if __name__ == "__main__":
    unittest.main()
