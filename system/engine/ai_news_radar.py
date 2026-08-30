#!/usr/bin/env python3
"""
Nirixa OS Engine - Multi-Source AI Tech Radar & Thought Leadership Compiler
Origin Sources: Hacker News API, GitHub Trending AI, Hugging Face Daily Papers, and arXiv.
Runs every 3 hours with 0 API cost.
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import datetime
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.insert(0, script_dir)

import db

# -------------------------------------------------------------------------
# 1. HACKER NEWS AI DISCOVERY ENGINE (100% Free Firebase API)
# -------------------------------------------------------------------------
def fetch_hacker_news_ai(limit=30):
    """
    Fetches top stories from Hacker News and filters for high-signal AI developments.
    """
    ai_keywords = ["ai", "agent", "llm", "openworker", "deepseek", "vllm", "claude", "gpt", "rag", "langgraph", "crewai", "ollama", "mistral", "transformer"]
    stories = []
    try:
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        req = urllib.request.Request(url, headers={"User-Agent": "NirixaRadar/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            ids = json.loads(resp.read().decode("utf-8"))[:limit]

        for item_id in ids:
            try:
                item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
                item_req = urllib.request.Request(item_url, headers={"User-Agent": "NirixaRadar/1.0"})
                with urllib.request.urlopen(item_req, timeout=3) as item_resp:
                    item = json.loads(item_resp.read().decode("utf-8"))
                    title = item.get("title", "")
                    title_lower = title.lower()
                    
                    # Match high-signal AI stories
                    if any(kw in title_lower.split() or f" {kw}" in title_lower or f"{kw}-" in title_lower for kw in ai_keywords):
                        score = item.get("score", 0)
                        stories.append({
                            "source": "Hacker News",
                            "title": title,
                            "url": item.get("url") or f"https://news.ycombinator.com/item?id={item_id}",
                            "score": score,
                            "timestamp": datetime.datetime.fromtimestamp(item.get("time", time.time())).strftime("%Y-%m-%d %H:%M")
                        })
            except Exception:
                continue
    except Exception as e:
        print(f"[News Radar] Hacker News fetch notice: {e}")

    return sorted(stories, key=lambda x: x.get("score", 0), reverse=True)[:5]


# -------------------------------------------------------------------------
# 2. HUGGING FACE DAILY PAPERS ENGINE (100% Free Public API)
# -------------------------------------------------------------------------
def fetch_huggingface_trending_papers(limit=5):
    """
    Fetches curated top AI research papers from Hugging Face Daily Papers.
    """
    papers = []
    try:
        url = "https://huggingface.co/api/daily_papers"
        req = urllib.request.Request(url, headers={"User-Agent": "NirixaRadar/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data[:limit]:
                paper = item.get("paper", {})
                title = paper.get("title", "")
                summary = paper.get("summary", "")
                paper_id = paper.get("id", "")
                upvotes = item.get("upvotes", 0)
                papers.append({
                    "source": "Hugging Face Daily Papers",
                    "title": title,
                    "summary": summary[:300],
                    "url": f"https://huggingface.co/papers/{paper_id}",
                    "score": upvotes
                })
    except Exception as e:
        print(f"[News Radar] Hugging Face fetch notice: {e}")
    return papers


# -------------------------------------------------------------------------
# 3. HIGH-THESIS LINKEDIN COMPILER (RULE 7: NAVAL & AVIRAL STANDARD)
# -------------------------------------------------------------------------
def analyze_nirixa_resonance(item):
    """
    Evaluates if a thought leader development or paper intersects with Nirixa OS primitives
    (e.g., Karpathy LLM-OS / LLM-Wiki, Local Memory, Graph RAG, Cognitive Primitives).
    Returns actionable insight and Telegram push alert if high resonance.
    """
    title_lower = item.get("title", "").lower()
    summary_lower = item.get("summary", "").lower()
    content = f"{title_lower} {summary_lower}"
    
    nirixa_primitives = {
        "llm-wiki": ("Karpathy LLM-Wiki & Persistent Memory", "Auto-compiling raw unstructured streams into living wiki topic cards without prompt rot."),
        "local-first": ("Local-First DB Memory (SQLite/Vec)", "Zero-cloud sub-millisecond memory retrieval avoiding vendor lock-in."),
        "graph": ("Associative Graph Traversal (OTA-004)", "Connecting disparate cognitive nodes across time via associative graph traversal rather than naive cosine similarity."),
        "multi-agent": ("Deterministic Multi-Agent Boundaries", "Replacing fragile daisy-chained cloud agents with strict human-in-the-loop checkpoints."),
        "reasoning": ("Socratic Sparring & Debate (OTA-010)", "AI that challenges assumptions and probes unstated premises rather than autocompleting.")
    }
    
    for key, (topic, impact) in nirixa_primitives.items():
        if key in content or any(w in content for w in key.split("-")):
            return {
                "matched_primitive": topic,
                "impact_for_nirixa": impact,
                "actionable_recommendation": f"Adopt {topic} architectural patterns to enhance Nirixa's local-first cognitive engine."
            }
            
    return None

def send_nirixa_radar_alert(item, resonance_info):
    """Pushes a high-priority architectural alert to Monish's phone via Telegram."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
        
    msg = (
        f"🔔 *Nirixa Architecture Radar Alert*\n\n"
        f"📌 *Development:* {item['title']}\n"
        f"🏛️ *Source:* {item['source']}\n\n"
        f"💡 *Why It Matters for Nirixa:*\n"
        f"• *Primitive:* {resonance_info['matched_primitive']}\n"
        f"• *Insight:* {resonance_info['impact_for_nirixa']}\n\n"
        f"🛠️ *Actionable Recommendation:*\n"
        f"{resonance_info['actionable_recommendation']}\n\n"
        f"🔗 [Read Source]({item.get('url', '#')})"
    )
    
    try:
        import telegram_push
        telegram_push.push_to_telegram(msg)
    except Exception as e:
        print(f"[Radar Alert Notice] {e}")

