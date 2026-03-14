#!/usr/bin/env python3
"""
Nirixa OS Engine - Phase 3 Resonance Engine (Vector Embeddings, Cosine Similarity & Graph Edges)

Manages text embeddings via sqlite-vec, calculates 3-signal resonance scores,
maintains ota_edges graph linkages, and retrieves resonant OTAs for sparring context.
"""

import os
import sys
import math
import json
import yaml
import sqlite3
import datetime
import struct

# Local imports
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, script_dir)

import db

try:
    import sqlite_vec
    HAS_SQLITE_VEC = True
except ImportError:
    HAS_SQLITE_VEC = False

def load_resonance_config(workspace_root=workspace_root):
    config_path = os.path.join(workspace_root, "system", "config", "config.yaml")
    defaults = {
        "weight_similarity": 0.6,
        "weight_recency": 0.2,
        "weight_domain": 0.2,
        "threshold_edge": 0.85,
        "decay_half_life_days": 90
    }
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                cfg = yaml.safe_load(f) or {}
                res_cfg = cfg.get("resonance", {})
                for k, v in res_cfg.items():
                    defaults[k] = float(v)
        except Exception as e:
            print(f"[Resonance Config Warning] {e}")
    return defaults

def generate_text_embedding(text, dim=384):
    """
    Generates a deterministic 384-dimensional normalized float32 vector embedding for text
    using term projection & n-gram feature hashing.
    """
    if not text:
        vec = [0.0] * dim
        return vec

    vec = [0.0] * dim
    words = text.lower().split()
    
    # 1-gram feature hashing
    for word in words:
        h = hash(word)
        idx = abs(h) % dim
        sign = 1.0 if (h >> 3) % 2 == 0 else -1.0
        vec[idx] += sign * (1.0 + math.log(1 + len(word)))

    # 2-gram feature hashing
    for i in range(len(words) - 1):
        bigram = f"{words[i]}_{words[i+1]}"
        h = hash(bigram)
        idx = abs(h) % dim
        sign = 1.0 if (h >> 3) % 2 == 0 else -1.0
        vec[idx] += sign * 1.5

    # L2 Normalization
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 1e-9:
        vec = [v / norm for v in vec]
    else:
        vec = [1.0 / math.sqrt(dim)] * dim

    return vec

def save_ota_embedding(ota_id, text, workspace_root=workspace_root):
    """Generates and persists a 384d vector embedding into vec_otas virtual table."""
    db_path = db.get_db_path(workspace_root)
    vec = generate_text_embedding(text, dim=384)
    
    conn = sqlite3.connect(db_path)
    if HAS_SQLITE_VEC:
        try:
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            conn.enable_load_extension(False)
            
            vec_bytes = sqlite_vec.serialize_float32(vec)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vec_otas WHERE ota_id = ?", (ota_id,))
            cursor.execute("INSERT INTO vec_otas(ota_id, embedding) VALUES (?, ?)", (ota_id, vec_bytes))
            conn.commit()
            print(f"[Resonance Engine] Stored sqlite-vec embedding for OTA #{ota_id}")
        except Exception as e:
            print(f"[sqlite-vec save warning] {e}")
    conn.close()
    return vec

def cosine_similarity(vec_a, vec_b):
    """Computes cosine similarity between two float vectors."""
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a < 1e-9 or norm_b < 1e-9:
        return 0.0
    return max(0.0, min(1.0, dot / (norm_a * norm_b)))

