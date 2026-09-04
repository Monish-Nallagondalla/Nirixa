
import sqlite3
import json
import os
import math

def compute_pagerank(nodes, edges, damping=0.85, max_iter=50, tol=1e-6):
    """Computes standard Google PageRank centrality for graph nodes."""
    N = len(nodes)
    if N == 0:
        return {}
        
    node_ids = [n["id"] for n in nodes]
    node_set = set(node_ids)
    
    # Build adjacency
    out_links = {nid: [] for nid in node_ids}
    in_links = {nid: [] for nid in node_ids}
    
    for src, tgt, w in edges:
        if src in node_set and tgt in node_set:
            out_links[src].append((tgt, w))
            in_links[tgt].append((src, w))
            
    # Initial PR
    pr = {nid: 1.0 / N for nid in node_ids}
    
    for _ in range(max_iter):
        new_pr = {}
        dangling_sum = sum(pr[nid] for nid in node_ids if len(out_links[nid]) == 0)
        
        for nid in node_ids:
            rank_sum = 0.0
            for src_id, w in in_links[nid]:
                total_out_w = sum(w2 for _, w2 in out_links[src_id]) or 1.0
                rank_sum += (pr[src_id] * (w / total_out_w))
                
            new_pr[nid] = ((1.0 - damping) / N) + damping * (rank_sum + (dangling_sum / N))
            
        # Check convergence
        diff = sum(abs(new_pr[nid] - pr[nid]) for nid in node_ids)
        pr = new_pr
        if diff < tol:
            break
            
    # Normalize to 0..1 scale
    max_pr = max(pr.values()) or 1.0
    return {nid: round(pr[nid] / max_pr, 4) for nid in node_ids}

