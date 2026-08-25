#!/usr/bin/env python3
"""
Nirixa OS System Script - Auto-Compile Multi-Slide PDF for LinkedIn (Rule 6 Compliance)
Generates high-signal, dark-mode 1080x1350 multi-slide PDF document for LinkedIn carousels.
"""

import os
import hashlib

# Patch hashlib.md5 for OpenSSL compatibility in reportlab
_orig_md5 = hashlib.md5
def _patched_md5(*args, **kwargs):
    kwargs.pop("usedforsecurity", None)
    return _orig_md5(*args, **kwargs)
hashlib.md5 = _patched_md5

from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors


PAGE_WIDTH = 540  # 1:1 or 4:5 aspect ratio layout points
PAGE_HEIGHT = 675

def draw_slide(c, title, bullets, slide_num, total_slides):
    # Background
    c.setFillColor(colors.HexColor("#0D1117"))
    c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=True, stroke=False)
    
    # Top Accent Line
    c.setFillColor(colors.HexColor("#38BDF8"))
    c.rect(0, PAGE_HEIGHT - 6, PAGE_WIDTH, 6, fill=True, stroke=False)
    
    # Header Tag
    c.setFillColor(colors.HexColor("#38BDF8"))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(36, PAGE_HEIGHT - 40, "NIRIXA OS // RESEARCH INSIGHT")
    
    # Title
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.setFont("Helvetica-Bold", 18)
    
    # Wrap title if long
    words = title.split(" ")
    line1, line2 = "", ""
    for w in words:
        if len(line1 + " " + w) < 32:
            line1 += (" " if line1 else "") + w
        else:
            line2 += (" " if line2 else "") + w
            
    c.drawString(36, PAGE_HEIGHT - 80, line1)
    if line2:
        c.drawString(36, PAGE_HEIGHT - 105, line2)
        
    y_start = PAGE_HEIGHT - 150 if line2 else PAGE_HEIGHT - 125
    
    # Divider Line
    c.setStrokeColor(colors.HexColor("#1E293B"))
    c.setLineWidth(1)
    c.line(36, y_start, PAGE_WIDTH - 36, y_start)
    
    y = y_start - 35
    
    # Bullet points
    c.setFont("Helvetica", 11)
    for b in bullets:
        c.setFillColor(colors.HexColor("#38BDF8"))
        c.drawString(36, y, "->")
        
        c.setFillColor(colors.HexColor("#94A3B8"))
        # Draw wrapped text
        b_words = b.split(" ")
        b_line1, b_line2 = "", ""
        for bw in b_words:
            if len(b_line1 + " " + bw) < 52:
                b_line1 += (" " if b_line1 else "") + bw
            else:
                b_line2 += (" " if b_line2 else "") + bw
                
        c.drawString(56, y, b_line1)
        if b_line2:
            y -= 18
            c.drawString(56, y, b_line2)
            
        y -= 28
        
    # Footer Slide Number
    c.setFillColor(colors.HexColor("#64748B"))
    c.setFont("Helvetica", 9)
    c.drawString(36, 25, "Monish Nallagondalla // Founder & Principal Architect")
    c.drawRightString(PAGE_WIDTH - 36, 25, f"Slide {slide_num} of {total_slides}")
    
    c.showPage()

def build_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    c = canvas.Canvas(output_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    
    slides = [
        (
            "The Empathy Asymmetry: Why AI Cannot Feel",
            [
                "Multimodal LLMs analyze pixels and tokens but do not feel.",
                "Text prediction is merely a lossy 1D projection of human thought.",
                "True biological emotion requires continuous physical stakes.",
                "Here is why AI struggles with empathy and how to design high-trust systems."
            ]
        ),
        (
            "1. Visceral Empathy vs Pattern Matching",
            [
                "Models predict the statistical next token associated with empathy.",
                "Human empathy requires shared lived experience and moral risk.",
                "Without skin in the game, an AI outputting empathy is pattern lookup."
            ]
        ),
        (
            "2. Long-Term Relational Trust",
            [
                "Trust is built over time through predictable execution under friction.",
                "Models operate in discrete single-turn context windows.",
                "They evaluate tokens, not consequences or long-term stakes."
            ]
        ),
        (
            "3. High-Empathy Enterprise Architecture",
            [
                "Crisis Triage: AI flags risk patterns while humans deliver empathy.",
                "Customer Retention: AI synthesizes context; senior leads build trust.",
                "Coaching & Mentorship: AI audits tone; human leads guide strategy."
            ]
        ),
        (
            "The Empathetic Co-Pilot Framework",
            [
                "Rule: Never replace human empathy with automated chatbots.",
                "Pattern: Offload cognitive load to AI; preserve empathy for humans.",
                "Outcome: High-trust enterprise scaling with zero brand degradation."
            ]
        )
    ]
    
    total = len(slides)
    for idx, (title, bullets) in enumerate(slides, 1):
        draw_slide(c, title, bullets, idx, total)
        
    c.save()
    print(f"Successfully compiled LinkedIn PDF carousel: {output_path}")

if __name__ == "__main__":
    out_pdf = os.path.abspath(os.path.join("docs", "content", "posts", "ai-vs-human-empathy-slides.pdf"))
    build_pdf(out_pdf)
