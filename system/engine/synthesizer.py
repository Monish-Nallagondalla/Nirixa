#!/usr/bin/env python3
"""
Nirixa OS Engine - Auto-Synthesizer (LLM-Wiki Engine)
Scans raw SQLite captures, clusters recurring concepts across weeks,
and compiles living Wiki Topic Cards into resources/wiki/.
"""

import os
import sqlite3
import datetime
import re

def get_db_path(workspace_root=None):
    if not workspace_root:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    return os.path.join(workspace_root, "system", "data", "nirixa.db")

def get_wiki_dir(workspace_root=None):
    if not workspace_root:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    wiki_dir = os.path.join(workspace_root, "resources", "wiki")
    os.makedirs(wiki_dir, exist_ok=True)
    return wiki_dir

def synthesize_topics(workspace_root=None):
    db_path = get_db_path(workspace_root)
    wiki_dir = get_wiki_dir(workspace_root)
    
    if not os.path.exists(db_path):
        return 0

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, anonymized_text FROM raw_captures WHERE status = 'unread'")
    rows = cursor.fetchall()
    
    if not rows:
        conn.close()
        return 0

    # Example topic extraction clusters aligned with The Question Project
    topics = {
        "question-primitives": {
            "title": "Questions as Primitive Computational Primitives (The Question Project)",
            "keywords": ["question", "primitive", "emergence", "intelligence", "token", "inquiry", "loop"],
            "entries": []
        },
        "associative-memory": {
            "title": "Associative Memory & Cognitive Bridges (Graph Traversal)",
            "keywords": ["memory", "graph", "associative", "recall", "water heater", "bridge", "subconscious"],
            "entries": []
        },
        "open-loops": {
            "title": "Open Loops & Intrinsic Curiosity Systems",
            "keywords": ["open loop", "curiosity", "unresolved", "months", "years", "goal"],
            "entries": []
        },
        "career-leagues": {
            "title": "Career Leagues & Executive Mastery Progression",
            "keywords": ["league", "amateur", "associate", "senior engagement", "director", "ey", "consulting"],
            "entries": []
        },
        "governor-theory": {
            "title": "Human Performance & The Mind Governor",
            "keywords": ["governor", "goggins", "potential", "velocity", "ceiling", "discipline"],
            "entries": []
        }
    }

    processed_ids = []

    for row in rows:
        c_id, ts, text = row
        low = text.lower()
        processed_ids.append(c_id)
        
        for topic_key, data in topics.items():
            if any(kw in low for kw in data["keywords"]):
                data["entries"].append(f"- **[{ts}]**: {text.strip()}")

    # Compile living wiki cards
    updated_count = 0
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    for topic_key, data in topics.items():
        if data["entries"]:
            wiki_path = os.path.join(wiki_dir, f"{topic_key}.md")
            
            header = f"# {data['title']}\n\n> Auto-synthesized Wiki Card from Nirixa OS Engine.\n> Last Updated: {now_str}\n\n---\n\n## Authentic Quotes & Evidence\n"
            
            existing_content = ""
            if os.path.exists(wiki_path):
                with open(wiki_path, "r", encoding="utf-8") as f:
                    existing_content = f.read()
            else:
                existing_content = header

            new_block = "\n".join(data["entries"]) + "\n"
            full_content = existing_content + "\n" + new_block
            
            with open(wiki_path, "w", encoding="utf-8") as f:
                f.write(full_content)
                
            updated_count += 1

    # Mark captures as processed
    if processed_ids:
        placeholders = ",".join("?" * len(processed_ids))
        cursor.execute(f"UPDATE raw_captures SET status = 'processed' WHERE id IN ({placeholders})", processed_ids)
        conn.commit()

    conn.close()
    return updated_count

if __name__ == "__main__":
    count = synthesize_topics()
    print(f"[Nirixa Synthesizer] Processed and updated {count} living Wiki Topic Cards in resources/wiki/")
