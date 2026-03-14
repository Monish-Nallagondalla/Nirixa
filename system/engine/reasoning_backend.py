#!/usr/bin/env python3
"""
Nirixa OS Engine - Pluggable Reasoning Backend Component (Addition 1)

Provides a pluggable reasoning interface for mobile captures:
`reason(capture_text, cross_domain_context) -> {draft_thesis, connections, content_angles}`

Primary Backend: `AntigravityBackend` (Gemini API / Antigravity SDK)
Fallback Backend: `LocalBackend` (`synthesizer.py` + DB context)

Boundary Principle: Output ALWAYS lands in `otas` table with `status='draft'`
for human sparring review. Decisions are NEVER auto-committed without human approval.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, script_dir)

import db
import synthesizer
import chief_of_staff

class BaseReasoningBackend:
    def reason(self, capture_text, cross_domain_context=None):
        raise NotImplementedError("Subclasses must implement reason()")

class AntigravityBackend(BaseReasoningBackend):
    def __init__(self, workspace_root=workspace_root):
        self.workspace_root = workspace_root

    def reason(self, capture_text, cross_domain_context=None):
        """Attempts reasoning via Antigravity API endpoint."""
        config_path = os.path.join(self.workspace_root, "system", "config", "config.yaml")
        env_path = os.path.join(self.workspace_root, "system", "config", ".env")

        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key and os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip()

        if not api_key:
            raise RuntimeError("No GEMINI_API_KEY available for AntigravityBackend")

        system_prompt = """You are the My-OS Antigravity Reasoning Engine.
Given a raw mobile capture and cross-domain context, analyze the core thesis, cross-domain connections, and content angles.
Respond ONLY with a valid JSON object in this exact schema:
{
  "draft_thesis": "One-line sharp thesis sentence",
  "connections": ["Connection to Career/Learning/Projects"],
  "content_angles": ["Angle 1 for X/LinkedIn", "Angle 2 for long-form"]
}"""

        user_content = f"RAW CAPTURE:\n{capture_text}\n\nCROSS-DOMAIN CONTEXT:\n{json.dumps(cross_domain_context or {})}"

        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_content}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 600, "responseMimeType": "application/json"}
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})

        with urllib.request.urlopen(req, timeout=10) as resp:
            res_json = json.loads(resp.read().decode("utf-8"))
            candidates = res_json.get("candidates", [])
            if candidates:
                text = candidates[0]["content"]["parts"][0]["text"]
                return json.loads(text)
            else:
                raise RuntimeError("Empty response candidates from Antigravity API")

class LocalBackend(BaseReasoningBackend):
    def __init__(self, workspace_root=workspace_root):
        self.workspace_root = workspace_root

    def reason(self, capture_text, cross_domain_context=None):
        """Fallback local reasoning engine using keyword heuristics and structured formatting."""
        keywords = re.findall(r'\b[A-Za-z]{4,}\b', capture_text)
        topic_str = ", ".join(list(set(keywords))[:3]) if keywords else "General Architecture"

        draft_thesis = f"First-principles thesis: {capture_text[:120]}..." if len(capture_text) > 120 else capture_text
        connections = [f"Mapped to [{topic_str}] domain in My-OS core"]
        content_angles = [
            f"X Thread: Breakdown of {topic_str}",
            f"LinkedIn Post: Lessons learned from {topic_str}"
        ]

        return {
            "draft_thesis": draft_thesis,
            "connections": connections,
            "content_angles": content_angles
        }

class ReasoningDispatcher:
    def __init__(self, workspace_root=workspace_root):
        self.workspace_root = workspace_root
        self.antigravity = AntigravityBackend(workspace_root=self.workspace_root)
        self.local = LocalBackend(workspace_root=self.workspace_root)
        self.db_path = db.get_db_path(self.workspace_root)

    def reason_over_capture(self, capture_id, capture_text, force_fallback=False):
        """
        Executes reasoning over raw capture.
        Attempts AntigravityBackend first. On failure/timeout or force_fallback,
        falls back to LocalBackend and logs metric 'reasoning_backend_fallback' to system_audits.
        Saves result into otas table with status='draft'.
        """
        cos = chief_of_staff.ChiefOfStaffDispatcher(workspace_root=self.workspace_root)
        cross_context = cos.get_cross_domain_context()

        result = None
        used_backend = "antigravity"

        if not force_fallback:
            try:
                result = self.antigravity.reason(capture_text, cross_context)
            except Exception as e:
                print(f"[Reasoning Backend Warning] Antigravity backend failed: {e}. Falling back to LocalBackend.")
                used_backend = "local_fallback"

        if not result:
            used_backend = "local_fallback"
            result = self.local.reason(capture_text, cross_context)
            db.log_audit_metric("reasoning_backend_fallback", f"Fallback triggered for capture #{capture_id}", db_path=self.db_path)

        # Boundary Enforcement: Save as status='draft' in otas for human sparring
        ota_id = db.save_ota(
            capture_id=capture_id,
            title=capture_text[:40],
            raw_thought=capture_text,
            refined_thesis=result.get("draft_thesis", capture_text),
            db_path=self.db_path
        )
        
        # Ensure status remains 'draft' (not published)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE otas SET status = 'draft' WHERE id = ?", (ota_id,))
        conn.commit()
        conn.close()

        print(f"[Reasoning Dispatcher] Processed capture #{capture_id} via '{used_backend}' -> Saved Draft OTA #{ota_id}")
        return ota_id, result, used_backend

if __name__ == "__main__":
    dispatcher = ReasoningDispatcher()
    test_ota_id, res, backend = dispatcher.reason_over_capture(1, "Testing pluggable reasoning backend architecture", force_fallback=True)
    print("Reasoning Result:", json.dumps(res, indent=2))
