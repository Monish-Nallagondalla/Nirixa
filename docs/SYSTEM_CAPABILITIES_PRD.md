# Product Requirements Document (PRD): Implemented System Capabilities

# My-OS / Nirixa OS Engine v0.1

**Author**: Monish Nallagondalla 
**Status**: Implemented & Operational (Production Baseline) 
**Date**: August 2026 
**Document Purpose**: Definitive technical specification and architectural inventory of all operational capabilities, daemons, skills, and data flows within **My-OS** for subsequent structural analysis, auditing, and optimization.

---

## 1. Executive Summary & Core System Vision

**My-OS** (powered by the **Nirixa OS Engine**) is a Personal Intelligence Operating System designed to augment human thinking over long horizons. Rather than serving as a passive note-taking repository, task manager, or standard AI wrapper, My-OS acts as a **living, event-driven intelligence hub** that captures mobile friction, refines raw thoughts into Original Thought Assets (OTAs), automates scheduling, and enforces elite copywriting and execution standards across platforms.

### Core Architectural Axiom
- **Memory belongs to the repository** (`system/data/nirixa.db`, markdown hubs).
- **Reasoning belongs to the AI** (Chief of Staff, Synthesizer, persona models).
- **Judgment belongs to the human** (Monish Nallagondalla).

---

## 2. Implemented Subsystems Overview

```
+-----------------------------------+
| Mobile Telegram Interface |
+-----------------+-----------------+
| (Webhooks / Polling)
v
+-----------------+-----------------+
| Nirixa OS Engine Daemon |
| (system/engine/daemon.py) |
+--------+----------------+---------+
| |
+-----------------+ +------------------+
v v
+------------+-------------+ +---------+----------------+
| SQLite Memory Core | | Telemetry & Auto-Start |
| (system/data/nirixa.db) | | (VBS, Batches, GCal) |
+------------+-------------+ +---------+----------------+
| |
v v
+------------+-------------+ +---------+----------------+
| 3-Stage Sync Workflow | | Multi-Agent Skill Suite |
| (Buffer -> Spar -> Save) | | (.agents/skills/*) |
+--------------------------+ +--------------------------+
```

---

## 3. Implemented Infrastructure & Backend Engines

### 3.1. Event-Driven Telegram Daemon (`system/engine/daemon.py`)
- **Real-Time Event Processing**: Operates a non-blocking asynchronous event loop listening for Telegram updates, messages, and callback button presses (`answerCallbackQuery`).
- **Proactive Daily Briefings**:
- **Morning Briefing**: Synthesizes priorities, unread mobile captures, and scheduled calendar blocks.
- **Evening Reflection**: Queries completed tasks, pending items, and prompts for evening sign-off.
- **Laptop Telemetry & Battery Monitoring**: Tracks battery percentage and power source; issues real-time alerts when running low on battery without AC power.
- **Zero-LLM Fast Path Reminders**: Handles exact-time and relative-time reminder parsing without invoking full LLM reasoning loops.

### 3.2. SQLite Database Memory Core (`system/engine/db.py`)
- **Location**: `system/data/nirixa.db` (Zero-dependency SQLite store).
- **Implemented Schema**:
1. `raw_captures`: Ingests mobile Telegram thoughts (`update_id`, `timestamp`, `raw_text`, `anonymized_text`, `status`).
2. `conversation_threads`: Tracks prompt-response trajectories for session context.
3. `otas` (Original Thought Assets): Stores refined thesis statements, LinkedIn/X content angles, and authentic scars.
4. `reminders`: Manages scheduled reminders with trigger times and execution flags.
5. `system_evolution`: Logs system upgrades, capability additions, and autonomous changes.
6. `audit_logs`: Records errors, system health checks, and daemon execution telemetry.

### 3.3. Chief of Staff Dispatcher & Core Synthesizer Modules
- **Unified Chief of Staff Dispatcher (`system/engine/chief_of_staff.py`)**: Consolidates cross-domain strategic reasoning across Career, Learning, Projects, and Writing. Coordinates mobile briefings, task delegation, and enforces Merge-First Skill Governance.
- **Synthesizer Engine (`system/engine/synthesizer.py`)**: Spar-first intelligence engine that constructs targeted multi-choice questions and thesis challenges during mobile sparring.
- **Self-Evolution Engine (`system/engine/evolver.py`)**: Evaluates operational metrics and updates system capability manifests.
- **Skill Distiller (`system/engine/skill_distiller.py`)**: Distills repeating multi-step workflows into reusable agent skills.

### 3.4. Windows Silent Background Auto-Start
- **Files**:
- `system/scripts/start_silent_daemon.vbs`: VBScript wrapper launching the daemon detached from console windows.
- `system/scripts/enable_autostart.bat` & `setup_windows_autostart.bat`: Registers startup hooks in Windows Startup folder for zero-touch 24/7 background uptime.
- `system/scripts/stop_daemon.bat`: Gracefully terminates running background python processes.

