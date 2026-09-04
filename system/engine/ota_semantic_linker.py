import sqlite3
import json
import os
import datetime
import re

# 1. Definitive 10-Verb Epistemic Weight Calibration
VERB_BASE_WEIGHTS = {
    "DEPENDS_ON": {"epistemic": 0.95, "desc": "Hard prerequisite: Target concept is fundamentally required to validate source"},
    "DERIVES_FROM": {"epistemic": 0.90, "desc": "Direct mathematical or first-principles derivation"},
    "EXTENDS": {"epistemic": 0.82, "desc": "Expands the conceptual boundary or operational scope"},
    "SUPPORTS": {"epistemic": 0.78, "desc": "Empirical or theoretical corroboration"},
    "APPLIES_TO": {"epistemic": 0.75, "desc": "Direct operationalization in software architecture or product UX"},
    "REFINES": {"epistemic": 0.72, "desc": "Increases analytical sharpness or removes ambiguity"},
    "QUESTIONS": {"epistemic": 0.68, "desc": "Probes unstated premises or exposes edge-case failure modes"},
    "CONTRADICTS": {"epistemic": 0.65, "desc": "Active dialectical tension challenging the opposing thesis"},
    "ANALOGOUS_TO": {"epistemic": 0.58, "desc": "Structural isomorphism across biological and synthetic substrates"},
    "INSPIRED_BY": {"epistemic": 0.52, "desc": "Cross-domain heuristic transference"}
}

# 2. Empirical Systems Grounding Registry
EMPIRICAL_GROUNDED_NODES = {
    "ota_043": 1.0,  # In-situ micro-calculator and zero-context-switch UX
    "ota_044": 0.95, # Machine-input inversion & cognitive ergonomics
    "ota_046": 0.95, # Dual-memory head vs world context engineering
    "ota_048": 0.90, # Sensorimotor tactile grounding & physical AI
    "ota_007": 0.95, # Asymmetric low-friction stream capture
    "ota_012": 0.95, # Multi-channel ephemeral buffer architecture
    "ota_019": 0.92, # Ephemeral-to-permanent 3-stage distillation pipeline
    "ota_004": 0.95, # SQLite ACID single source of truth
    "ota_003": 0.92, # Deterministic fast path
    "ota_009": 0.90, # FTS5 deterministic semantic anchoring
    "ota_027": 0.95, # Automated continuous health eval suite
    "ota_028": 0.90, # Proactive asynchronous task delegation
    "ota_040": 0.92, # Desktop agent vs Cognitive OS
    "ota_021": 0.95, # Asymmetric knowledge compounding flywheel
    "ota_016": 0.95  # Decadal compounding horizon
}

def tokenize(text):
    return set(re.findall(r'\b[a-zA-Z]{3,}\b', text.lower()))

def calculate_jaccard_similarity(text1, text2):
    tokens1 = tokenize(text1)
    tokens2 = tokenize(text2)
    if not tokens1 or not tokens2:
        return 0.5
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return round(len(intersection) / len(union), 3)

