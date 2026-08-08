# Master Architecture & Technical Specification: My-OS

# Personal Intelligence Operating System (Nirixa OS Engine v0.1)

**System Owner**: Monish Nallagondalla  
**Document Purpose**: Comprehensive end-to-end technical reference, directory map, subsystem specification, and architectural review package for external analysis and feedback (prepared for Claude / AI Reviewers / Engineering Interns).  
**Date**: August 2026  
**Status**: Production Baseline (Phase 1 Complete + Phase 2 Chief of Staff Engine Implemented)

---

## 1. Executive Summary & Core Philosophy

**My-OS** (powered by the backend **Nirixa OS Engine**) is a personal intelligence operating system built to augment long-term human thinking, decision-making, and original content creation over decades.

Unlike conventional note-taking applications (Obsidian, Notion) or standard conversational AI wrappers (ChatGPT wrappers), My-OS is designed as an **event-driven, repo-native intelligence hub** that captures raw mobile friction, refines ideas through interactive sparring, schedules time blocks, and automates platform-native publishing.

```
+-------------------------------------------------------------------------+
|                         CORE ARCHITECTURAL AXIOM                         |
+-------------------------------------------------------------------------+
|  1. Memory belongs to the repository (system/data/nirixa.db & Markdown) |
|  2. Reasoning belongs to the AI (Chief of Staff & Persona Models)       |
|  3. Judgment belongs to the human (Monish Nallagondalla)                |
+-------------------------------------------------------------------------+
```

---

## 2. Workspace Directory Map & System Taxonomy

The repository is organized into distinct functional layers separating long-term memory, engine code, agent skills, and content outputs:

```
My-Os/
├── .agents/                      # Agent Customization & Skill Roots
│   └── skills/                   # The 10 Active Agent Custom Skills
│       ├── agent-evaluator/      # Reader persona evaluation matrix (Engineer, Exec, PM)
│       ├── calendar-scheduler/   # Actionable task -> Google Calendar scheduling
│       ├── content-stylist/      # High-Signal Minimalist minimalist copywriting engine
│       ├── daily-login/          # Login context resumption ("I am back")
│       ├── daily-signoff/        # End-of-day signoff & mobile push workflow
│       ├── founder-council-evaluator/ # Multi-founder strategic audit (Jobs, Huang, etc.)
│       ├── mobile-sync/          # Telegram thought ingestion to monthly inbox log
│       ├── mobile-task-delegator/ # Async mobile micro-task & decision push
│       ├── omni-channel-publisher/ # X.com (280-char/threads) & LinkedIn (PDF carousel)
│       └── persona-advisory-board/ # Multi-persona debate engine (Cagan, Goggins, etc.)
├── AGENTS.md                     # The 9 Non-Negotiable System Operating Rules
├── README.md                     # High-level vision & philosophical principles
├── docs/                         # System Documentation & Specifications
│   ├── ARCHITECTURE.md           # High-level architectural diagrams
│   ├── CAREER_DASHBOARD.md       # Strategic career goals & milestones
│   ├── MY_OS_MASTER_ARCHITECTURE.md # (This Document) Master Spec & Audit Package
│   ├── PLAYBOOK.md               # Standard operating procedures
│   ├── PRD.md                    # Product vision & 5-Phase Roadmap
│   ├── SYSTEM_CAPABILITIES_PRD.md # Live system capability specification
│   └── VISION.md                 # Long-term philosophy & non-goals
├── system/                       # Nirixa OS Engine Core Infrastructure
│   ├── Chief-of-Staff.md         # Operational Chief of Staff prompt spec
│   ├── config/                   # Configuration files (config.yaml, .env)
│   ├── data/                     # Data persistence & state tracking
│   │   ├── nirixa.db             # Primary SQLite Memory Core
│   │   └── synced_messages.json  # 7-day Telegram chat message retention state
│   ├── engine/                   # Python Core Engine Modules
│   │   ├── chief_of_staff.py     # [NEW] Unified Cross-Domain Strategic Dispatcher
│   │   ├── daemon.py             # Event-Driven Telegram Listener & Telemetry Loop
│   │   ├── db.py                 # SQLite Memory Core & FTS5 Indexing
│   │   ├── evolver.py            # Self-Evolution Engine & Capability Logging
│   │   ├── skill_distiller.py    # Workflow-to-Skill Distillation Engine
│   │   └── synthesizer.py        # Spar-First Intelligence & Thesis Extractor
│   └── scripts/                  # Background Scripts & Windows Launchers
│       ├── bot_listener.py       # Telegram polling listener
│       ├── calendar_sync.py      # Google Calendar OAuth2 API Sync
│       ├── enable_autostart.bat  # Windows Startup Registry Integration
│       ├── start_silent_daemon.vbs # Detached silent daemon process wrapper
│       ├── stop_daemon.bat       # Process shutdown script
│       └── telegram_push.py      # Asynchronous outbound notification script
├── inbox/                        # Monthly Mobile Stream Consolidation Hubs
│   └── 2026-08-mobile-inbox.md   # Active month processed mobile notes
├── content/                      # Refined Original Thought Assets & Calendars
│   └── linkedin/                 # Master LinkedIn content calendar & assets
├── career/                       # Career strategy, resume iterations & network
├── knowledge/                    # Long-term evergreen mental models & frameworks
├── projects/                     # Shared active projects execution directory
└── journal/                      # Daily reflections & unedited observations
```