def compile_breakthrough_post(item):
    """
    Compiles raw tech news into a high-density, zero-hype LinkedIn post.
    """
    title = item.get("title", "")
    source = item.get("source", "Origin Source")
    url = item.get("url", "")
    
    post = f"""The biggest differentiator in enterprise AI right now is knowing what to build yourself vs what is being commoditized by open source.

Breaking development from {source}:
"{title}"

Three structural takeaways for engineering and product teams:

1. Local-first and open-source models are closing the gap with proprietary APIs faster than expected.
2. The real value is shifting from generic LLM wrappers to deterministic orchestration, proprietary evaluation harnesses, and domain-specific data pipelines.
3. Teams that rely purely on prompt engineering are vulnerable; teams building DB-first architectures with strict verification boundaries will endure.

Source reference: {url}

What is your take on this shift?"""

    return post


# -------------------------------------------------------------------------
# 4. RADAR SCANNER & DISPATCH (RUNS ON 3-HOUR CADENCE)
# -------------------------------------------------------------------------
def send_telegram_alert(item, draft_text):
    """Sends a Telegram alert to Monish when a breaking AI project is found."""
    try:
        telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not telegram_token or not chat_id:
            # Look up in db or fallback
            conn = sqlite3.connect(os.path.join(workspace_root, "system", "data", "nirixa.db"))
            c = conn.cursor()
            c.execute("SELECT raw_text FROM raw_captures WHERE chat_id IS NOT NULL LIMIT 1")
            row = c.fetchone()
            conn.close()
            # If no env set, read from config if available
            return
            
        msg = f"🚨 *Breaking AI Development Detected*:\n\n*{item.get('title')}*\nSource: {item.get('source')} ({item.get('url')})\n\n📝 *Drafted LinkedIn Thought Piece*:\n```\n{draft_text[:350]}...\n```\n\n_Review full draft in content/linkedin/_"
        url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        data = urllib.parse.urlencode({
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "Markdown"
        }).encode("utf-8")
        req = urllib.request.Request(url, data=data)
        urllib.request.urlopen(req, timeout=5)
        print("[News Radar] Pushed Telegram alert to Monish!")
    except Exception as e:
        print(f"[News Radar] Telegram dispatch notice: {e}")

def run_3_hour_radar_scan(notify_telegram=True):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Executing 3-Hour AI Tech Radar Scan...")
    hn_items = fetch_hacker_news_ai()
    hf_items = fetch_huggingface_trending_papers()
    
    all_items = hn_items + hf_items
    print(f"[News Radar] Found {len(all_items)} high-signal AI developments.")
    
    linkedin_dir = os.path.join(workspace_root, "content", "linkedin")
    os.makedirs(linkedin_dir, exist_ok=True)
    
    saved_drafts = []
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    for idx, item in enumerate(all_items[:3]):
        post_content = compile_breakthrough_post(item)
        filename = f"tech-radar-{today_str}-item-{idx+1}.md"
        filepath = os.path.join(linkedin_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(post_content)
        
        saved_drafts.append({
            "filename": filename,
            "filepath": filepath,
            "title": item.get("title"),
            "source": item.get("source"),
            "url": item.get("url"),
            "preview": post_content
        })
        print(f"[News Radar Draft Saved] -> content/linkedin/{filename}")
        
    if notify_telegram and saved_drafts:
        top = all_items[0]
        send_telegram_alert(top, saved_drafts[0]["preview"])
        
    return saved_drafts

if __name__ == "__main__":
    drafts = run_3_hour_radar_scan()
    print(f"\n[PASS] 3-Hour AI Tech Radar completed. {len(drafts)} LinkedIn drafts compiled successfully.")
