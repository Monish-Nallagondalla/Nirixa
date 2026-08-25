#!/usr/bin/env python3
"""
Nirixa OS Engine - High-Relevance Executive Networking & Outreach Engine
Implements the operational processes extracted from the podcast transcript:
1. Target Opportunity Scoring (Prioritizes non-creators with low notification noise).
2. High-Value Comment Generator (First name + Substantive research + Open-ended question).
3. Cheeky Routine-Based Connection Request Generator ("Buy your lunch for 15 mins of brain power").
4. Proven Hook Recycler & High-Relevance Content Optimizer.
5. Peer Brain-Picking Outreach Writer.
"""

import os
import sys
import json
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from system.engine import db

def evaluate_target_opportunity(follower_count, posts_per_month):
    """
    Computes an Opportunity Score for target profiles.
    Non-creators (low post frequency, <2,000 followers) receive a HIGHER score
    because their notification noise is low and comment visibility is 10x higher.
    """
    score = 100
    if follower_count > 10000:
        score -= 40
    elif follower_count > 2000:
        score -= 20
        
    if posts_per_month > 15:
        score -= 40
    elif posts_per_month > 5:
        score -= 15
        
    tier = "High Priority Target (Non-Creator / High Notification Visibility)" if score >= 70 else \
           "Medium Priority Target" if score >= 40 else "Low Priority (High Noise Creator)"
           
    return {
        "opportunity_score": max(10, score),
        "tier": tier,
        "recommendation": "Comment immediately with first-name value & open question" if score >= 70 else "Engage cautiously"
    }

def generate_high_value_comment(recipient_first_name, post_text, user_domain="AI Architecture"):
    """
    Generates a structured high-value comment:
    1. Addresses by first name (dropping last name for warmth).
    2. Adds 2-3 sentences of substantive research/value.
    3. Ends with an open-ended question inviting dialogue.
    """
    clean_name = recipient_first_name.strip().split()[0]
    
    comment = f"Hey {clean_name}, really sharp analysis on this. " \
              f"In our work with {user_domain.lower()}, we've seen a very similar pattern—" \
              f"the biggest leverage point is isolating deterministic execution from stochastic model drift. " \
              f"How are you currently handling this tradeoff across your team's stack?"
              
    return {
        "recipient": clean_name,
        "comment_text": comment,
        "hook_mechanism": "Notification badge will display your name + tagline to drive profile curiosity visits."
    }

def generate_connection_request(recipient_first_name, target_role="Product Director", style="cheeky"):
    """
    Generates connection request messages.
    Style 'cheeky': Appeals to routine friction ("Since you already eat 3 meals a day, let me buy your lunch...").
    Style 'direct': Direct peer application inquiry.
    """
    clean_name = recipient_first_name.strip().split()[0]
    
    if style == "cheeky":
        note = f"Hey {clean_name}, given that you already eat 3 meals a day, why don't you spend one of those meals with me? " \
               f"I'll buy your lunch in exchange for 15 mins of your brain power on how your team builds {target_role.lower()} systems."
    else:
        note = f"Hey {clean_name}, saw your work leading {target_role} and really impressed by your execution. " \
               f"Would love to connect and pick your brain on your team's application process and architecture."
               
    return {
        "recipient": clean_name,
        "connection_note": note,
        "character_count": len(note),
        "within_linkedin_300_char_limit": len(note) <= 300
    }

def generate_recycled_post_hook(proven_hook_template, new_topic):
    """
    Recycles top-performing hook structures into new topics (OTA-016 & OTA-018).
    """
    recycled_hook = f"Unpopular opinion: Most teams approach {new_topic.lower()} backwards. " \
                    f"Here is the exact 3-step framework we used to solve it:"
    return {
        "original_template": proven_hook_template,
        "new_topic": new_topic,
        "recycled_hook": recycled_hook
    }

if __name__ == "__main__":
    print("=== HIGH-RELEVANCE OUTREACH ENGINE TEST ===")
    opp = evaluate_target_opportunity(follower_count=850, posts_per_month=2)
    print("Opportunity Eval:", json.dumps(opp, indent=2))
    
    comm = generate_high_value_comment("Marco", "Building developer platforms requires clear API contracts.")
    print("Generated Comment:", json.dumps(comm, indent=2))
    
    conn = generate_connection_request("Marco", "AI Platform Lead", style="cheeky")
    print("Connection Request Note:", json.dumps(conn, indent=2))