---

## 3. End-to-End System Data Flow & Architecture

```
                                  +---------------------------------------+
                                  |      MONISH (Mobile Telegram)         |
                                  +-------------------+-------------------+
                                                      |
                                       (Raw Audio / Text Capture)
                                                      v
                                  +-------------------+-------------------+
                                  |  Nirixa OS Engine Daemon              |
                                  |  (system/engine/daemon.py)            |
                                  +---------+-------------------+---------+
                                            |                   |
                     +----------------------+                   +---------------------+
                     | (Ingest Raw Note)                                              | (Periodic Trigger)
                     v                                                                v
+--------------------+---------------------+                      +-------------------+-------------------+
| SQLite Memory Core                       |                      | Unified Chief of Staff Dispatcher |
| (system/data/nirixa.db)                  |                      | (system/engine/chief_of_staff.py) |
| - raw_captures (FTS5 search)             |                      +---------+-------------------+---------+
| - otas (Original Thought Assets)         |                                |                   |
| - reminders & evolution_logs             |                                |                   |
+--------------------+---------------------+                                |                   |
                     |                                                      |                   |
                     | (Sparring / Context Retrieval)                       v                   v
                     v                                            +---------+--------+  +-----+-----------+
+--------------------+---------------------+                      | Synthesizer Engine|  | GCal Sync Engine|
| 3-Stage Sync Workflow                    |                      | (synthesizer.py) |  | (calendar_sync) |
| 1. Buffer (Telegram ingestion)           |                      +------------------+  +-----------------+
| 2. Sparring (Interactive Q&A)            |                                |
| 3. Processed Save (inbox/ & content/)    |                                v
+--------------------+---------------------+                      +-----------------------------------+
                     |                                            | Omni-Channel Publishing Engine    |
                     +------------------------------------------->| (.agents/skills/omni-channel-pub) |
                                                                  | - X.com 280-char / 1/N threads    |
                                                                  | - LinkedIn Single Auto-PDF        |
                                                                  +-----------------------------------+
```

---

## 4. In-Depth Subsystem Technical Specifications

### 4.1. The Unified Chief of Staff Dispatcher (`system/engine/chief_of_staff.py`)
- **Role**: Serves as the central reasoning orchestrator across Career, Learning, Projects, and Writing.
- **Key Functions**:
  - `get_cross_domain_context()`: Aggregates active milestones from `docs/CAREER_DASHBOARD.md`, active project directories in `projects/`, recent Original Thought Assets (OTAs) from `nirixa.db`, and pending reminders.
  - `synthesize_strategic_briefing(briefing_type)`: Generates structured Morning Priorities and Evening Reflection briefings combining unread captures with domain objectives.
  - `evaluate_skill_distillation(workflow_name, target_intent)`: Enforces the **Merge-First Skill Rule** to prevent skill proliferation.

