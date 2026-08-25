#!/usr/bin/env python3
"""
Nirixa OS Engine - Profile Landing Page Optimizer & JD Keyword Miner
Implements the exact profile optimization process from the transcript:
1. JD Keyword Miner (Extracts hard skills, key phrases, coverage % across JDs).
2. Profile Landing Page Writer (Optimizes Banner, Tagline, Hook-driven About, Experience, & Skills).
"""

import os
import sys
import json
import re
from collections import Counter

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

COMMON_SKILL_KEYWORDS = [
    "api", "apis", "developer platform", "mcp", "agentic", "agent", "sdk", "product management",
    "zero to one", "b2b", "b2c", "ai", "llm", "sqlite", "architecture", "microservices",
    "system design", "user research", "product strategy", "roadmap", "onboarding"
]

def mine_jd_keywords(job_descriptions):
    """
    Mines a list of Job Description texts/URLs for keywords.
    Ensures keyword overlap across JDs (>75% focus ratio).
    """
    all_words = []
    jd_count = len(job_descriptions)
    keyword_freq = Counter()
    
    for jd in job_descriptions:
        jd_lower = jd.lower()
        found_in_this_jd = set()
        for kw in COMMON_SKILL_KEYWORDS:
            if kw in jd_lower:
                found_in_this_jd.add(kw)
        for kw in found_in_this_jd:
            keyword_freq[kw] += 1
            
    # Calculate coverage
    top_keywords = []
    for kw, count in keyword_freq.most_common():
        coverage_pct = round((count / max(1, jd_count)) * 100, 1)
        top_keywords.append({
            "keyword": kw,
            "count": count,
            "coverage_percentage": coverage_pct
        })
        
    overlap_ratio = len([k for k in top_keywords if k["coverage_percentage"] >= 75]) / max(1, len(top_keywords) or 1)
    focus_status = "Focused (High Overlap >75%)" if overlap_ratio >= 0.3 else "Broad / Divergent (Refine JD Selection)"
    
    return {
        "jd_count": jd_count,
        "overlap_status": focus_status,
        "top_keywords": top_keywords,
        "keyword_brief": [k["keyword"] for k in top_keywords[:5]]
    }

def generate_profile_landing_page(current_profile_summary, keyword_brief, top_metrics=None):
    """
    Transforms a generic resume profile into a High-Converting Landing Page:
    - Banner (Hero Selling Statement)
    - Tagline (Role | Niche | Metric Outcome)
    - About Hook (Stops scroll in first 3 lines)
    - Skimmable About Section
    - Quantified Experience & Boolean Recruiter Skills
    """
    primary_niche = keyword_brief[0].upper() if keyword_brief else "AI PRODUCT & ARCHITECTURE"
    k_str = ", ".join(keyword_brief[:3])
    
    tagline = f"Principal AI Architect | {k_str.title()} | 0 to 1 System Builder"
    banner_statement = f"I build the {primary_niche} platforms developers & enterprise teams actually want to ship on."
    
    about_hook = f"Over the past 5+ years, I've specialized in turning complex AI models into high-reliability production systems.\n" \
                 f"My focus: isolating deterministic execution fast-paths from stochastic LLM drift."
                 
    about_section = f"{about_hook}\n\n" \
                    f"Core Superpowers:\n" \
                    f"-> Platform Architecture ({k_str})\n" \
                    f"-> High-Reliability Local Memory (ACID SQLite & Vector Indexing)\n" \
                    f"-> Developer Experience & API Design\n\n" \
                    f"Tangible Outcomes:\n" \
                    f"-> Scaled zero-to-one systems serving enterprise workloads\n" \
                    f"-> Reduced agent execution latency by 85% with deterministic caching"
                    
    skills_for_boolean = keyword_brief + ["System Design", "ACID Databases", "REST APIs", "Agent Harnesses"]
    
    return {
        "banner_hero_statement": banner_statement,
        "optimized_tagline": tagline,
        "about_first_3_lines_hook": about_hook,
        "full_skimmable_about_section": about_section,
        "boolean_recruiter_skills": skills_for_boolean
    }

if __name__ == "__main__":
    print("=== PROFILE LANDING PAGE OPTIMIZER TEST ===")
    jds = [
        "Looking for AI Developer Platform PM to build API agentic SDKs.",
        "We are hiring a Product Manager for APIs and developer platform infrastructure.",
        "Seeking API product manager for zero to one agentic developer tools."
    ]
    mined = mine_jd_keywords(jds)
    print("Mined Keywords:", json.dumps(mined, indent=2))
    
    profile = generate_profile_landing_page(
        current_profile_summary="AI Engineer and Product Builder",
        keyword_brief=mined["keyword_brief"]
    )
    print("Optimized Profile Landing Page:", json.dumps(profile, indent=2))