def generate_ota_network_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    
    db_path = os.path.join(workspace_root, "system", "data", "nirixa.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Fetch all nodes
    cursor.execute("SELECT node_key, node_type, label, properties_json FROM graph_nodes")
    nodes_raw = cursor.fetchall()
    
    # 2. Fetch all edges
    cursor.execute("SELECT source_key, target_key, relation_type, weight, properties_json FROM graph_edges")
    edges_raw = cursor.fetchall()
    conn.close()
    
    nodes = []
    node_keys = set()
    
    pillar_colors = {
        "pillar_human_intelligence": "#38bdf8",     # Cyan
        "pillar_ai_agents": "#a855f7",              # Purple
        "pillar_product_design": "#22c55e",         # Emerald Green
        "pillar_product_management": "#f59e0b",     # Amber Gold
        "phd_master_topic": "#ef4444",              # Red Core
        "phd_rq": "#ec4899",                        # Pink
        "other": "#94a3b8"                          # Slate
    }
    
    ota_pillar_lookup = {}
    for src, tgt, rel, w, props in edges_raw:
        if rel == "GROUNDS_PILLAR" and src.startswith("pillar_") and tgt.startswith("ota_"):
            ota_pillar_lookup[tgt] = src
            
    # Calculate degrees and edge weights for PageRank
    degree_lookup = {}
    graph_edges_for_pr = []
    
    for src, tgt, rel, w, props in edges_raw:
        weight_val = w if isinstance(w, (int, float)) else 1.0
        degree_lookup[src] = degree_lookup.get(src, 0) + 1
        degree_lookup[tgt] = degree_lookup.get(tgt, 0) + 1
        graph_edges_for_pr.append((src, tgt, weight_val))
        
    for n_key, n_type, label, props_str in nodes_raw:
        props = json.loads(props_str) if props_str else {}
        node_keys.add(n_key)
        
        group = "other"
        color = pillar_colors["other"]
        val_size = 8
        
        if n_key == "phd_master_topic":
            group = "Master Core"
            color = pillar_colors["phd_master_topic"]
            val_size = 28
        elif n_key.startswith("pillar_"):
            group = "Pillar Hub"
            color = pillar_colors.get(n_key, pillar_colors["other"])
            val_size = 20
        elif n_key.startswith("phd_rq"):
            group = "Research Question"
            color = pillar_colors["phd_rq"]
            val_size = 14
        elif n_key.startswith("ota_"):
            pillar = ota_pillar_lookup.get(n_key, "pillar_human_intelligence")
            color = pillar_colors.get(pillar, "#38bdf8")
            val_size = 10 + min(degree_lookup.get(n_key, 1) * 2, 16)
            
            if pillar == "pillar_human_intelligence":
                group = "Pillar 1: Human Intelligence"
            elif pillar == "pillar_ai_agents":
                group = "Pillar 2: AI Agents"
            elif pillar == "pillar_product_design":
                group = "Pillar 3: Product Design (HACD)"
            elif pillar == "pillar_product_management":
                group = "Pillar 4: Product Management"
                
        ota_num = ""
        if n_key.startswith("ota_"):
            ota_num = n_key.replace("ota_", "OTA-").upper()
            
        nodes.append({
            "id": n_key,
            "label": label,
            "type": n_type,
            "group": group,
            "color": color,
            "size": val_size,
            "degree": degree_lookup.get(n_key, 1),
            "ota_num": ota_num,
            "properties": props
        })
        
    # Calculate PageRank Centrality across the entire graph
    pagerank_scores = compute_pagerank(nodes, graph_edges_for_pr)
    N = len(nodes)
    
    # Calculate normalized node metrics
    for n in nodes:
        nid = n["id"]
        deg = n["degree"]
        deg_centrality = round(deg / (N - 1), 4) if N > 1 else 0.0
        pr_score = pagerank_scores.get(nid, 0.1)
        
        # Authority Score (0 to 100)
        auth_score = round((0.55 * pr_score + 0.45 * (deg / 12.0)) * 100, 1)
        auth_score = min(99.5, max(15.0, auth_score))
        
        n["metrics"] = {
            "degree_centrality": deg_centrality,
            "pagerank": pr_score,
            "authority_score": auth_score
        }

    # Build links list
    links = []
    for src, tgt, rel, w, props_str in edges_raw:
        if src in node_keys and tgt in node_keys:
            props = json.loads(props_str) if props_str else {}
            weight_val = w if isinstance(w, (int, float)) else 0.85
            links.append({
                "source": src,
                "target": tgt,
                "type": rel,
                "weight": weight_val,
                "properties": props
            })
            
    network_data = {
        "metrics": {
            "total_nodes": len(nodes),
            "total_edges": len(links),
            "total_otas": len([n for n in nodes if n["id"].startswith("ota_")]),
            "total_rqs": len([n for n in nodes if n["id"].startswith("phd_rq")]),
            "total_pillars": 4,
            "density": round((2.0 * len(links)) / (len(nodes) * (len(nodes) - 1)), 4) if len(nodes) > 1 else 0
        },
        "nodes": nodes,
        "links": links
    }
    
    # 1. Save JSON
    os.makedirs(os.path.join(workspace_root, "system", "data"), exist_ok=True)
    out_path = os.path.join(workspace_root, "system", "data", "ota_network.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(network_data, f, indent=2)
        
    # 2. Inject inline into ota_explorer.html
    html_path = os.path.join(workspace_root, "system", "dashboard", "ota_explorer.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        json_js = f"window.INLINE_NETWORK_DATA = {json.dumps(network_data)};"
        
        if "/* INLINE_DATA_START */" in content and "/* INLINE_DATA_END */" in content:
            start_idx = content.find("/* INLINE_DATA_START */") + len("/* INLINE_DATA_START */")
            end_idx = content.find("/* INLINE_DATA_END */")
            new_content = content[:start_idx] + "\n" + json_js + "\n" + content[end_idx:]
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(new_content)
                
    print(f"Computed network metrics ({len(nodes)} nodes, {len(links)} links, density: {network_data['metrics']['density']})!")
    return network_data

if __name__ == "__main__":
    generate_ota_network_json()
