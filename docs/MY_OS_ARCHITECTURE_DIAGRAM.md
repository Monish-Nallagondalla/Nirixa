# My-OS v0.2 - Master Architecture Diagram (Refined & Verified)

**Purpose**: High-density architectural diagram formatted in GFM Mermaid syntax for structural review, capability auditing, and feedback by external LLMs (Claude 3.5 Sonnet / Claude Opus).

---

## Complete End-to-End System Architecture

```mermaid
flowchart TD
    %% 1. Ingestion Layer (Local-Only Air-Gap Boundary)
    subgraph INGESTION["1. Ingestion & Air-Gap Local Stream"]
        TG["Telegram Mobile App"] -->|Raw Voice/Text Note| DAEMON["daemon.py (Event-Driven Telegram Daemon)"]
        DAEMON -->|8s Debounce Buffer| DEBOUNCE["Debouncer Stream"]
        DAEMON -->|Zero-Delay Local Append| INBOX["inbox/YYYY-MM-mobile-inbox.md (Local Only)"]
        DAEMON -->|7-Day Retention| ROLLOVER["synced_messages.json"]
    end

    %% 2. Memory & Storage Core
    subgraph MEMORY["2. DB-First Memory Core (system/data/nirixa.db)"]
        DEBOUNCE -->|Raw Thought Persistence| SQLITE_RAW[("raw_captures Table")]
        SQLITE_RAW --> FTS[("FTS5 Full-Text Search Core")]
    end

    %% 3. Pluggable Reasoning Layer
    subgraph REASONING["3. Pluggable Reasoning & Dispatcher Layer"]
        SQLITE_RAW --> DISPATCHER["ReasoningDispatcher (reasoning_backend.py)"]
        DISPATCHER -->|Direct API Call| AG_BACKEND["AntigravityBackend (Gemini Flash API)"]
        AG_BACKEND -->|API Limit / Error| FALLBACK_LOG["Audit Metric: reasoning_backend_fallback"]
        FALLBACK_LOG --> LOCAL_BACKEND["LocalBackend (Keyword & Rule Heuristics)"]
        
        DISPATCHER --> COS["chief_of_staff.py (Cross-Domain Engine)"]
        COS -->|Cross-Domain Synthesis| CONFLICTS["detect_cross_domain_conflicts()"]
        CONFLICTS -->|Context Injection| DRAFT_STAGING["Draft Staging (status = 'draft')"]
    end

    %% 4. Closed Retrieval Loop & Resonance Store
    subgraph RETRIEVAL["4. Vector Resonance & Closed Retrieval Loop (Phase 3)"]
        PROCESSED_SAVE[("otas Table (status = 'refined' / 'published')")] -->|Refined Thesis Source| VEC[("sqlite-vec Vector Store (vec_otas)")]
        VEC --> RESONANCE["resonance.py (3-Signal Engine)"]
        RESONANCE -->|Score >= 0.85| EDGES[("ota_edges Graph Table")]
        RESONANCE -->|Closed Loop Injection| COS
    end

    %% 5. Human Judgment & Sparring Stage
    subgraph SPARRING["5. Human Judgment & Sparring Stage (Rule 1)"]
        DRAFT_STAGING --> SPARRING_CHAT["Telegram Interactive Sparring"]
        SPARRING_CHAT --> MONISH{"Monish (Human Judgment)"}
        MONISH -->|Reject / Refine| DRAFT_STAGING
        MONISH -->|Explicit Approval| PROCESSED_SAVE
    end

    %% 6. Publishing Mechanics & Air-Gap Git Push
    subgraph PUBLISHING["6. Omni-Channel Publisher & Publish-Time Git Push"]
        PROCESSED_SAVE --> PUBLISHER["omni-channel-publisher"]
        PUBLISHER -->|Rule 7 Emoji Regex Scan| EMOJI_AUDIT["Zero Hype Emoji Filter"]
        PUBLISHER -->|Strict <280 Chars| TWEETS["X.com Thread Auto-Splitter"]
        PUBLISHER -->|Auto PDF Compilation| CAROUSEL["LinkedIn Multi-Slide PDF Builder"]
        
        PROCESSED_SAVE -->|Status -> 'published'| GIT_SYNC["Publish-Time Git Sync (sync.run_git_sync)"]
        GIT_SYNC -->|Air-Gap Export Push| GIT["GitHub Remote Repository"]
    end

    %% 7. Accountability & Nudge Engine
    subgraph ACCOUNTABILITY["7. Staleness & Accountability Engine (accountability.py)"]
        PROCESSED_SAVE -->|Status -> 'published'| ENG_CHECK["Schedule 24h Engagement Follow-Up"]
        ENG_CHECK --> REMINDERS[("reminders Table")]
        
        DAILY_SCAN["run_daily_accountability_audit()"] -->|Scan Drafts > 3d| STALE_DRAFTS["Stale Draft Nudges"]
        DAILY_SCAN -->|Scan Overdue Tasks| OVERDUE_NUDGES["Overdue Task Escalation"]
        
        STALE_DRAFTS --> DELEGATOR["mobile-task-delegator (Daily Cap: 4)"]
        OVERDUE_NUDGES --> DELEGATOR
        DELEGATOR -->|Priority Telegram Push| TG
    end

    %% 8. 3-Track Eval Framework & Dashboard
    subgraph EVALS["8. 3-Track Eval Framework & Local Dashboard"]
        REGRESSION["run_system_evals.py (Track A: 9 Checks)"] -->|Pass/Fail Logging| EVAL_DB[("eval_results Table")]
        EVOLVER["evolver.py (Track B: Capability Snapshots)"] -->|Snapshot Logging| SNAP_DB[("capability_snapshots Table")]
        GROWTH["Track C: Self-Assessments & Proxies"] --> ASSESS_DB[("self_assessments & product_metrics Tables")]
        
        EVAL_DB --> DASH_SERVER["dashboard_server.py (Python Local Server)"]
        SNAP_DB --> DASH_SERVER
        ASSESS_DB --> DASH_SERVER
        DASH_SERVER --> UI["Local Read-Only Dashboard (http://localhost:8000)"]
    end
```

---

## Key Architecture Clarifications

1. **Strict Air-Gap Boundary**: Mobile Telegram raw notes append locally to `inbox/YYYY-MM-mobile-inbox.md`. No auto `git push` occurs on raw capture ingestion. `git commit & push` fires **strictly when an OTA is published**, keeping unsanitized thoughts local.
2. **Refined-Thesis Vector Store**: `vec_otas` is populated **strictly from clean `otas.refined_thesis`** statements, matching refined concepts against each other for Thought Resonance.
3. **Closed Retrieval Loop**: `resonance.get_injected_sparring_context(query_text)` is directly embedded into `chief_of_staff.get_cross_domain_context()`, resurfacing top-K resonant past OTAs into active Telegram sparring prompts.
4. **Programmatic Quality Gates**: `docs/STANDARDS.md` is Monish's human calibration guide. Automated checks in `omni-channel-publisher` gate on testable regex rules (zero hype emojis, 280-char X split).
5. **Direct API Reasoning**: `AntigravityBackend` uses direct Gemini API endpoints for low-latency thesis generation with `reasoning_backend_fallback` metric auditing.
