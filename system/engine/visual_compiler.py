#!/usr/bin/env python3
"""
Nirixa OS Engine - High-Signal Visual Slide & Document Compiler
Generates stunning, minimalist, high-contrast dark-mode multi-page PDF slides for LinkedIn Document Uploads.
Enforces:
- Dark sleek aesthetic (#0b0f19 background, #38bdf8 accents, Inter-style typography)
- High contrast, zero fluff, razor-sharp architectural schematics
- 1080x1350 vertical aspect ratio (perfect for mobile & desktop LinkedIn carousels)
"""

import os
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patches as patches

def create_slide_1_cover():
    fig, ax = plt.subplots(figsize=(8, 10), facecolor='#0b0f19')
    ax.set_facecolor('#0b0f19')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    # Accent Top Pill
    pill = patches.FancyBboxPatch((0.8, 10.4), 3.2, 0.6, boxstyle="round,pad=0.1",
                                  facecolor='#1e293b', edgecolor='#38bdf8', linewidth=1.5)
    ax.add_patch(pill)
    ax.text(2.4, 10.7, "PERSONAL AGI MANIFESTO", color='#38bdf8', fontsize=11,
            fontweight='bold', ha='center', va='center')

    # Main Title
    ax.text(0.8, 9.2, "Spinoza's Lens\n& Personal AGI", color='#f8fafc',
            fontsize=26, fontweight='bold', ha='left', va='top', linespacing=1.2)

    # Subtitle Hook
    ax.text(0.8, 7.4, "Why the tech world is looking for AGI\nin all the wrong places—and why you must\nown your cognition.",
            color='#94a3b8', fontsize=14, ha='left', va='top', linespacing=1.4)

    # Story Anchor Box
    story_box = patches.FancyBboxPatch((0.8, 3.2), 8.4, 3.4, boxstyle="round,pad=0.2",
                                       facecolor='#111827', edgecolor='#334155', linewidth=1)
    ax.add_patch(story_box)

    ax.text(1.2, 6.2, "IN 1656, SPINOZA WAS OFFERED 1,000 GUILDERS", color='#f59e0b',
            fontsize=11, fontweight='bold', ha='left')
    ax.text(1.2, 5.6, "• They asked him to stop building, keep quiet, and conform.\n• He refused. By day he ground optical lenses.\n• By night, locked in a desk drawer, he wrote the Ethics.",
            color='#cbd5e1', fontsize=12, ha='left', va='top', linespacing=1.5)
    ax.text(1.2, 3.8, "400 years later: Corporate AI offers us the exact same trap.",
            color='#38bdf8', fontsize=12, fontweight='bold', ha='left')

    # Footer
    ax.text(0.8, 1.0, "NIRIXA OS ARCHITECTURE SERIES", color='#64748b', fontsize=10, fontweight='bold')
    ax.text(9.2, 1.0, "SLIDE 01 / 04 →", color='#38bdf8', fontsize=10, fontweight='bold', ha='right')

    return fig

def create_slide_2_comparison():
    fig, ax = plt.subplots(figsize=(8, 10), facecolor='#0b0f19')
    ax.set_facecolor('#0b0f19')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    ax.text(0.8, 10.8, "THE TWO FUTURES OF AGI", color='#38bdf8', fontsize=11, fontweight='bold')
    ax.text(0.8, 10.0, "Corporate AGI vs Personal AGI", color='#f8fafc', fontsize=22, fontweight='bold')

    # Box 1: Corporate AGI (Red/Gray border)
    box1 = patches.FancyBboxPatch((0.8, 5.8), 8.4, 3.6, boxstyle="round,pad=0.2",
                                  facecolor='#181216', edgecolor='#f87171', linewidth=1.5)
    ax.add_patch(box1)
    ax.text(1.2, 8.9, "1. THE RENTED CORPORATE ASSISTANT ($20/MO)", color='#f87171', fontsize=12, fontweight='bold')
    ax.text(1.2, 8.2, "• Resets context every time you close the browser tab.\n• Gets vendor lobotomies without your consent.\n• Your judgment & scars compound in someone else's cloud.\n• High platform dependency & lock-in risk.",
            color='#cbd5e1', fontsize=11.5, ha='left', va='top', linespacing=1.5)

    # Box 2: Personal AGI (Blue/Green border)
    box2 = patches.FancyBboxPatch((0.8, 1.6), 8.4, 3.8, boxstyle="round,pad=0.2",
                                  facecolor='#0f172a', edgecolor='#38bdf8', linewidth=1.5)
    ax.add_patch(box2)
    ax.text(1.2, 4.9, "2. THE SOVEREIGN OPERATING SYSTEM (NIRIXA)", color='#38bdf8', fontsize=12, fontweight='bold')
    ax.text(1.2, 4.2, "• Runs locally on your laptop with SQLite & Markdown memory.\n• Owns 25 years of your life, career, and research context.\n• Executes skills you wrote. Zero vendor lock-in.\n• Model reasoning is rented; context is 100% owned.",
            color='#cbd5e1', fontsize=11.5, ha='left', va='top', linespacing=1.5)

    ax.text(0.8, 0.8, "NIRIXA OS • LOCAL-FIRST SOVEREIGNTY", color='#64748b', fontsize=10)
    ax.text(9.2, 0.8, "SLIDE 02 / 04 →", color='#38bdf8', fontsize=10, fontweight='bold', ha='right')

    return fig

