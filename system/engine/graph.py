import os
import sys
import sqlite3
import datetime
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from system.engine import db


def add_node(node_key, node_type, label, properties=None, db_path=None):
    if not db_path:
        db_path = db.get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    props_str = json.dumps(properties or {})
    try:
        cursor.execute("""
        INSERT OR REPLACE INTO graph_nodes (node_key, node_type, label, properties_json, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (node_key, node_type, label, props_str, now_str))
        conn.commit()
        last_id = cursor.lastrowid
    except Exception as e:
        last_id = None
    finally:
        conn.close()
    return last_id

def add_edge(source_key, target_key, relation_type, weight=1.0, properties=None, db_path=None):
    if not db_path:
        db_path = db.get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    props_str = json.dumps(properties or {})
    try:
        cursor.execute("""
        INSERT OR REPLACE INTO graph_edges (source_key, target_key, relation_type, weight, properties_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (source_key, target_key, relation_type, weight, props_str, now_str))
        conn.commit()
        last_id = cursor.lastrowid
    except Exception as e:
        last_id = None
    finally:
        conn.close()
    return last_id

def traverse_ancestry(start_node_key, max_depth=3, db_path=None):
    """
    Performs multi-hop recursive graph traversal starting from start_node_key.
    Uses SQLite WITH RECURSIVE CTE for zero-dependency execution.
    """
    if not db_path:
        db_path = db.get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    query = """
    WITH RECURSIVE graph_cte(source_key, target_key, relation_type, depth, path) AS (
        -- Base Case: Outgoing and Incoming edges from start_node_key
        SELECT source_key, target_key, relation_type, 1 AS depth,
               source_key || ' -> [' || relation_type || '] -> ' || target_key AS path
        FROM graph_edges
        WHERE source_key = ? OR target_key = ?
        
        UNION ALL
        
        -- Recursive Step
        SELECT e.source_key, e.target_key, e.relation_type, c.depth + 1,
               c.path || ' -> [' || e.relation_type || '] -> ' || e.target_key
        FROM graph_edges e
        JOIN graph_cte c ON (e.source_key = c.target_key OR e.target_key = c.source_key)
        WHERE c.depth < ? AND c.path NOT LIKE '%' || e.target_key || '%'
    )
    SELECT DISTINCT source_key, target_key, relation_type, depth, path
    FROM graph_cte
    ORDER BY depth ASC;
    """
    
    cursor.execute(query, (start_node_key, start_node_key, max_depth))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            "source_key": r[0],
            "target_key": r[1],
            "relation_type": r[2],
            "depth": r[3],
            "path": r[4]
        })
    return results

def get_subgraph(start_node_key, max_depth=2, db_path=None):
    """
    Returns nodes and edges forming a connected subgraph around start_node_key.
    Useful for GraphRAG context injection into LLM prompts.
    """
    traversals = traverse_ancestry(start_node_key, max_depth=max_depth, db_path=db_path)
    keys = set([start_node_key])
    edges = []
    for t in traversals:
        keys.add(t["source_key"])
        keys.add(t["target_key"])
        edges.append(t)
        
    if not db_path:
        db_path = db.get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    nodes = []
    if keys:
        placeholders = ",".join(["?"] * len(keys))
        cursor.execute(f"SELECT node_key, node_type, label, properties_json FROM graph_nodes WHERE node_key IN ({placeholders})", list(keys))
        for r in cursor.fetchall():
            nodes.append({
                "node_key": r[0],
                "node_type": r[1],
                "label": r[2],
                "properties": json.loads(r[3] or "{}")
            })
    conn.close()
    return {"start_node": start_node_key, "nodes": nodes, "edges": edges}

def seed_default_ota_graph(db_path=None):
    """Seeds the 15 Core OTAs and system architecture connections into the Graph Database."""
    # Seed Core OTAs
    add_node("ota_001", "ota", "OTA-001: Questions as First-Class Primitives", {"category": "epistemology"}, db_path=db_path)
    add_node("ota_003", "ota", "OTA-003: Deterministic Fast Path vs Stochastic World Models", {"category": "architecture"}, db_path=db_path)
    add_node("ota_011", "ota", "OTA-011: Thought Ancestry & Lineage", {"category": "lineage"}, db_path=db_path)
    add_node("ota_012", "ota", "OTA-012: Autonomous Self-Evolution Engine", {"category": "rl_feedback"}, db_path=db_path)
    add_node("ota_014", "ota", "OTA-014: Multi-Member Relational Graph", {"category": "multi_tenancy"}, db_path=db_path)

    # Seed Code & System Nodes
    add_node("code_identity_router", "code", "system/engine/identity_router.py", {"subsystem": "engine"}, db_path=db_path)
    add_node("code_graph_engine", "code", "system/engine/graph.py", {"subsystem": "engine"}, db_path=db_path)
    add_node("skill_household", "code", ".agents/skills/household-companion/SKILL.md", {"subsystem": "skills"}, db_path=db_path)
    add_node("member_monish", "member", "Monish (Primary Owner)", {"role": "admin"}, db_path=db_path)
    add_node("member_harshitha", "member", "Harshitha (Spouse)", {"role": "member"}, db_path=db_path)

    # Seed Relationships
    add_edge("ota_014", "code_identity_router", "IMPLEMENTED_IN", weight=1.0, db_path=db_path)
    add_edge("ota_014", "skill_household", "POWERED_BY", weight=1.0, db_path=db_path)
    add_edge("code_identity_router", "code_graph_engine", "UTILIZES", weight=1.0, db_path=db_path)
    add_edge("member_monish", "ota_014", "CREATED", weight=1.0, db_path=db_path)
    add_edge("member_harshitha", "skill_household", "COLLABORATES_ON", weight=1.0, db_path=db_path)
    add_edge("ota_001", "ota_011", "EXTENDED_BY", weight=1.0, db_path=db_path)

if __name__ == "__main__":
    db.init_db()
    seed_default_ota_graph()
    subgraph = get_subgraph("ota_014", max_depth=2)
    print(f"[Graph Core] Seeded & Verified Subgraph for 'ota_014':")
    print(json.dumps(subgraph, indent=2))
