# 📘 The My-OS Master Manual & Operating Playbook
### The Unified System Manual for Monish Nallagondalla Srinath & Nirixa OS

---

## 🧭 I. The Foundational Vision

> **"You are not building software. You are building a framework for understanding intelligence."**
> 
> My-OS is your private cognitive laboratory. Nirixa is the interface. The book is the communication. LinkedIn is the public experimentation lab. Your career is the empirical data. All compound toward your **Global Keynote / TED Talk before Age 33 (2029)** and an independent AI Research Institute.

---

## 📁 II. Repository Directory Manual & Folder Anatomy

```
My-Os/
├── docs/                               # 🏛️ Master Strategic & Epistemological Blueprints
│   ├── THE_QUESTION_PROJECT_UNIFIED_CONSTITUTION.md # The 34 Pillars & 10 Frontier Inquiries
│   ├── THE_QUESTION_PROJECT_COMPLETE_RESEARCH_CONTEXT.md # In-depth research context & hypothesis
│   ├── MASTER_OTA_REGISTRY.md          # Complete taxonomy of OTA-001 through OTA-015 + Seeds
│   ├── CUSTOM_GOALS_AND_EXTENSIONS.md  # Guide on defining custom goals & persona advisors
│   ├── CAREER_DASHBOARD.md             # Inbound opportunities, milestones & speaking tracks
│   └── PLAYBOOK.md                     # This master system manual
│
├── personal/                           # 🔒 Private & Air-Gapped Personal Knowledge
│   ├── USER_PROFILE.md                 # Age, demographics, family, finances & vehicle telemetry
│   └── PROFILE_README.md               # Master profile summary & verified credentials
│
├── inbox/                              # 📥 Friction Capture & Monthly Thinking Streams
│   ├── YYYY-MM-mobile-inbox.md         # Consolidated monthly stream of processed reflections
│   └── README.md                       # Stream architecture explanation
│
├── system/                             # ⚙️ Core Engine & Subsystems
│   ├── data/
│   │   ├── nirixa.db                   # SQLite memory store (FTS5 search, OTAs, milestones)
│   │   └── synced_messages.json        # 7-day rolling Telegram message retention
│   ├── engine/
│   │   ├── daemon.py                   # Telegram long-polling daemon & 8s debouncer
│   │   ├── chief_of_staff.py           # Context-adaptive Socratic reasoning & OTA connector
│   │   ├── synthesizer.py              # LLM-Wiki auto-clustering & 4-part extraction
│   │   ├── resonance.py                # 3-signal vector resonance math
│   │   ├── ai_news_radar.py            # $0 multi-source autonomous tech radar
│   │   └── evals/                      # 3-Track evaluation regression harness
│   ├── scripts/                        # Automated startup, Wi-Fi recovery & utility scripts
│   └── config/                         # System configuration & environment variables
│
├── dashboard/                          # 🖥️ Local-First Control Center (Port 8000)
│   ├── dashboard_server.py             # Python HTTP server with Control Center action APIs
│   └── index.html                      # Glowing dark glassmorphism layout & telemetry
│
├── .agents/                            # 🤖 Agent Rules & Cognitive Skills
│   ├── AGENTS.md                       # Master workspace rules & Rule 9 Epistemological Standard
│   └── skills/                         # Specialized capabilities:
│       ├── persona-advisory-board/     # Marty Cagan, David Goggins, Paramahansa Yogananda
│       ├── content-stylist/            # Naval & Aviral high-signal minimalist copywriting
│       ├── mobile-sync/                # 3-Stage Telegram friction sync
│       ├── omni-channel-publisher/     # Platform-native PDF carousel & X validator
│       └── calendar-scheduler/         # Google Calendar task & milestone scheduling
│
├── nirixa-open-source/                 # 🌐 Public, Generic & 100% Air-Gapped Framework Repo
│   ├── docs/                           # Generic architecture specs & extensibility guides
│   ├── system/                         # Reusable core engine code (zero private data)
│   └── README.md                       # Flagship open-source documentation
│
└── start_os.bat                        # 🚀 1-Click Master Launcher (Daemon + Dashboard)
```

---

## ⚡ III. The 3-Stage Processing Pipeline

```
[Mobile Friction on Telegram]
             │
             ▼ (8s Debouncer Buffer)
[Chief of Staff Interactive Sparring]
             │ (Context-Adaptive Socratic Debate)
             ▼
[Refined Crystallization] ───► Stored in inbox/YYYY-MM-mobile-inbox.md
                          ───► Linked to OTA in docs/MASTER_OTA_REGISTRY.md
                          ───► Mapped to LinkedIn Content Calendar
```

1. **Stage 1 (Buffer)**: Raw voice notes and rapid thoughts sent via Telegram are held in an 8-second debounce buffer to prevent fragmented spam.
2. **Stage 2 (Sparring & Socratic Debate)**: When `sync` runs, the Chief of Staff does not autocomplete. It challenges unstated premises, tests edge cases, and demands authentic scars.
3. **Stage 3 (Refined Save)**: Only the refined entry ($\text{Context} + \text{Thesis} + \text{Scars} + \text{OTA Link}$) is saved to permanent storage.

---

## 🧠 IV. Context-Adaptive Sparring Protocols

| Domain / Topic | Agent Sparring Behavior | Output Goal |
| :--- | :--- | :--- |
| **Philosophical & Systems Ideas** | **Active Socratic Debate**: Challenges assumptions, searches for counter-evidence, probes for unstated premises (`OTA-010`). | Maps inquiry to **OTA-001 through OTA-015** or the 10 Frontier Domains. |
| **Work & Consulting Friction (EY)** | **Architectural Extraction**: Probes for real-world scars, organizational dynamics, and enterprise lessons with **strict PII anonymization**. | Crystallizes reusable frameworks and LinkedIn hypothesis experiments. |
| **Technical & Code Tasks** | **Deterministic Precision**: Pure, zero-fluff, deterministic code execution with 100% regression verification. | Working code, passing tests, and updated system artifacts. |

---

## 💎 V. The OTA (Original Thought Asset) Life-Cycle

Every original insight compounds as an asset through this traceable lineage (`OTA-011`):

$$\text{Real-World Friction / Podcast} \longrightarrow \text{Open Question} \longrightarrow \text{Original Thought Asset (OTA)} \longrightarrow \text{LinkedIn Hypothesis Test} \longrightarrow \text{Book Chapter / Keynote}$$

- **An OTA is never finished when written down.** It evolves over years as new evidence accumulates.
- **Questions as First-Class Objects**: Questions are stored with their counterarguments, research threads, and related inquiries in `nirixa.db`.

---

## 🔒 VI. The Strict Air-Gap Privacy Standard

- **Private Workspace (`My-Os`)**: Contains your real name, family demographics, salary details, client notes, and local database.
- **Public Framework (`nirixa-open-source`)**: 100% generic, containing zero personal names, zero private notes, zero resumes, and zero proprietary data.

---

## 🚀 VII. Quick Operation Commands

- **Launch Everything**: Double-click `start_os.bat` on Desktop or workspace root.
- **Access Dashboard**: Open `http://localhost:8000` in any browser.
- **Run Tech Radar**: Click **Scan AI Radar** on Dashboard or run `python system/engine/ai_news_radar.py`.
- **Run System Regression**: Run `python system/engine/evals/run_system_evals.py` (Must score 100%).
- **Recover Wi-Fi**: Double-click `system/scripts/reset_wifi.bat`.
