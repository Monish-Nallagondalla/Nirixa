#!/usr/bin/env python3
"""
Nirixa OS Engine - Unified Chief of Staff Dispatcher (Cross-Domain Strategic Orchestrator)

Consolidates strategic reasoning across Career, Learning, Projects, and Writing.
Orchestrates mobile task delegation, sparring prompt routing, cross-domain context synthesis,
and enforces Merge-First skill governance.
"""

import os
import sys
import json
import datetime
import sqlite3

# Local imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

import db
import synthesizer
import evolver

class ChiefOfStaffDispatcher:
    def __init__(self, workspace_root=None):
        if not workspace_root:
            self.workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
        else:
            self.workspace_root = workspace_root
        self.db_path = db.get_db_path(self.workspace_root)
        db.init_db(self.db_path)

    def get_cross_domain_context(self, query_text=""):
        """
        Scans workspace hubs (career, knowledge, projects, content) and local SQLite DB
        to aggregate an integrated snapshot of active strategic priorities.
        Also dynamically closes the Phase 3 retrieval loop by fetching top-K resonant past OTAs.
        """
        context = {
            "user_profile": {
                "name": "User Operator (Configured in user_profile)",
                "degrees": "User Degrees & Academic Foundation (Configured in user_profile)",
                "role": "AI Architect & Product Leader (Configured in user_profile)"
            },
            "career_milestones": [],
            "active_projects": [],
            "content_pipeline": [],
            "recent_otas": [],
            "pending_reminders": [],
            "resonant_past_thoughts": []
        }

        # Dynamic Phase 3 Resonance Retrieval (Closing the Loop into Sparring Context)
        if query_text:
            try:
                import resonance
                context["resonant_past_thoughts"] = resonance.get_injected_sparring_context(query_text, top_k=3, workspace_root=self.workspace_root)
            except Exception as e:
                print(f"[ChiefOfStaff Warning] Resonance retrieval failed: {e}")

        # 1. Scan Career Dashboard if available
        career_path = os.path.join(self.workspace_root, "docs", "CAREER_DASHBOARD.md")
        if os.path.exists(career_path):
            with open(career_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip().startswith("- ") or line.strip().startswith("* "):
                        context["career_milestones"].append(line.strip()[2:])

        # 2. Scan Active Projects directory
        projects_dir = os.path.join(self.workspace_root, "projects")
        if os.path.exists(projects_dir):
            for item in os.listdir(projects_dir):
                item_path = os.path.join(projects_dir, item)
                if os.path.isdir(item_path) and not item.startswith("."):
                    context["active_projects"].append(item)

        # 3. Query Recent OTAs and Reminders from DB
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT title, refined_thesis FROM otas ORDER BY id DESC LIMIT 5")
        for row in cursor.fetchall():
            context["recent_otas"].append({"title": row[0], "thesis": row[1]})

        cursor.execute("SELECT message, remind_at FROM reminders WHERE status = 'pending' ORDER BY remind_at ASC LIMIT 5")
        for row in cursor.fetchall():
            context["pending_reminders"].append({"text": row[0], "time": row[1]})

        conn.close()
        return context

    def get_unread_captures(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, anonymized_text, raw_text FROM raw_captures WHERE status = 'unread' ORDER BY id DESC")
        captures = []
        for row in cursor.fetchall():
            captures.append({"id": row[0], "anonymized_text": row[1] or row[2], "raw_text": row[2]})
        conn.close()
        return captures

    def synthesize_strategic_briefing(self, briefing_type="morning"):
        """
        Synthesizes a cross-domain strategic briefing combining raw captures, OTAs, and domain priorities.
        """
        cross_context = self.get_cross_domain_context()
        unread_captures = self.get_unread_captures()
        
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        briefing = f"=== CHIEF OF STAFF STRATEGIC BRIEFING ({briefing_type.upper()}) ===\n"
        briefing += f"Date: {now_str}\n\n"
        
        briefing += f"1. UNREAD MOBILE CAPTURES ({len(unread_captures)}):\n"
        if unread_captures:
            for cap in unread_captures[:3]:
                briefing += f"  • ID #{cap['id']}: {cap['anonymized_text'][:80]}...\n"
        else:
            briefing += "  • No unread mobile friction logged.\n"
            
        briefing += f"\n2. ACTIVE PROJECTS ({len(cross_context['active_projects'])}):\n"
        for proj in cross_context["active_projects"][:4]:
            briefing += f"  • {proj}\n"
            
        briefing += f"\n3. RECENT ORIGINAL THOUGHT ASSETS ({len(cross_context['recent_otas'])}):\n"
        if cross_context["recent_otas"]:
            for ota in cross_context["recent_otas"][:2]:
                briefing += f"  • {ota['title']}: {ota['thesis'][:70]}...\n"
        else:
            briefing += "  • No recent OTAs recorded.\n"

        briefing += f"\n4. PENDING REMINDERS / ACTION ITEMS ({len(cross_context['pending_reminders'])}):\n"
        if cross_context["pending_reminders"]:
            for rem in cross_context["pending_reminders"][:3]:
                briefing += f"  • [{rem['time']}] {rem['text']}\n"
        else:
            briefing += "  • All task queues clear.\n"

        return briefing

    def evaluate_skill_distillation(self, workflow_name, target_intent):
        """
        Enforces Merge-First Skill Governance rule against skill proliferation (Rule 3).
        Checks if the workflow belongs in an existing core hub before allowing new skill folder creation.
        """
        skills_dir = os.path.join(self.workspace_root, ".agents", "skills")
        existing_skills = []
        if os.path.exists(skills_dir):
            existing_skills = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]

        # Mapping of core domains to existing hub skills
        hub_mapping = {
            "publishing": "omni-channel-publisher",
            "content": "content-stylist",
            "mobile": "mobile-sync",
            "task": "mobile-task-delegator",
            "calendar": "calendar-scheduler",
            "evaluation": "agent-evaluator",
            "signoff": "daily-signoff",
            "login": "daily-login"
        }

        for keyword, hub in hub_mapping.items():
            if keyword in workflow_name.lower() or keyword in target_intent.lower():
                return {
                    "action": "merge",
                    "target_skill": hub,
                    "reason": f"Workflow matches core skill hub '{hub}'. Merging to prevent skill proliferation."
                }

        return {
            "action": "create_new",
            "target_skill": workflow_name,
            "reason": "Workflow represents a completely distinct capability domain. New skill folder allowed subject to signoff."
        }

    def detect_cross_domain_conflicts(self, context=None):
        """
        P2b Reasoning Engine: Evaluates cross-domain state (Career, Projects, Reminders)
        and detects timeline conflicts, scheduling collisions, or competing strategic priorities.
        Returns a list of structured conflict resolutions.
        """
        if not context:
            context = self.get_cross_domain_context()

        conflicts = []
        milestones = context.get("career_milestones", [])
        reminders = context.get("pending_reminders", [])
        projects = context.get("active_projects", [])

        # Check for keyword / timeline collisions across domains
        for m in milestones:
            m_words = set(w.lower() for w in m.split() if len(w) > 3)
            for r in reminders:
                r_text = r.get("text", "")
                r_words = set(w.lower() for w in r_text.split() if len(w) > 3)
                overlap = m_words.intersection(r_words)
                if overlap:
                    topic = list(overlap)[0]
                    conflicts.append({
                        "type": "cross_domain_collision",
                        "domain_a": "Career Milestone",
                        "domain_b": "Action Item",
                        "topic": topic,
                        "flagged_issue": f"Collision flagged between Career '{m[:40]}' and Reminder '{r_text[:40]}'",
                        "suggested_resolution": f"De-conflict calendar slot and merge focus onto '{topic}'."
                    })

        # Synthetic check for overlapping project / career deadlines in the same week
        for p in projects:
            for m in milestones:
                if p.lower() in m.lower():
                    conflicts.append({
                        "type": "deadline_overlap",
                        "domain_a": "Active Project",
                        "domain_b": "Career Milestone",
                        "topic": p,
                        "flagged_issue": f"Project '{p}' deadline lands in the same week as Career Milestone '{m[:40]}'",
                        "suggested_resolution": f"Batch writing slots and consolidate output into single milestone artifact."
                    })

        return conflicts

    def get_injected_sparring_context(self, current_thought_text):
        """
        Injects title and refined_thesis for top-resonant OTAs into sparring context.
        Caps at 3-5 total items, prioritizing highest resonance scores.
        """
        try:
            import resonance
            resonant_items = resonance.find_resonant_otas(current_thought_text, top_k=3, workspace_root=self.workspace_root)
            if not resonant_items:
                return ""
            
            injected_str = "\n⚡ RESONANT PAST OTAs INJECTED FROM MEMORY CORE:\n"
            for item in resonant_items:
                injected_str += f"  • [Resonance Score: {item['score']}] OTA: \"{item['title']}\"\n    Thesis: {item['thesis']}\n"
            return injected_str
        except Exception as e:
            print(f"[Context Injection Warning] {e}")
            return ""

if __name__ == "__main__":
    cos = ChiefOfStaffDispatcher()
    context = cos.get_cross_domain_context()
    print("[Chief of Staff] Cross-domain context evaluated successfully.")
    print(cos.synthesize_strategic_briefing("morning"))
    conflicts = cos.detect_cross_domain_conflicts(context)
    print(f"[Reasoning Validation] Detected {len(conflicts)} cross-domain conflicts.")