### 4.2. Event-Driven Telegram Daemon (`system/engine/daemon.py`)
- **Role**: Continuous non-blocking background process providing 24/7 mobile connectivity.
- **Key Capabilities**:
  - Real-time polling and callback button handling (`answerCallbackQuery`).
  - Proactive Daily Briefings (Morning priorities at 08:00, Evening signoff prompt at 20:00).
  - Laptop Telemetry & Battery Monitor: Monitors battery percentage and power status, sending immediate alerts when running low without AC power.
  - Zero-LLM Fast Path: Intercepts deterministic reminder strings (e.g., `remind me in 30m to check build`) and persists directly to SQLite without invoking LLM tokens.

### 4.3. SQLite Database Memory Core (`system/engine/db.py`)
- **Location**: `system/data/nirixa.db` (Zero-dependency SQLite store).
- **Tables**:
  - `raw_captures`: `id`, `update_id`, `timestamp`, `chat_id`, `raw_text`, `anonymized_text`, `source`, `status`.
  - `conversation_threads`: `id`, `session_id`, `user_prompt`, `agent_reply`, `timestamp`.
  - `otas`: `id`, `capture_id`, `title`, `raw_thought`, `refined_thesis`, `draft_x`, `draft_linkedin`, `status`, `created_at`.
  - `reminders`: `id`, `chat_id`, `message`, `remind_at`, `status`, `created_at`.
  - `evolution_logs`: `id`, `capture_id`, `rating`, `feedback_text`, `rule_extracted`, `created_at`.
  - `system_audits`: `id`, `metric_name`, `metric_value`, `timestamp`.
  - `raw_captures_fts`: SQLite FTS5 Virtual Table for full-text keyword indexing across captures.

### 4.4. Synthesizer & Evolver Modules (`synthesizer.py`, `evolver.py`, `skill_distiller.py`)
- **`synthesizer.py`**: Extracts authentic scars, raw context, refined theses, and content angles during interactive sparring.
- **`evolver.py`**: Records feedback ratings on generated assets and appends learnings to system rules.
- **`skill_distiller.py`**: Distills repeating multi-step user workflows into candidate skill definitions.

### 4.5. Google Calendar Synchronization Engine (`system/scripts/calendar_sync.py`)
- Authenticates via OAuth2 (`credentials.json` / `token.pickle`).
- Parses time-blocked tasks from My-OS thoughts and programmatically inserts event blocks into Google Calendar.

---

## 5. The Multi-Agent Skill Suite (`.agents/skills/`)

My-OS operates 10 specialized agent skills:

1. **`mobile-sync`**: Fetches raw Telegram notes, formats them into `inbox/YYYY-MM-mobile-inbox.md`, and commits updates to Git.
2. **`daily-login`**: Resumes context when Monish says "I am back", providing a clean summary of unread mobile captures.
3. **`daily-signoff`**: Handles end-of-day sign-off, logging finished work and pushing pending tasks to Telegram for mobile review.
4. **`mobile-task-delegator`**: Delegates low-friction micro-tasks (sparring prompts, voice note requests, inline decision buttons) to Monish's phone.
5. **`omni-channel-publisher`**: Enforces strict platform mechanics (splits X posts into <280 char threads; auto-compiles multi-slide LinkedIn carousels into single ready-to-upload PDF documents).
6. **`content-stylist`**: Enforces First-Principles Technical Copywriting copywriting standard (zero hype emojis, sparse line breaks, high thesis density).
7. **`persona-advisory-board`**: Runs multi-perspective debates (Marty Cagan for product vision, David Goggins for discipline, Paramahansa Yogananda for core purpose).
8. **`founder-council-evaluator`**: Audits strategy against elite tech leaders (Steve Jobs, Jensen Huang, Sundar Pichai, Mark Zuckerberg).
9. **`agent-evaluator`**: Simulates target reader personas (Senior Engineer, Executive VP, Junior PM) to score emotional impact.
10. **`calendar-scheduler`**: Translates structured task definitions into Google Calendar API payloads.