### 3.5. Google Calendar Integration Engine (`system/scripts/calendar_sync.py`)
- **OAuth2 Token Handling**: Authenticates via `credentials.json` and caches access tokens in `token.pickle`.
- **Automated Block Scheduling**: Parses actionable tasks, writing sessions, and career milestones from My-OS thoughts directly into Google Calendar events.

---

## 4. Multi-Agent Skill Suite (`.agents/skills/`)

The workspace contains **10 active custom skills** configured for specialized agent execution:

| Skill Directory | Primary Function & Capabilities |
| :--- | :--- |
| **`mobile-sync`** | Automates fetching raw Telegram thoughts into monthly inbox logs (`inbox/YYYY-MM-mobile-inbox.md`), applies strict anonymization, and pushes updates to Git. |
| **`daily-login`** | Executes context resumption when user logs in ("I am back"), summarizing unread Telegram messages and pending system state. |
| **`daily-signoff`** | Handles end-of-day signoff workflow, prompts for status updates, logs completed items, and pushes pending tasks to Telegram for async mobile review. |
| **`mobile-task-delegator`** | Delegates micro-tasks (sparring prompts, 30s voice note requests, inline approval buttons, strategic options) to Monish's phone via Telegram. |
| **`omni-channel-publisher`** | Platform-native publishing mechanics: strictly validates X 280-char limits, splits long posts into `1/N` threads, auto-compiles multi-slide graphics into single PDF documents for LinkedIn, and generates explicit Document Titles. |
| **`content-stylist`** | Enforces high-signal, minimalist tech copywriting (Naval Ravikant & Aviral Bhatnagar standard). Eliminates hype emojis, colored dots, and artificial sales formatting. |
| **`persona-advisory-board`** | Simulates multi-perspective debates among core personas (Marty Cagan for product vision, David Goggins for relentless discipline, Paramahansa Yogananda for deep purpose). |
| **`founder-council-evaluator`** | Audits My-OS architecture and content through the lens of elite tech leaders (Steve Jobs, Jensen Huang, Sundar Pichai, Mark Zuckerberg). |
| **`agent-evaluator`** | Evaluates content drafts against 3 simulated target reader personas (Senior Engineer, Executive VP, Junior PM), generating emotional response matrices and tuning suggestions. |
| **`calendar-scheduler`** | Converts task specifications into Google Calendar API event payloads. |

---

## 5. Governance & Operating Rules (`AGENTS.md`)

The operational behavior of the system is governed by **9 non-negotiable rules**:

1. **Collaborative Q&A Before Execution**: Dialogue first; explore options and refine approaches via Q&A before editing code or running execution commands.
2. **3-Stage Sync Workflow**: Buffer (Telegram capture) -> Sparring (interactive refinement via Q&A) -> Processed Save (save refined thesis into `inbox/YYYY-MM-mobile-inbox.md` & content calendars).
3. **Zero File Proliferation**: Avoid creating unnecessary markdown files; consolidate thoughts into central monthly hubs and active content plans.
4. **7-Day Rolling Retention**: Synced Telegram chat messages are tracked in `system/data/synced_messages.json` and automatically pruned from chat interface after 7 days.
5. **Strict Anonymization**: Never expose specific company names, client names, or proprietary systems. Abstract to architectural patterns and psychological insights.
6. **Proactive End-to-End Execution Standard**: Never deliver raw intermediate assets (e.g., carousels MUST be auto-compiled as single ready-to-upload PDFs).
7. **High-Signal Minimalist Copywriting**: Zero emoji clutter (no , , , ), sparse line breaks, high thesis density.
8. **Monish 10/10 Quality Calibration**: Zero self-satisfaction; baseline expectations set to zero-prompt autonomy and top 1% content execution.
9. **Proactive Mobile Task Delegation**: Chief of Staff AI authorized to push low-friction micro-tasks to Telegram when Monish is away from desk.

---

## 6. Analysis Framework & Evaluation Dimensions

To perform an in-depth structural analysis of what is implemented, the following dimensions are specified:

### 6.1. Architectural Latency & Performance
- Event loop polling response times in `daemon.py`.
- SQLite query concurrency and locking handling in `db.py`.
- Network resiliency of Telegram API calls and Google Calendar OAuth token refresh cycles.

### 6.2. Content Pipeline Quality & Signal-to-Noise Ratio
- Compliance rate with Naval/Aviral copywriting style across generated assets.
- Anonymization coverage across ingested raw mobile thoughts.
- Single-page PDF auto-compilation reliability for LinkedIn multi-slide graphics.

### 6.3. Roadmap Alignment & Gap Analysis
- Comparison of current implementation against **Phase 1-5 Roadmap** in `docs/PRD.md`.
- Evaluation of current transition state between Phase 2 (Chief of Staff & Context Builder) and Phase 3 (Knowledge Graph & Thought Resonance).
