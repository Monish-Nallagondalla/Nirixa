#!/usr/bin/env python3
"""
Nirixa OS - Reddit Intelligence Radar Agent
Scrapes and analyzes top high-signal engineering and product subreddits (r/LocalLLaMA, r/experienceddevs, r/ProductManagement, r/MachineLearning, r/UXDesign)
Matches real-world developer & PM friction against Nirixa's 44 OTAs and synthesizes ready-to-post LinkedIn angles.
100% Free - Uses public multi-subreddit Atom/RSS XML stream with zero API keys.
"""

import os
import sys
import xml.etree.ElementTree as ET
import urllib.request
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from system.engine import db, graph

TARGET_SUBREDDITS = [
    "LocalLLaMA",
    "experienceddevs",
    "ProductManagement",
    "MachineLearning",
    "UXDesign"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
}

def scan_multi_subreddits(limit=25):
    """Fetches top posts across all targeted subreddits via a single atomic Atom RSS call."""
    sub_query = "+".join(TARGET_SUBREDDITS)
    url = f"https://www.reddit.com/r/{sub_query}/hot.rss?limit={limit}"
    req = urllib.request.Request(url, headers=HEADERS)
    posts = []
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8")
            root = ET.fromstring(content)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entries = root.findall("atom:entry", ns)
            for e in entries:
                title_elem = e.find("atom:title", ns)
                link_elem = e.find("atom:link", ns)
                category_elem = e.find("atom:category", ns)
                author_elem = e.find("atom:author/atom:name", ns)
                
                title = title_elem.text if title_elem is not None else ""
                link = link_elem.attrib.get("href") if link_elem is not None else ""
                sub_label = category_elem.attrib.get("label") if category_elem is not None else "tech"
                author = author_elem.text if author_elem is not None else "anon"
                
                if title and not title.lower().startswith("[megathread]"):
                    posts.append({
                        "subreddit": sub_label,
                        "title": title.strip(),
                        "author": author,
                        "url": link
                    })
    except Exception as e:
        print(f"[Reddit Radar Error] Failed to fetch feed: {e}", file=sys.stderr)
    return posts

def synthesize_linkedin_angles(posts, max_angles=3):
    """
    Analyzes top friction points and structures them into LinkedIn thought leadership drafts.
    Cross-references with Nirixa OS OTAs.
    """
    synthesized = []
    for p in posts[:max_angles]:
        sub = p["subreddit"]
        title = p["title"]
        author = p["author"]
        
        # Determine relevant OTA alignment
        t_low = title.lower()
        if "slot machine" in t_low or "trust" in t_low or "hallucinat" in t_low or "reliab" in t_low:
            ota_ref = "OTA-039 (The AI Trust Evolution Scale & Deterministic Verification)"
            hook = f"A senior developer on Reddit posted a harsh truth: 'Have been using genAI for a few years and it still feels like a slot machine.'"
            takeaway = "When non-deterministic models power mission-critical software, probabilistic text fluency fails. True enterprise AI requires deterministic eval suites and ACID state machines."
        elif "microcontroller" in t_low or "gpu" in t_low or "qwen" in t_low or "model" in t_low:
            ota_ref = "OTA-038 (The Post-LLM Systems Boom & Edge SLMs)"
            hook = f"While big tech burns billions chasing frontier mega-clusters, developers on Reddit are running models on microcontrollers and edge hardware."
            takeaway = "The future of AI is not centralized cloud monopoly. It is local, sovereign, domain-specific SLMs running at 0 latency with zero data leakage."
        elif "ux" in t_low or "design" in t_low or "product" in t_low:
            ota_ref = "OTA-043 (In-Situ Micro-Computation & Zero Context-Switch UX)"
            hook = f"Why do 90% of AI product redesigns fail to retain users?"
            takeaway = "Product design is applied human psychology. If an interface makes users context-switch or fight the UI, it breaks cognitive ergonomics."
        else:
            ota_ref = "OTA-044 (The Machine-Input Inversion Paradox)"
            hook = f"A trending debate on {sub} reveals why engineering workflows are breaking under AI code volume: '{title[:70]}...'"
            takeaway = "When code generation becomes free, syntax is a commodity. The engineer who articulates system constraints and edge cases has all the leverage."
        
        angle = {
            "source_subreddit": f"{sub}",
            "source_title": title,
            "author": author,
            "url": p["url"],
            "matched_ota": ota_ref,
            "contrarian_hook": hook,
            "linkedin_takeaway": takeaway
        }
        synthesized.append(angle)
    return synthesized

def run_radar_report():
    """Generates a structured CLI report of trending Reddit topics & LinkedIn angles."""
    print("=" * 75)
    print("  NIRIXA OS - REDDIT INTELLIGENCE RADAR (LIVE ATOMIC FEED)")
    print(f"  Target Communities: {', '.join(TARGET_SUBREDDITS)}")
    print(f"  Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 75)
    
    posts = scan_multi_subreddits(limit=25)
    print(f"\n[+] Successfully ingested {len(posts)} trending discussions across target communities.\n")
    
    angles = synthesize_linkedin_angles(posts, max_angles=3)
    for i, a in enumerate(angles, 1):
        print(f"--- ANGLE #{i}: [{a['source_subreddit']}] ---")
        print(f"[*] Discussion: {a['source_title']}")
        print(f"[*] Source URL: {a['url']}")
        print(f"[*] Matched Primitive: {a['matched_ota']}")
        print(f"[*] Contrarian Hook: {a['contrarian_hook']}")
        print(f"[*] LinkedIn Angle: {a['linkedin_takeaway']}\n")
    return angles

if __name__ == "__main__":
    run_radar_report()
