#!/usr/bin/env python3
"""
Nirixa OS Engine - Continuous Associative Thought Graph Evolution Engine
Implements Monish's vision of how a mind works (OTA-022):
1. Dynamically links every new OTA/Thought to pre-existing OTAs via semantic & logical edges.
2. Computes Associative Thought Centrality across the entire knowledge graph.
3. Enables Nirixa OS to continuously evolve its cognitive understanding of Monish's mental model over time.
"""

import os
import sys
import sqlite3
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from system.engine import db, graph

def auto_link_ota_node(new_ota_key, label, category, related_ota_keys=None, db_path=None):
    """
    Adds a new OTA node and automatically links it to related OTAs,
    creating a continuous small-world associative graph network.
    """
    if not db_path:
        db_path = db.get_db_path()
        
    # Add node
    graph.add_node(new_ota_key, "ota", label, {"category": category}, db_path=db_path)
    
    # Connect to primary owner
    graph.add_edge("member_monish", new_ota_key, "CREATED", weight=1.0, db_path=db_path)
    
    # Auto-link related OTAs
    linked_count = 0
    if related_ota_keys:
        for rel_key in related_ota_keys:
            graph.add_edge(new_ota_key, rel_key, "ASSOCIATED_WITH", weight=1.0, db_path=db_path)
            linked_count += 1
            
    return {
        "node_key": new_ota_key,
        "label": label,
        "category": category,
        "auto_linked_edges": linked_count + 1
    }

def compute_thought_centrality(db_path=None):
    """
    Calculates edge degree centrality across all OTAs in the SQLite Knowledge Graph.
    Identifies the most central core thoughts driving Monish's operating system.
    """
    if not db_path:
        db_path = db.get_db_path()
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT target_key, COUNT(*) as degree 
        FROM graph_edges 
        GROUP BY target_key 
        ORDER BY degree DESC 
        LIMIT 10
    """)
    rows = cursor.fetchall()
    conn.close()
    
    centrality_rankings = []
    for r in rows:
        centrality_rankings.append({
            "node_key": r[0],
            "in_degree_connections": r[1]
        })
        
    return {
        "top_central_thoughts": centrality_rankings,
        "graph_evolution_status": "Continuous Small-World Network Active"
    }

if __name__ == "__main__":
    print("=== CONTINUOUS GRAPH EVOLUTION ENGINE TEST ===")
    res = auto_link_ota_node(
        "ota_022",
        "OTA-022: Continuous Associative Thought Graph Invariant",
        "cognitive_graph",
        related_ota_keys=["ota_001", "ota_011", "ota_019", "ota_020", "ota_021"]
    )
    print("Auto-Linked Node:", json.dumps(res, indent=2))
    
    cent = compute_thought_centrality()
    print("Thought Centrality Rankings:", json.dumps(cent, indent=2))
