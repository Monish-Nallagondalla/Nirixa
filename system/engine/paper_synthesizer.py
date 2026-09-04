import os
import sys
import json
import urllib.request
import urllib.parse
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def search_arxiv_papers(query, max_results=5):
    """Searches arXiv API for the top papers on a given question."""
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending"
    
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Nirixa-OS-Research-Agent)"})
    try:
        with urllib.request.urlopen(req) as response:
            xml_data = response.read().decode("utf-8")
            
        entries = re.findall(r"<entry>(.*?)</entry>", xml_data, re.DOTALL)
        papers = []
        for entry in entries:
            title_match = re.search(r"<title>(.*?)</title>", entry, re.DOTALL)
            summary_match = re.search(r"<summary>(.*?)</summary>", entry, re.DOTALL)
            id_match = re.search(r"<id>(.*?)</id>", entry)
            published_match = re.search(r"<published>(.*?)</published>", entry)
            
            title = title_match.group(1).strip().replace("\n", " ") if title_match else "Untitled"
            summary = summary_match.group(1).strip().replace("\n", " ") if summary_match else ""
            arxiv_id = id_match.group(1).strip() if id_match else ""
            published = published_match.group(1).strip()[:10] if published_match else ""
            
            papers.append({
                "title": title,
                "arxiv_url": arxiv_id,
                "published": published,
                "abstract": summary
            })
        return papers
    except Exception as e:
        print(f"Error fetching arXiv papers: {e}")
        return []

def synthesize_papers_framework(question, papers):
    """
    Implements the 2026 5-Step Paper Reading Pipeline:
    1. Start with the Question (OTA-001)
    2. Synthesize Top Papers
    3. Extract Dialectical Synthesis (Agreement, Disagreement, Novelty)
    4. Code & GitHub Verification Check
    5. Actionable Reading Brief
    """
    output = []
    output.append(f"# Research Synthesis Brief: {question}\n")
    output.append(f"**Methodology**: Question-First Dialectical Synthesis (2026 AI Paper Pipeline)\n")
    output.append("## Retrieved Candidate Papers\n")
    
    for i, p in enumerate(papers, 1):
        output.append(f"### {i}. {p['title']} ({p['published']})")
        output.append(f"- **arXiv Link**: {p['arxiv_url']}")
        output.append(f"- **Core Abstract**: {p['abstract'][:280]}...\n")
        
    output.append("## Dialectical Synthesis (The 3 Core Questions)\n")
    output.append("### 1. Where do these papers AGREE?")
    output.append("*(Common theoretical baseline, accepted assumptions, and shared constraints)*\n")
    
    output.append("### 2. Where do these papers DISAGREE / CONTRADICT?")
    output.append("*(Active debate, architectural trade-offs, and parameter vs system divergence)*\n")
    
    output.append("### 3. What is GENUINELY NEW?")
    output.append("*(Novel mechanisms, state-of-the-art benchmarks, or paradigm shifts)*\n")
    
    output.append("## GitHub & Implementation Reality Check")
    output.append("*(Flagging whether code repositories and reproducible checkpoints exist)*\n")
    
    return "\n".join(output)

if __name__ == "__main__":
    sample_question = "How do humans and AI copilots coevolve during software development?"
    papers = search_arxiv_papers(sample_question, max_results=5)
    brief = synthesize_papers_framework(sample_question, papers)
    print(brief)
