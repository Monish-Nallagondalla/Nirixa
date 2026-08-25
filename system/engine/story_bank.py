#!/usr/bin/env python3
"""
Nirixa OS Engine - Story Bank Harness Module
Stores, indexes, and retrieves personal career stories, empirical scars, and achievements.
Provides the story context harness for writing high-authority posts (MoFu) and landing page About sections.
"""

import os
import sys
import sqlite3
import json
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from system.engine import db

def init_story_bank_table(db_path=None):
    if not db_path:
        db_path = db.get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS story_bank (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            situation TEXT,
            friction TEXT,
            outcome TEXT,
            metrics_json TEXT,
            tags_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_story(title, situation, friction, outcome, metrics=None, tags=None, db_path=None):
    if not db_path:
        db_path = db.get_db_path()
    init_story_bank_table(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO story_bank (title, situation, friction, outcome, metrics_json, tags_json)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        title,
        situation,
        friction,
        outcome,
        json.dumps(metrics or {}),
        json.dumps(tags or [])
    ))
    story_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return story_id

def query_stories(query_tag=None, db_path=None):
    if not db_path:
        db_path = db.get_db_path()
    init_story_bank_table(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, situation, friction, outcome, metrics_json, tags_json, created_at FROM story_bank ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    stories = []
    for r in rows:
        tags = json.loads(r[6] or "[]")
        if query_tag and query_tag.lower() not in [t.lower() for t in tags] and query_tag.lower() not in r[1].lower():
            continue
        stories.append({
            "id": r[0],
            "title": r[1],
            "situation": r[2],
            "friction": r[3],
            "outcome": r[4],
            "metrics": json.loads(r[5] or "{}"),
            "tags": tags,
            "created_at": r[7]
        })
    return stories

def deconstruct_viral_post_template(post_text):
    """
    Deconstructs any viral post into its 4 core structural components:
    Hook -> Story Bridge -> Educational Meat -> Mic Drop.
    """
    lines = [l.strip() for l in post_text.strip().split("\n") if l.strip()]
    hook = lines[0] if lines else ""
    bridge = lines[1:3] if len(lines) > 2 else []
    meat = lines[3:-2] if len(lines) > 5 else lines[1:-1]
    mic_drop = lines[-2:] if len(lines) >= 2 else lines[-1:]
    
    return {
        "hook": hook,
        "story_bridge": " ".join(bridge),
        "educational_meat": " ".join(meat),
        "mic_drop": " ".join(mic_drop),
        "template_structure": "Hook -> Story Bridge -> Educational Meat -> Mic Drop"
    }

if __name__ == "__main__":
    print("=== STORY BANK HARNESS TEST ===")
    s_id = add_story(
        title="Vibe Coding Architecture Breakthrough",
        situation="Building multi-agent autonomous system in local IDE",
        friction="LLM drift caused cascading tool failures",
        outcome="Isolated deterministic SQLite fast-path from stochastic LLMs",
        metrics={"latency_reduction": "85%", "pass_rate": "100%"},
        tags=["vibe_coding", "ai_architecture", "sqlite"]
    )
    print(f"Added Story #{s_id}")
    fetched = query_stories("vibe_coding")
    print(f"Queried Stories: {len(fetched)} found")
    print(json.dumps(fetched[0], indent=2))
