# Product Requirements Document (PRD): Nirixa Episteme OS
**Category**: Epistemic Operating System & Cognitive CRM  
**Status**: Approved for Architecture & Implementation  
**Target Platform**: Full-Stack Next.js 14+ (App Router) • Offline-First Native SQLite (`nirixa.db`)  
**Lead Architect**: Monish Nallagondalla & Antigravity (Pair Programming / Chief of Staff AI)  
**Version**: 1.0.0 (Production Core)  
**Repository Target**: `My-Os/apps/episteme` (Private) & `nirixa-open-source/apps/episteme` (Public Showcase)

---

## 1. Executive Summary & Vision

### 1.1 The Epistemic Problem
Modern knowledge workers, researchers, and students face severe **cognitive fragmentation**:
1. Thoughts, voice notes, and sparks are captured on mobile (Telegram, WhatsApp) and die in forgotten chat threads.
2. Academic papers are read and annotated in silos (Apple Books, Preview, Zotero) without connecting to the thinker's living intellectual assets.
3. Content creation (LinkedIn, X, Substack) is disconnected from original research, resulting in either generic AI-marketing slop or sporadic publishing.
4. Long-term goals (PhD dissertations, books, keynotes) remain distant abstractions because daily friction never compounds systematically into chapter foundations.

### 1.2 The Solution: Nirixa Episteme
**Nirixa Episteme** is a category-defining **Epistemic Operating System and Cognitive CRM**. It unifies:
- **Multimodal Friction Capture**: Ingestion from Telegram (voice, text, YouTube links with auto-transcripts).
- **Epistemic Knowledge Graph**: 48 Original Thought Assets (OTAs) with mathematical affinity and lineage traversal.
- **In-Situ Academic Paper Reading**: PDF ingestion, highlight anchoring, and cross-paper gap synthesis.
- **Dual-Channel Distribution Studio**: High-signal LinkedIn publishing pipeline + Academic Thesis/LaTeX citation generator.
- **Living Human–AI Coevolution Cockpit**: Real-time telemetry documenting the interdependent coevolution of human cognition and an autonomous AI agent—serving as the living empirical laboratory for Monish's PhD publication.

---

## 2. User Personas & Primary Use Cases

### Persona A: Monish (The Technical PM & PhD Aspirant at EY)
- **Daily Context**: High-stress enterprise consulting at EY, strict client boundaries, mobile commute.
- **Goal**: Capture sparks on mobile via 2-second Telegram Share Sheet, synthesize research on weekends, publish high-signal technical essays on LinkedIn, and build undeniable research evidence for European PhD labs.
- **Pain Point**: Zero bandwidth for manual tagging or multi-server maintenance. Needs instant local execution.

### Persona B: Academic Researcher / Doctoral Student (Open-Source User)
- **Daily Context**: Reviewing 50+ papers per semester, building literature reviews, hunting for research gaps.
- **Goal**: Trace how one author's premise connects to another paper across disciplines, anchor notes to research questions, and export clean BibTeX/citation trees.

### Persona C: Lifelong Learner & Ambitious Student
- **Goal**: Replace chaotic Notion/Obsidian boards with a structured, compounding system that turns podcasts and books into published articles and personal mastery.

---

## 3. The 4 Life Segments Architecture

All thoughts, captures, and assets in Nirixa Episteme are categorized across **4 Living Segments**:

| Segment ID | Segment Name | Core Entities Tracked | Primary Output Artifact |
| :--- | :--- | :--- | :--- |
| **SEG-01** | **PhD Research Core** | RQ1–RQ8, Literature Gaps, Evidence Vault, Papers | Doctoral Proposal, Academic Papers |
| **SEG-02** | **LinkedIn Authority** | 48 OTAs, MoFu/ToFu Funnels, Lineage Trees | High-Signal Essays, Multi-Slide Carousels |
| **SEG-03** | **Enterprise Strategy** | Consulting Scars (Sanitized), Nirixa Engine, Open Source | System Architecture Specs, Open Source Releases |
| **SEG-04** | **Personal Life & Mastery** | Focus, Energy Routines, Life Milestones | Daily Clarity, Zero-Burnout Sustainability |