def compute_resonance(ota_id_a, ota_id_b, workspace_root=workspace_root):
    """
    Computes 3-signal resonance score between two OTAs:
    Score = w_sim * cosine_sim + w_recency * recency_decay + w_domain * domain_overlap
    """
    cfg = load_resonance_config(workspace_root)
    db_path = db.get_db_path(workspace_root)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, title, refined_thesis, created_at FROM otas WHERE id IN (?, ?)", (ota_id_a, ota_id_b))
    rows = cursor.fetchall()
    conn.close()
    
    if len(rows) < 2:
        return 0.0

    row_a = rows[0] if rows[0][0] == ota_id_a else rows[1]
    row_b = rows[1] if rows[1][0] == ota_id_b else rows[0]

    # Signal 1: Cosine Similarity
    vec_a = generate_text_embedding(f"{row_a[1]} {row_a[2]}")
    vec_b = generate_text_embedding(f"{row_b[1]} {row_b[2]}")
    sim_score = cosine_similarity(vec_a, vec_b)

    # Signal 2: Recency Decay (exponential with half-life)
    try:
        dt_a = datetime.datetime.fromisoformat(row_a[3])
        dt_b = datetime.datetime.fromisoformat(row_b[3])
        days_diff = abs((dt_a - dt_b).total_seconds()) / 86400.0
    except Exception:
        days_diff = 0.0

    half_life = cfg["decay_half_life_days"]
    lambda_decay = math.log(2.0) / half_life
    recency_score = math.exp(-lambda_decay * days_diff)

    # Signal 3: Domain Overlap
    # Check keyword domain overlap across titles/theses
    text_a_lower = f"{row_a[1]} {row_a[2]}".lower()
    text_b_lower = f"{row_b[1]} {row_b[2]}".lower()
    domains = ["career", "learning", "projects", "engineering", "ai", "product"]
    domain_overlap = 0.0
    for d in domains:
        if d in text_a_lower and d in text_b_lower:
            domain_overlap = 1.0
            break

    # Total Weighted Score
    score = (cfg["weight_similarity"] * sim_score) + \
            (cfg["weight_recency"] * recency_score) + \
            (cfg["weight_domain"] * domain_overlap)

    score = round(max(0.0, min(1.0, score)), 4)

    # Check and record edge if score >= threshold
    if score >= cfg["threshold_edge"]:
        record_ota_edge(ota_id_a, ota_id_b, score, db_path=db_path)

    return score

def record_ota_edge(ota_id_a, ota_id_b, resonance_score, db_path=None):
    """Inserts a edge row into ota_edges if not already linked."""
    if not db_path:
        db_path = db.get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().isoformat()
    
    cursor.execute("""
    SELECT id FROM ota_edges
    WHERE (ota_id_a = ? AND ota_id_b = ?) OR (ota_id_a = ? AND ota_id_b = ?)
    """, (ota_id_a, ota_id_b, ota_id_b, ota_id_a))
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO ota_edges (ota_id_a, ota_id_b, resonance_score, created_at)
        VALUES (?, ?, ?, ?)
        """, (ota_id_a, ota_id_b, resonance_score, now_str))
        conn.commit()
        print(f"[Resonance Edge Created] OTA #{ota_id_a} <--> OTA #{ota_id_b} (Score: {resonance_score})")
    conn.close()

def find_resonant_otas(target_text, top_k=3, workspace_root=workspace_root):
    """
    Finds top-K highest resonance OTAs matching target_text for sparring context injection.
    Always includes 1-2 top resonance items regardless of domain, filled with domain matched items.
    """
    db_path = db.get_db_path(workspace_root)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, refined_thesis, created_at FROM otas ORDER BY id DESC")
    all_otas = cursor.fetchall()
    conn.close()

    if not all_otas:
        return []

    target_vec = generate_text_embedding(target_text)
    cfg = load_resonance_config(workspace_root)
    
    scored_otas = []
    for ota_id, title, thesis, created_at in all_otas:
        ota_vec = generate_text_embedding(f"{title} {thesis}")
        sim = cosine_similarity(target_vec, ota_vec)
        
        try:
            dt = datetime.datetime.fromisoformat(created_at)
            days_ago = (datetime.datetime.now() - dt).total_seconds() / 86400.0
        except Exception:
            days_ago = 0.0
            
        recency = math.exp(-(math.log(2.0) / cfg["decay_half_life_days"]) * days_ago)
        score = (cfg["weight_similarity"] * sim) + (cfg["weight_recency"] * recency)
        scored_otas.append({
            "id": ota_id,
            "title": title,
            "thesis": thesis,
            "score": round(score, 4)
        })

    # Sort descending by resonance score
    scored_otas.sort(key=lambda x: x["score"], reverse=True)
    return scored_otas[:top_k]

def get_injected_sparring_context(target_text, top_k=3, workspace_root=workspace_root):
    """
    Retrieves top-K resonant past OTAs formatted for prompt context injection during sparring.
    """
    matches = find_resonant_otas(target_text, top_k=top_k, workspace_root=workspace_root)
    if not matches:
        return []
    
    injected = []
    for m in matches:
        injected.append({
            "ota_id": m["id"],
            "title": m["title"],
            "thesis": m["thesis"],
            "score": m["score"]
        })
    return injected

if __name__ == "__main__":
    cfg = load_resonance_config()
    print("[Resonance Engine] Initialized successfully with config:", cfg)