def link_all_otas_with_rigorous_scoring(db_path=None):
    if not db_path:
        db_path = os.path.join("system", "data", "nirixa.db")
        
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}, skipping edge persistence.")
        return
        
    conn = sqlite3.connect(db_path, timeout=30.0)
    cursor = conn.cursor()
    
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("SELECT node_key, label, properties_json FROM graph_nodes")
    nodes_map = {}
    for n_key, label, props_json in cursor.fetchall():
        props = json.loads(props_json) if props_json else {}
        nodes_map[n_key] = {
            "label": label,
            "description": props.get("description", label)
        }
        
    cursor.execute("SELECT source_key, target_key FROM graph_edges WHERE relation_type = 'GROUNDS_PILLAR'")
    pillar_map = {tgt: src for src, tgt in cursor.fetchall()}
    
    raw_edges = [
        ("ota_046", "ota_044", "EXTENDS", "Context Engineering extends Don Norman's head vs world duality into AI architecture, solving the Machine-Input Inversion."),
        ("ota_046", "ota_047", "SUPPORTS", "Knowledge in the World context engineering supports why parametric weight scaling alone hits reasoning limits."),
        ("ota_044", "ota_045", "DEPENDS_ON", "Human-Agent symbiotic coevolution depends on eliminating low-level mechanical syntax friction first."),
        ("ota_045", "ota_040", "DERIVES_FROM", "Coevolutionary intelligence derives from an associative Cognitive OS foundation rather than transient scripts."),
        ("ota_048", "ota_047", "ANALOGOUS_TO", "High-frequency haptic mechanoreception is analogous to multimodal sensorimotor token streams."),
        ("ota_043", "ota_044", "APPLIES_TO", "In-situ micro-computation applies the machine-input inversion fix directly to transaction friction."),
        ("ota_043", "ota_036", "APPLIES_TO", "In-situ micro-computation applies the human-centric design invariant by collapsing intent-to-action friction."),
        ("ota_001", "ota_031", "REFINES", "Socratic query primacy refines how the question-driven system engine traverses living thoughts."),
        ("ota_001", "ota_010", "QUESTIONS", "Socratic queries actively question and probe unstated premises during adversarial sparring."),
        ("ota_011", "ota_039", "SUPPORTS", "Thought ancestry supports verifiable trust by preserving complete epistemic lineage across time."),
        ("ota_035", "ota_044", "INSPIRED_BY", "Agent interface abstraction is inspired by Don Norman's 3 cognitive processing layers (Visceral, Behavioral, Reflective)."),
        ("ota_033", "ota_047", "ANALOGOUS_TO", "Subconscious associative topology in human memory is analogous to non-parametric GraphRAG retrieval."),
        ("ota_034", "ota_047", "INSPIRED_BY", "Dynamic attention weighting is inspired by biological biochemical hormonal flooding (amygdala valency)."),
        ("ota_042", "ota_037", "REFINES", "Human taste acts as the critical selection pressure refining machine-generated narrative models."),
        ("ota_007", "ota_012", "SUPPORTS", "Mobile capture asymmetry supports zero-friction logging via multi-channel ephemeral buffers."),
        ("ota_012", "ota_019", "EXTENDS", "The ephemeral mobile buffer extends directly into the permanent 3-stage distillation pipeline."),
        ("ota_019", "ota_004", "DEPENDS_ON", "The 3-stage distillation pipeline depends on SQLite ACID single-source-of-truth persistence."),
        ("ota_003", "ota_002", "DERIVES_FROM", "Deterministic fast paths derive from the zero-cost resilience fallback hierarchy."),
        ("ota_009", "ota_004", "SUPPORTS", "Deterministic semantic anchoring supports ACID invariants by preventing vector drift."),
        ("ota_013", "ota_046", "REFINES", "The 3-tier layered memory hierarchy refines the technical implementation of Knowledge in the World."),
        ("ota_017", "ota_010", "REFINES", "Multi-turn Socratic loops refine the multi-perspective debate mechanism."),
        ("ota_020", "ota_044", "REFINES", "The cognitive load equalizer refines the mechanical offloading layer to preserve human creative taste."),
        ("ota_021", "ota_016", "EXTENDS", "The asymmetric knowledge flywheel extends daily captures toward long-term compounding horizons."),
        ("ota_023", "ota_025", "APPLIES_TO", "High-dwell architectural frameworks apply directly to thought leadership positioning."),
        ("ota_027", "ota_004", "SUPPORTS", "Continuous health eval suites support database integrity through automated verification checks."),
        ("ota_028", "ota_012", "APPLIES_TO", "Proactive task delegation applies micro-task prompts directly to mobile endpoints."),
        ("ota_029", "ota_040", "APPLIES_TO", "Executable markdown skills apply directly inside the Cognitive OS harness."),
        ("ota_038", "ota_047", "CONTRADICTS", "The systems engineering boom thesis contradicts the assumption that reasoning improves solely by scaling parameters."),
        ("ota_039", "ota_003", "DEPENDS_ON", "AI Trust scales only when backed by deterministic fast-path verifiers.")
    ]
    
    total_edges = 0
    for src, tgt, verb, reason in raw_edges:
        src_info = nodes_map.get(src, {"label": src, "description": ""})
        tgt_info = nodes_map.get(tgt, {"label": tgt, "description": ""})
        
        jaccard = calculate_jaccard_similarity(src_info["label"] + " " + src_info["description"], 
                                               tgt_info["label"] + " " + tgt_info["description"])
        sem_score = round(min(0.98, max(0.65, 0.60 + (jaccard * 1.5))), 3)
        epist_score = VERB_BASE_WEIGHTS.get(verb, {}).get("epistemic", 0.75)
        
        src_pillar = pillar_map.get(src, "pillar_p1")
        tgt_pillar = pillar_map.get(tgt, "pillar_p2")
        bridge_score = 0.95 if src_pillar != tgt_pillar else 0.65
        
        src_emp = EMPIRICAL_GROUNDED_NODES.get(src, 0.60)
        tgt_emp = EMPIRICAL_GROUNDED_NODES.get(tgt, 0.60)
        scar_score = round((src_emp + tgt_emp) / 2.0, 3)
        
        composite = round((0.30 * epist_score) + (0.30 * sem_score) + (0.25 * bridge_score) + (0.15 * scar_score), 3)
        
        props = {
            "reason": reason,
            "verb": verb,
            "score": composite,
            "attributes": {
                "semantic_similarity": sem_score,
                "epistemic_dependency": epist_score,
                "cross_pillar_bridge": bridge_score,
                "empirical_resonance": scar_score,
                "composite_score": composite
            }
        }
        
        cursor.execute("""
        INSERT OR REPLACE INTO graph_edges (source_key, target_key, relation_type, weight, properties_json, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (src, tgt, verb, composite, json.dumps(props), now_str))
        total_edges += 1
        
    conn.commit()
    conn.close()
    print(f"Computed rigorous multi-attribute scoring across {total_edges} graph edges in open source repository!")

if __name__ == "__main__":
    link_all_otas_with_rigorous_scoring()