---

## 4. System Architecture & Technical Specifications

```
+---------------------------------------------------------------------------------+
|                                 CLIENT LAYER                                    |
|   Next.js 14+ (App Router) • React 18/19 • TailwindCSS • Lucide Icons           |
|   - Obsidian Dark Theme (#05070D)                                               |
|   - Interactive SVG/Canvas Knowledge Graphs                                     |
|   - Touch & Mobile Friendly (iPad Safari Compatible)                            |
+---------------------------------------------------------------------------------+
                                      |
                                      | Sub-millisecond Native Node Bindings
                                      v
+---------------------------------------------------------------------------------+
|                        LOCAL FULL-STACK SERVER LAYER                            |
|   Next.js Server Actions & API Route Handlers (/api/friction, /api/otas, etc.)  |
|   `better-sqlite3` Direct Engine (Read/Write Latency < 2ms)                     |
+---------------------------------------------------------------------------------+
                                      |
                   +------------------+------------------+
                   |                                     |
                   v                                     v
+------------------------------------+ +------------------------------------------+
|       DATA PERSISTENCE LAYER       | |         BACKGROUND DAEMONS               |
|  - SQLite Database (`nirixa.db`)   | |  - `telegram_listener.py` (24/7 Mobile)  |
|  - PDF Vault (`data/papers/*.pdf`) | |  - `ota_semantic_linker.py` (Embeddings) |
|  - Markdown Sync (`inbox/*.md`)    | |  - YouTube Transcript Fetcher            |
+------------------------------------+ +------------------------------------------+
```

### 4.1 Technology Stack & Decisions
1. **Frontend & Framework**: Next.js 14+ with App Router.
2. **Styling**: Vanilla CSS Modules + Tailwind CSS for surgical design tokens. Zero generic UI libraries.
3. **Database Engine**: `better-sqlite3`. Synchronous, direct C-level SQLite access. Zero network latency, zero cloud dependency, 100% offline.
4. **PDF Engine**: `pdfjs-dist` / `@react-pdf-viewer` for smooth, in-browser PDF rendering and text selection.
5. **Portability Invariant**: Configured via `.env.local` (`DATABASE_PATH=../../system/data/nirixa.db`). Runs identically in private `My-Os` and open-source `nirixa-open-source`.
6. **Zero External API Dependency**: Embeddings and classification execute locally via Python scripts or local algorithms. Agent interactions hook through file-based communication or Antigravity IDE sessions.

---

## 5. Core Functional Modules

### Module 1: Unified Friction Inbox & Triage Feed
- **Ingestion Sources**:
  - Telegram voice messages (transcribed locally).
  - YouTube video & Shorts links (automatic transcript fetch via `youtube_transcript_api`).
  - Text sparks and book quotes (via iOS 2-Second Share Sheet).
- **Automated Triage Engine**:
  - Automatically calculates TF-IDF and keyword affinity against the 48 OTAs.
  - Automatically maps capture to the most probable PhD Research Question (RQ1–RQ8).
  - In-UI One-Click Actions: `[Accept Linkage]`, `[Reroute to OTA]`, `[Convert to LinkedIn Draft]`, `[Archive]`.

### Module 2: The Thought Lineage & Provenance Traversal Engine
- **Lineage Chain**:
  $$\text{Raw Mobile Capture} \longrightarrow \text{Spark Question (OTA-001)} \longrightarrow \text{OTA Node (1-48)} \longrightarrow \text{PhD RQ (1-8)} \longrightarrow \text{LinkedIn Essay} \longrightarrow \text{Thesis Chapter}$$
- **Interactive Traversal UI**:
  - Clicking any node displays upstream parents (origins) and downstream children (publications).
  - Mathematical multi-attribute affinity score displayed on hover ($S = 0.45 \cdot \text{Vector} + 0.35 \cdot \text{Lexical} + 0.20 \cdot \text{PageRank}$).
  - Forward/Backward graph traversal with breadcrumb history.

### Module 3: In-Situ Research PDF Annotator & Gap Matrix
- **PDF Storage**: Cleanly managed under `data/papers/<file_hash>.pdf`.
- **Reader Interface**:
  - Split-screen workspace: PDF document on left (65%), active annotation & synthesis pane on right (35%).
  - Text Highlight Popup:
    1. `[Save as Note]`: Appends quote with exact page number and bounding box.
    2. `[Anchor to OTA]`: Connects paper quote directly to an OTA as supporting or falsifying evidence.
    3. `[Identify Research Gap]`: Flags as open problem for PhD Research Questions.
- **Cross-Paper Synapse Matrix**:
  - When viewing an annotation, the sidebar surfaces related annotations from other papers in the database with overlapping keywords.

### Module 4: LinkedIn Content Studio (The Authority Engine)
- **Drafting Workspace**:
  - Queue of **48 Unpublished OTAs** prominently displayed.
  - Split view: Thesis & Scars on left, clean drafting document on right.
- **Real-Time Validation Guardrails**:
  - Character counter: LinkedIn (max 3,000 chars), X.com (max 280 chars with thread break indicators).
  - **Tone & Signal Auditor**: Flags hype emojis (🔥, 🚀), buzzwords, and marketing gimmicks. Enforces minimalist, high-signal tech copywriting.
  - Auto-compiles multi-slide carousels into ready-to-upload PDF documents.

### Module 5: The Book & 2029 TED Talk Compounding Tracker
- **Foundational Chapters**:
  - Tracks 8 foundational book chapters corresponding to the core philosophical pillars.
  - **Chapter Density Metric**: Automatically calculated as:
    $$\text{Maturity} = \frac{\text{OTAs Bound} \times 2 + \text{Published Essays} \times 3 + \text{Paper Annotations} \times 1.5}{\text{Target Threshold}} \times 100\%$$
  - Provides Monish with quiet, compounding progress that builds toward the 2029 Keynote without daily pressure.

### Module 6: Human–AI Coevolution Telemetry Cockpit (The Living PhD Artifact)
- **Live Empirical Evidence**:
  - Records session history, agent prompt iterations, and Socratic challenge rates.
  - Quantifies cognitive scaffolding and conceptual drift over time.
  - One-Click **Export to LaTeX**: Generates publication-ready figures, tables, and interaction logs for academic papers.

---

## 6. Database Schema Extensions (`nirixa.db`)

The existing database already holds `raw_captures`, `otas`, `phd_research_questions`, and `graph_nodes`. We cleanly introduce 3 complementary tables:

```sql
-- Research Papers Table
CREATE TABLE IF NOT EXISTS papers (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    year INTEGER,
    venue TEXT,
    doi TEXT,
    abstract TEXT,
    file_path TEXT NOT NULL,
    file_hash TEXT UNIQUE NOT NULL,
    total_pages INTEGER DEFAULT 1,
    phd_rq_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (phd_rq_id) REFERENCES phd_research_questions(id)
);

-- Research Annotations Table
CREATE TABLE IF NOT EXISTS paper_annotations (
    id TEXT PRIMARY KEY,
    paper_id TEXT NOT NULL,
    page_number INTEGER NOT NULL,
    highlighted_text TEXT NOT NULL,
    note TEXT,
    annotation_type TEXT CHECK(annotation_type IN ('note', 'ota_anchor', 'research_gap')) DEFAULT 'note',
    linked_ota_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (paper_id) REFERENCES papers(id) ON DELETE CASCADE,
    FOREIGN KEY (linked_ota_id) REFERENCES otas(id)
);

-- Book Anthology Chapters Table
CREATE TABLE IF NOT EXISTS book_chapters (
    id TEXT PRIMARY KEY,
    chapter_number INTEGER NOT NULL,
    title TEXT NOT NULL,
    subtitle TEXT,
    synopsis TEXT,
    target_ota_count INTEGER DEFAULT 6,
    maturity_percentage REAL DEFAULT 0.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7. UI/UX Design System & Ergonomics (Awwwards SOTD Benchmark)

### 7.1 Visual Tokens
- **Background**: Void Cosmic Obsidian (`#06080F` to `#08090E`) with subtle 3% ambient grain and multi-color atmospheric blur spheres.
- **Surfaces**: Frosted Translucent Dark Glass (`rgba(16, 18, 27, 0.65)`) with `backdrop-filter: blur(32px) saturate(180%)`.
- **Directional Lighting**: 1px top-edge rim lighting (`linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent)`).
- **Accents**:
  - **Synapse Cyan** (`#38BDF8`): Links, traversal paths, highlight anchors, primary actions.
  - **Spectral Violet** (`#818CF8` / `#A855F7`): Academic papers, research questions, citations.
  - **Solar Amber** (`#FBBF24`): Book chapters, authority milestones, 2029 Keynote goals.
  - **Electric Emerald** (`#34D399`): Telegram voice sparks, live stream telemetry.
- **Typography**: `Inter` with optical kerning (`letter-spacing: -0.02em`) paired with `JetBrains Mono` for surgical data tags and shortcuts.

### 7.2 The 4 Core Views (The Complete Suite)
1. **The Executive Cockpit Bento (Primary Hub)**:
   - 4 Life Segments switcher (*PhD Core*, *LinkedIn Authority*, *Enterprise Strategy*, *Personal Mastery*).
   - Weekly Compounding Dials (Papers Annotated, OTAs Connected, Book Chapter 2 Maturity at 74%).
   - Mobile Audio Waveform Player for recent Telegram voice notes with transcription tags.
   - Interactive 3D Mini-Constellation of active synaptic connections.
2. **The Cosmic Knowledge Orbit (Planetary Constellation)**:
   - Full-canvas concentric planetary orbital rings connecting all 48 OTAs and PhD RQs.
   - Floating frosted-glass inspector card showing upstream origin, downstream publication, and academic citations.
3. **The In-Situ Research PDF Lab**:
   - High-resolution PDF document viewer with margin notes.
   - Text highlight popup dock (`[Cite]`, `[Link Concept]`, `[Anchor to OTA]`).
4. **The LinkedIn & Thesis Writing Studio**:
   - 48 Unpublished OTAs dropdown selector.
   - Real-time character counter (LinkedIn 3,000 / X.com 280 chars).
   - AI High-Signal Tone Validator badge (*Zero Hype • High Density*).

---

## 8. Rollout Plan & Milestones

- **Phase 1: Project Initialization & Core API (Current)**
  - Initialize `apps/episteme` Next.js 14 project.
  - Set up `better-sqlite3` native database client and API routes.
  - Establish Dark Obsidian design tokens and layout shell.
- **Phase 2: Friction Inbox & OTA Synapse Traversal**
  - Live Telegram capture feed and YouTube transcript viewer.
  - 48 OTAs constellation and bidirectional lineage traversal rail.
- **Phase 3: In-Situ Research PDF Annotator**
  - PDF upload, canvas rendering, text selection highlight popup, and SQLite note anchoring.
- **Phase 4: LinkedIn Studio & Book Compounding Cockpit**
  - Content drafting workspace, character auditor, chapter maturity meters.
- **Phase 5: Open-Source Sync & Showcase Release**
  - Sanitize personal data, generate `sample.db`, and sync directly to `nirixa-open-source`.

---

*This document serves as the permanent, tool-agnostic architectural specification for Nirixa Episteme OS.*