def create_slide_3_cognitive_physics():
    fig, ax = plt.subplots(figsize=(8, 10), facecolor='#0b0f19')
    ax.set_facecolor('#0b0f19')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    ax.text(0.8, 10.8, "COGNITIVE PHYSICS", color='#38bdf8', fontsize=11, fontweight='bold')
    ax.text(0.8, 10.0, "7 Items vs The 1M Token Library", color='#f8fafc', fontsize=22, fontweight='bold')

    # Working Memory Card
    card1 = patches.FancyBboxPatch((0.8, 6.6), 8.4, 2.6, boxstyle="round,pad=0.2",
                                   facecolor='#111827', edgecolor='#64748b', linewidth=1)
    ax.add_patch(card1)
    ax.text(1.2, 8.7, "HUMAN BIOLOGICAL WORKING MEMORY: 7 ± 2 ITEMS", color='#fbbf24', fontsize=12, fontweight='bold')
    ax.text(1.2, 8.0, "Every meeting, standup, and org chart in human history\nwas a prosthetic for this 7-item biological bottleneck.",
            color='#94a3b8', fontsize=11.5, ha='left', va='top', linespacing=1.4)

    # 1M Token Agent Card
    card2 = patches.FancyBboxPatch((0.8, 3.4), 8.4, 2.8, boxstyle="round,pad=0.2",
                                   facecolor='#111827', edgecolor='#818cf8', linewidth=1)
    ax.add_patch(card2)
    ax.text(1.2, 5.7, "THE 1,000,000 TOKEN CONTEXT AGENT", color='#818cf8', fontsize=12, fontweight='bold')
    ax.text(1.2, 5.0, "Your career is not 3 open books—it is a 25-year library.\nThe critical question: Who decides which 3 books\nare open on the desk at any given second?",
            color='#cbd5e1', fontsize=11.5, ha='left', va='top', linespacing=1.4)

    # The Invariant Callout
    inv_box = patches.FancyBboxPatch((0.8, 1.4), 8.4, 1.6, boxstyle="round,pad=0.15",
                                     facecolor='#1e1b4b', edgecolor='#a855f7', linewidth=1.5)
    ax.add_patch(inv_box)
    ax.text(5.0, 2.2, "\"Own your skill files. If you don't,\nyour job becomes a skill file.\"",
            color='#f3e8ff', fontsize=13, fontweight='bold', ha='center', va='center', style='italic')

    ax.text(0.8, 0.8, "NIRIXA OS • COGNITIVE ARCHITECTURE", color='#64748b', fontsize=10)
    ax.text(9.2, 0.8, "SLIDE 03 / 04 →", color='#38bdf8', fontsize=10, fontweight='bold', ha='right')

    return fig

def create_slide_4_cta():
    fig, ax = plt.subplots(figsize=(8, 10), facecolor='#0b0f19')
    ax.set_facecolor('#0b0f19')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis('off')

    ax.text(0.8, 10.8, "THE OPEN SOURCE MOVEMENT", color='#38bdf8', fontsize=11, fontweight='bold')
    ax.text(0.8, 10.0, "Take Custody of Your Cognition", color='#f8fafc', fontsize=22, fontweight='bold')

    # Center Hero Box
    hero = patches.FancyBboxPatch((0.8, 3.8), 8.4, 5.4, boxstyle="round,pad=0.2",
                                  facecolor='#0f172a', edgecolor='#38bdf8', linewidth=2)
    ax.add_patch(hero)

    ax.text(5.0, 8.4, "NIRIXA OS", color='#38bdf8', fontsize=24, fontweight='bold', ha='center')
    ax.text(5.0, 7.6, "Local-First • Open-Source • Sovereign", color='#94a3b8', fontsize=13, ha='center')

    ax.text(1.4, 6.6, "✓ Local SQLite Memory Core (Sub-millisecond recall)", color='#cbd5e1', fontsize=11.5)
    ax.text(1.4, 5.8, "✓ Socratic Sparring Partner (Pushes back on assumptions)", color='#cbd5e1', fontsize=11.5)
    ax.text(1.4, 5.0, "✓ 3-Bucket Wealth & Career Compounding Architecture", color='#cbd5e1', fontsize=11.5)
    ax.text(1.4, 4.2, "✓ 100% Air-Gapped: Your context never leaks", color='#4ade80', fontsize=11.5, fontweight='bold')

    # GitHub link badge
    gh_box = patches.FancyBboxPatch((1.6, 1.8), 6.8, 1.4, boxstyle="round,pad=0.15",
                                    facecolor='#1e293b', edgecolor='#64748b', linewidth=1)
    ax.add_patch(gh_box)
    ax.text(5.0, 2.7, "STAR & CLONE ON GITHUB:", color='#94a3b8', fontsize=10, ha='center')
    ax.text(5.0, 2.2, "github.com/Monish-Nallagondalla/Nirixa", color='#38bdf8', fontsize=12, fontweight='bold', ha='center')

    ax.text(0.8, 0.8, "BY MONISH NALLAGONDA", color='#64748b', fontsize=10)
    ax.text(9.2, 0.8, "NIRIXA OS 2026", color='#64748b', fontsize=10, ha='right')

    return fig

def compile_post_1_pdf(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with PdfPages(output_path) as pdf:
        s1 = create_slide_1_cover()
        pdf.savefig(s1, bbox_inches='tight', dpi=150)
        plt.close(s1)

        s2 = create_slide_2_comparison()
        pdf.savefig(s2, bbox_inches='tight', dpi=150)
        plt.close(s2)

        s3 = create_slide_3_cognitive_physics()
        pdf.savefig(s3, bbox_inches='tight', dpi=150)
        plt.close(s3)

        s4 = create_slide_4_cta()
        pdf.savefig(s4, bbox_inches='tight', dpi=150)
        plt.close(s4)

    print(f"[Visual Compiler] Compiled 4-Slide PDF Document at {output_path}")
    return output_path

if __name__ == "__main__":
    out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "content", "linkedin", "post-1-personal-agi-slides.pdf"))
    compile_post_1_pdf(out)