---

## 6. System Governance & Non-Negotiable Rules (`AGENTS.md`)

All operations strictly adhere to **9 non-negotiable rules**:

1. **Collaborative Q&A Before Execution**: Dialogue first; talk through ideas and refine approaches via Q&A before modifying files or running commands.
2. **3-Stage Sync Workflow**: Buffer (Telegram capture) -> Sparring (interactive refinement) -> Processed Save (save to `inbox/` & content calendars).
3. **Zero File Proliferation**: Consolidate thoughts into central monthly hubs (`inbox/YYYY-MM-mobile-inbox.md`) and active master content plans.
4. **7-Day Rolling Retention**: Telegram chat messages tracked in `system/data/synced_messages.json` are auto-cleaned from chat after 7 days.
5. **Strict Anonymization**: Never expose client names or proprietary systems; abstract into structural architectural patterns.
6. **Proactive End-to-End Execution Standard**: Never deliver raw intermediate assets (e.g., carousels MUST be auto-compiled as single ready-to-upload PDFs).
7. **High-Signal Minimalist Copywriting**: Zero emoji clutter (no 🔴, 🟢, 🔥, 🚀), high density, razor-sharp thesis.
8. **Monish 10/10 Quality Calibration**: Zero self-satisfaction; baseline expectations set to zero-prompt autonomy and top 1% content execution.
9. **Proactive Mobile Task Delegation**: Chief of Staff authorized to push low-friction micro-tasks to Telegram when Monish is away from desk.

---

## 7. The Three Key Structural Solutions Implemented

During system analysis, three critical structural friction points were resolved:

### Solution 1: Unified Chief of Staff Dispatcher (`system/engine/chief_of_staff.py`)
- **Problem**: Chief of Staff responsibilities were scattered across daemon listeners, skills, and synthesizers without a central reasoning component.
- **Fix**: Implemented `chief_of_staff.py` as an Orchestrator/Dispatcher layer. It aggregates cross-domain state (Career, Learning, Projects, OTAs) and acts as the central coordinator for briefings, sparring, and delegation.

### Solution 2: Air-Gapped Publish-Time Anonymization Policy
- **Problem**: Anonymizing raw captures at *storage time* stripped raw context, names, and code identifiers needed for high-precision semantic retrieval in Phase 3.
- **Fix**: Defined an explicit **Air-Gap Boundary**. Local SQLite storage (`nirixa.db`) preserves 100% authentic, un-sanitized context for local vector embeddings. Strict anonymization (Rule 5) is enforced **exclusively at Publish-Time** when exporting to external platforms (LinkedIn PDFs, X threads, public docs).

### Solution 3: Merge-First Skill Governance against Proliferation
- **Problem**: Automated workflow distillation (`skill_distiller.py`) risked creating hundreds of single-use skill folders, violating Rule 3.
- **Fix**: Enforced a **Merge-First Governance Rule** inside `chief_of_staff.py`. Newly distilled workflows must first attempt to merge into existing skill hubs (`omni-channel-publisher`, `mobile-sync`, `content-stylist`) before spawning new folders.

---

## 8. Detailed Roadmap Position & Phase 3 Gap Analysis

### Current Status Matrix

| Roadmap Phase | Target Description | Implementation Status | Delta / Notes |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Repository, Journal, Manual Workflow | **COMPLETED + SURPASSED** | Surpassed manual workflow with non-blocking event-driven Telegram daemon (`daemon.py`). |
| **Phase 2** | CLI, Context Builder, Chief of Staff | **COMPLETED & VALIDATED** | Telegram acts as mobile interface; `synthesizer.py` builds context; `chief_of_staff.py` unifies cross-domain reasoning & conflict detection. |
| **Phase 3** | Knowledge Graph, Thought Resonance, Semantic Retrieval | **COMPLETED (v0.2 Baseline)** | Implemented `sqlite-vec` vector store (`vec_otas`), 3-signal resonance engine (`resonance.py`), `ota_edges` graph store, and context injection. |
| **Phase 4** | Local Intelligence Layer & Multi-Model Support | Planned | Local LLM fallback & multi-model routing. |
| **Phase 5** | Personal Intelligence Platform | Long-term | Autonomous multi-device personal intelligence network. |

