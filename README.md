<div align="center">

# ⚡ NIRIXA OS

**The Open-Source, Local-First Personal AI Operating System & Thought Architecture**

*Event-Driven Mobile Ingestion • Sub-Millisecond SQLite Memory • 3-Track Eval Suite • Zero-Hype Output*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: Local--First](https://img.shields.io/badge/Architecture-Local--First-emerald.svg)](#)
[![Evaluations: 3--Track](https://img.shields.io/badge/Evals-3--Track%20Harness-purple.svg)](#)
[![Build: Passing](https://img.shields.io/badge/Build-Passing-brightgreen.svg)](#)

<p align="center">
  <a href="#-the-problem">The Problem</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-quickstart">Quickstart</a> •
  <a href="#-core-subsystems">Subsystems</a> •
  <a href="#-evaluations--telemetry">Evaluations</a> •
  <a href="#-configuration">Configuration</a> •
  <a href="#-contributing">Contributing</a>
</p>

</div>

---

## 🛑 The Problem with Modern AI Agents

Most AI agent frameworks today suffer from three fatal design flaws:

1. **Non-Deterministic Memory Decay**: Storing agent context in bloated prompt context windows or cloud vector databases leads to prompt rot, high latency ($>10s$), and hallucinations.
2. **Infinite Reasoning Deadlocks**: Daisy-chaining autonomous agents without strict deterministic boundaries compounds failure rates exponentially.
3. **Cloud Lock-In & Privacy Leaks**: Personal journals, raw mobile notes, and proprietary work thoughts are shipped to unverified third-party cloud wrappers.

**Nirixa OS** was built from first principles to solve this. It is a **local-first, event-driven personal AI operating system** that turns fragmented thoughts, voice notes, and friction into high-density assets while keeping 100% of your data private on your local disk.

---

## 🏛️ Architecture & System Philosophy

Nirixa OS separates memory, reasoning, and human judgment into three isolated boundaries:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           1. INGESTION LAYER                             │
│   Telegram Mobile App ──> 8s Debouncer ──> Local Air-Gapped Disk Ingest  │
└─────────────────────────────────────┬────────────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                      2. DB-FIRST MEMORY CORE (SQLite)                     │
│   raw_captures (FTS5 Search) ──> vec_otas (Vector Store) ──> Resonance   │
└─────────────────────────────────────┬────────────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       3. PLUGGABLE REASONING ENGINE                      │
│   AntigravityBackend (Gemini Flash) ──[Fallback]──> Local Rule Heuristics │
└─────────────────────────────────────┬────────────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       4. HUMAN JUDGMENT BOUNDARY                         │
│   Telegram Interactive Sparring ──[Rule 1 Confirmation]──> Published OTA │
└─────────────────────────────────────┬────────────────────────────────────┘
                                      ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                   5. ACCOUNTABILITY & EVALS DASHBOARD                    │
│   24h/3d/7d Schedule ──> Track A Regression ──> Local Glassmorphism UI   │
└──────────────────────────────────────────────────────────────────────────┘
```

### The Three Core Axioms:
- **Memory belongs to the repository**: High-speed, local SQLite (`nirixa.db`) with `sqlite-vec` vector similarity and FTS5 full-text indexing.
- **Reasoning belongs to the AI**: Pluggable reasoning dispatcher with automatic fallback to local deterministic heuristics on rate limits.
- **Judgment belongs to the human**: AI outputs are strictly staged as `status='draft'` until explicitly approved by the human operator.

---

## 🧠 The 3-Layer Local Memory Core

Unlike generic RAG implementations that flood context windows with noisy vector chunks, Nirixa OS utilizes a **deterministic 3-layer memory retrieval engine** operating in sub-milliseconds:

```
                       INCOMING INQUIRY / NOTE
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
[Layer 1: FTS5]          [Layer 2: Resonance]        [Layer 3: Graph Edges]
Exact Lexical Search     3-Signal Vector Math        Associative Traversal
(BM25 Inverted Index)    (Embedding + Time Decay)    (ota_edges >= 0.85)
```

1. **Layer 1: Sub-Millisecond Exact Search (SQLite FTS5)**: Fast BM25 lexical search for exact entity and keyword retrieval ($< 1\text{ms}$).
2. **Layer 2: The 3-Signal Mathematical Resonance Model**:
   $$\text{Resonance} = \underbrace{w_s \cdot \text{Vector Similarity}}_{\text{Semantic Meaning (60\%)}} + \underbrace{w_r \cdot e^{-\lambda t}}_{\text{Time Decay (20\%)}} + \underbrace{w_d \cdot \text{Domain Overlap}}_{\text{Context Alignment (20\%)}}$$
3. **Layer 3: Associative Graph Traversal (`ota_edges`)**: Subconscious bridge linking related cognitive assets across months and years when resonance surpasses $0.85$.

---

## 🏢 Enterprise & Team Deployment (Institutional Memory)

Nirixa OS scales beyond individual productivity into **Enterprise Cognitive Infrastructure**:

- **Institutional Knowledge Retention**: Captures friction, architectural decisions, and post-mortems locally across teams, eliminating tribal knowledge loss when engineers transition.
- **Decentralized Multi-Agent Coordination**: Eliminates fragile daisy-chained cloud agents by providing deterministic, single-boundary memory stores for distributed product teams.
- **Zero Data Leakage**: Runs 100% air-gapped on private VPCs or on-premise hardware without shipping confidential enterprise PRDs to third-party vector clouds.
- **Cross-Domain Collision Detection**: Automated background heuristics detect scheduling collisions, competing milestone timelines, and PRD conflicts across departments.

---

## ⚡ Quickstart (Under 2 Minutes)

### 1. Prerequisites
- Python 3.10 or higher
- A free Telegram Bot Token (from [@BotFather](https://t.me/BotFather))
- A free Google Gemini API Key (from [Google AI Studio](https://aistudio.google.com/))

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/Monish-Nallagondalla/Nirixa.git
cd Nirixa

# Install dependencies
pip install -r requirements.txt
```

### 3. Initialize Nirixa OS
Run the automated one-command setup utility:
```bash
python system/scripts/setup.py
```

### 4. Configure Credentials
Copy `.env.example` to `.env` and fill in your keys:
```env
TELEGRAM_BOT_TOKEN="your_bot_token"
TELEGRAM_AUTHORIZED_CHAT_ID="your_chat_id"
GEMINI_API_KEY="your_gemini_api_key"
```

### 5. Start the Engine & Telemetry Dashboard
```bash
# Terminal 1: Launch the event-driven mobile daemon
python system/scripts/telegram_daemon.py

# Terminal 2: Launch the local telemetry dashboard
python dashboard/dashboard_server.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser to view your live telemetry!

---

## 🧩 Core Subsystems

| Subsystem | File Location | Purpose & Mechanics |
| :--- | :--- | :--- |
| **Event Ingestion Daemon** | `system/engine/daemon.py` | Long-polling Telegram daemon with an 8s debouncer that buffers fragmented mobile bursts into unified sparring sessions. |
| **DB-First Memory Core** | `system/engine/db.py` | SQLite schema hosting `raw_captures`, `otas`, `vec_otas`, `user_profile`, and full-text FTS5 search tables. |
| **Reasoning Dispatcher** | `system/engine/reasoning_backend.py` | High-speed generative AI integration with instant, offline local heuristic fallback. |
| **Chief of Staff Engine** | `system/engine/chief_of_staff.py` | Cross-domain context synthesis, schedule collision detection, and morning/evening briefings. |
| **Thought Resonance Engine** | `system/engine/resonance.py` | 3-signal similarity algorithm ($0.6 \text{ cosine} + 0.2 \text{ recency} + 0.2 \text{ domain}$) with 90-day decay. |
| **Accountability Engine** | `system/engine/accountability.py` | Scans stale drafts ($>3\text{d}$), past-due tasks, and triggers automated 24h, Day 3, and Day 7 follow-ups. |
| **AI News Radar Agent** | `system/engine/ai_news_radar.py` | Autonomous agent scanning arXiv AI preprints and compiling zero-hype LinkedIn thought leadership. |

---

## 📊 Evaluations & Quality Telemetry

Nirixa OS includes a production-grade **3-Track Evaluation Framework**:

```bash
# Run the automated Track A health regression suite
python system/engine/evals/run_system_evals.py
```

- **Track A (Regression Suite)**: 9 automated system health checks evaluating daemon heartbeat, pipeline ingestion, reasoning fallback, Rule 7 copywriting compliance, and air-gap security.
- **Track B (Capability Evolver)**: Time-series snapshots tracking skill growth, rule expansion, and database schema counts over time.
- **Track C (Personal Growth)**: Monthly self-assessments and engagement proxy metrics stored directly in SQLite.

---

## 🛠️ Configuration Guide (`config.yaml`)

Customize system behavior via `system/config/config.yaml`:

```yaml
system:
  name: "Nirixa OS"
  version: "0.2.0"

delegator:
  daily_cap: 4              # Maximum mobile pushes per day
  debounce_seconds: 8       # Mobile text burst buffer window

resonance:
  weight_similarity: 0.6    # Cosine vector similarity weight
  weight_recency: 0.2       # Time-decay freshness weight
  weight_domain: 0.2        # Cross-domain alignment weight
  threshold_edge: 0.85      # Minimum score to create an ota_edges connection
  decay_half_life_days: 90  # Exponential decay rate

accountability:
  stale_draft_days: 3       # Days before an unreviewed draft is flagged
```

---

## 📁 Repository Directory Tour

```
Nirixa/
├── .agents/                    # Reusable agent skills and evaluation rules
├── dashboard/                  # Local read-only HTTP server & glassmorphism UI
│   ├── dashboard_server.py     # Python HTTP server (Port 8000)
│   └── index.html              # Dark glassmorphism dashboard layout
├── docs/                       # Architectural PRDs, playbooks, and specifications
├── system/
│   ├── config/                 # System configuration templates
│   ├── engine/                 # Nirixa Core Engine
│   │   ├── daemon.py           # Telegram long-polling daemon & debouncer
│   │   ├── db.py               # SQLite DB-first memory core & FTS5 search
│   │   ├── reasoning_backend.py# Pluggable reasoning dispatcher & local fallback
│   │   ├── chief_of_staff.py   # Cross-domain synthesis & briefing engine
│   │   ├── resonance.py        # Vector embeddings & 3-signal resonance math
│   │   ├── accountability.py   # Staleness scanner & 3-stage touchpoint schedule
│   │   ├── ai_news_radar.py    # Autonomous AI news collector & post generator
│   │   └── evals/              # 3-Track evaluation regression harness
│   └── scripts/                # Automated setup & utility scripts
├── .env.example                # Environment variables template
├── CONTRIBUTING.md             # Developer contribution guidelines
├── LICENSE                     # MIT Open-Source License
└── README.md                   # Flagship showcase documentation
```

---

## 🎯 Custom Goals, Milestones & Persona Extensibility

Nirixa OS is designed to be completely user-programmable. You can define your own **life milestones**, **custom persona boards**, and **original thought assets (OTAs)** without writing complex boilerplate:

- **Custom Life Milestones**: Track long-term horizons (e.g. Keynote Talks, Book Releases, Research Labs) in SQLite via Python API or Dashboard.
- **Custom Persona Advisory Board**: Add custom simulated mentors (e.g. Paul Graham, Jensen Huang, Sam Altman) in `.agents/skills/persona-advisory-board/`.
- **Original Thought Assets (OTAs)**: Register custom foundational hypotheses and lineage trees.

👉 **Read the complete guide**: **[docs/CUSTOM_GOALS_AND_EXTENSIONS.md](docs/CUSTOM_GOALS_AND_EXTENSIONS.md)**

---

## 🤝 Contributing

We welcome contributions from system architects, AI engineers, and builders! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines, testing protocols, and PR workflows.

---

## 📄 License

Nirixa OS is open-source software licensed under the [MIT License](LICENSE).