#!/usr/bin/env python3
"""
Nirixa OS - Model Context Protocol (MCP) Server
Exposes Nirixa's 3-Layer Memory Core, OTAs, and Inquiries as standard MCP tools
for Cursor, Windsurf, Claude Code, Antigravity, and any IDE-agnostic agent.
"""

import os
import sys
import json
import sqlite3

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, script_dir)

import db
import resonance

def handle_mcp_request(request_json):
    """
    Standard JSON-RPC handler for MCP tool calls.
    Supported Tools:
    - search_memory: Full-text BM25 search + 3-signal vector resonance
    - get_relevant_otas: Retrieves active Original Thought Assets
    - get_user_profile: Retrieves user baseline & family demographics
    - get_active_goals: Retrieves 30-year life milestones & TED Talk targets
    - record_thought: Appends a new thought into SQLite and monthly inbox
    """
    method = request_json.get("method")
    params = request_json.get("params", {})
    
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "search_memory",
                    "description": "Performs hybrid RRF search across Nirixa OS long-term memory and captures.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"]
                    }
                },
                {
                    "name": "get_relevant_otas",
                    "description": "Retrieves top matching Original Thought Assets (OTAs) for cognitive context.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}, "top_k": {"type": "integer", "default": 3}}
                    }
                },
                {
                    "name": "get_active_goals",
                    "description": "Retrieves strategic life milestones and 30-year compounding targets.",
                    "inputSchema": {"type": "object", "properties": {}}
                },
                {
                    "name": "record_thought",
                    "description": "Permanently saves a new thought or scar into local SQLite memory.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"thought": {"type": "string"}},
                        "required": ["thought"]
                    }
                }
            ]
        }
        
    elif method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        if name == "search_memory":
            q = arguments.get("query", "")
            matches = resonance.get_injected_sparring_context(q, top_k=5, workspace_root=workspace_root)
            return {"content": [{"type": "text", "text": json.dumps(matches, indent=2)}]}
            
        elif name == "get_relevant_otas":
            q = arguments.get("query", "")
            top_k = arguments.get("top_k", 3)
            otas = resonance.find_resonant_otas(q, top_k=top_k, workspace_root=workspace_root)
            return {"content": [{"type": "text", "text": json.dumps(otas, indent=2)}]}
            
        elif name == "get_active_goals":
            conn = sqlite3.connect(db.get_db_path(workspace_root))
            c = conn.cursor()
            c.execute("SELECT milestone, target_year, category FROM life_milestones ORDER BY target_year ASC")
            goals = [{"milestone": r[0], "target_year": r[1], "category": r[2]} for r in c.fetchall()]
            conn.close()
            return {"content": [{"type": "text", "text": json.dumps(goals, indent=2)}]}
            
        elif name == "record_thought":
            thought = arguments.get("thought", "")
            capture_id = db.save_raw_capture(thought, source="mcp_ide", status="unread", workspace_root=workspace_root)
            return {"content": [{"type": "text", "text": f"Successfully stored thought #{capture_id} in Nirixa OS memory core."}]}
            
    return {"error": {"code": -32601, "message": f"Method {method} not found"}}

if __name__ == "__main__":
    # Standard stdio JSON-RPC loop for IDEs
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample_req = {"method": "tools/list"}
        print(json.dumps(handle_mcp_request(sample_req), indent=2))
    else:
        for line in sys.stdin:
            if line.strip():
                try:
                    req = json.loads(line)
                    res = handle_mcp_request(req)
                    sys.stdout.write(json.dumps(res) + "\n")
                    sys.stdout.flush()
                except Exception as e:
                    err = {"error": {"code": -32700, "message": str(e)}}
                    sys.stdout.write(json.dumps(err) + "\n")
                    sys.stdout.flush()