### Gap Closure Status: v0.2 Implemented & Verified

All priority items from the Gap Closure Brief have been systematically implemented and verified:
- **P0 (Daemon Reliability)**: Built-in exponential backoff, unhandled crash logging, `system_audits` heartbeats, boot self-checks, and Windows Startup auto-launch.
- **P1 (Delegator Rate Limiting)**: `daily_cap: 4` in `config.yaml`, `quiet` mute commands, outcome tracking, and 7-day dismissal auto-adjustment.
- **P2 (Phase 3 Retrieval)**: `sqlite-vec` vector store (`vec_otas`), 3-signal `resonance.py`, `ota_edges` threshold graph table, and context injection.
- **P2b (Reasoning Validation)**: `chief_of_staff.py` conflict detection (`detect_cross_domain_conflicts()`) verified via `test_chief_of_staff.py` (5/5 unit tests passed).
- **P3 (Governance & Metrics)**: Separated Rule 8 into `docs/STANDARDS.md`, tracked PRD metrics (`product_metrics` table in SQLite).

---

## 9. Strategic Questions & Review Vectors for External Critique (Claude)

We invite Claude / external system reviewers to analyze this architecture and provide feedback on the following 5 strategic questions:

1. **Vector Memory Store for Phase 3**: Given our zero-dependency SQLite constraint (`nirixa.db`), should we integrate `sqlite-vss` / `sqlite-vec` directly into SQLite, or maintain a lightweight companion vector store (e.g., ChromaDB / LanceDB) for fast semantic similarity search?
2. **Thought Resonance Algorithm**: How should "Thought Resonance" be mathematically quantified? (e.g., a hybrid score combining Cosine Similarity of embeddings + Recency Decay + Domain Overlap between Career/Learning/Projects)?
3. **Graph Topology**: Should old thoughts be linked in a true Graph structure (nodes = OTAs, edges = semantic relationships), or is a dynamic vector retrieval top-K enough for personal intelligence?
4. **Context Window Optimization**: When `chief_of_staff.py` synthesizes context for sparring, what is the optimal chunking strategy to feed relevant past OTAs into the prompt without blowing token budgets?
5. **Autonomy vs. Friction**: How far can mobile task delegation (`mobile-task-delegator`) go toward zero-prompt autonomy before it becomes noisy for Monish on mobile?

---

## 10. Integrated 3-Track Evaluation Framework

To ensure system reliability, structural evolution tracking, and personal cognitive outcomes, My-OS implements a 3-track evaluation architecture:

- **Track A (System Health Evals)**: An automated 8-check regression suite ([run_system_evals.py](file:///c:/Users/MONISH/OneDrive/Documents/My-Os/system/engine/evals/run_system_evals.py)) logging pass/fail results into `eval_results`. Checks daemon liveness, startup integrity, capture pipeline live smoke test, Chief of Staff reasoning, resonance accuracy, publishing compliance (Rule 7 emoji audit + 280-char X split), anonymization air-gap boundaries, and data integrity.
- **Track B (Capability Snapshots - Day 1 to Day N)**: Captures time-series capability snapshots in `capability_snapshots` table (`active_skill_count`, `active_skill_names`, `table_count`, `rule_count`, `eval_pass_rate`, `total_otas`, `total_captures`). Automatically triggered by `evolver.py`.
- **Track C (Personal Growth & Outcomes)**:
  - *Part 1 (Objective Proxies)*: Capture-to-published latency, OTA resurfacing rate, near-duplicate capture rate, and monthly published volume tracked in `product_metrics`.
  - *Part 2 (Structured Self-Assessments)*: Monthly 1-5 scale ratings for Clarity of Thinking, Decision Quality, and Overall Progress stored in `self_assessments`.

