<p align="center">
<pre align="center">
 ███╗   ██╗██╗██████╗ ██╗██╗  ██╗ █████╗        ██████╗ ███████╗
 ████╗  ██║██║██╔══██╗██║╚██╗██╔╝██╔══██╗      ██╔═══██╗██╔════╝
 ██╔██╗ ██║██║██████╔╝██║ ╚███╔╝ ███████║█████╗██║   ██║███████╗
 ██║╚██╗██║██║██╔══██╗██║ ██╔██╗ ██╔══██║╚════╝██║   ██║╚════██║
 ██║ ╚████║██║██║  ██║██║██╔╝ ██╗██║  ██║      ╚██████╔╝███████║
 ╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝       ╚═════╝ ╚══════╝
</pre>
</p>

# Nirixa OS & Episteme Cockpit
<p align="center">
  <a href="https://github.com/Monish-Nallagondalla/Nirixa">Nirixa OS</a> | <a href="docs/architecture/EPISTEME_OS_PRD.md">Episteme PRD</a> | <a href="docs/getting-started/QUICKSTART.md">Getting Started</a> | <a href="docs/guides/LEADER_BLUEPRINT.md">Daily Blueprint</a> | <a href="docs/README.md">Documentation Hub</a>
</p>
<p align="center">
  <a href="docs/architecture/EPISTEME_OS_PRD.md"><img src="https://img.shields.io/badge/PRD-Episteme_OS_Spec-C89B53?style=for-the-badge" alt="PRD Spec"></a>
  <a href="docs/README.md"><img src="https://img.shields.io/badge/Docs-Documentation_Hub-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://github.com/Monish-Nallagondalla/Nirixa/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Next.js-16.3-black?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js">
  <img src="https://img.shields.io/badge/Storage-SQLite_Core-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Telegram-Connected-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
</p>

**The autonomous cognitive operating system, full-stack Episteme cockpit, and AI coevolution partner.** Nirixa combines an Awwwards-caliber Monastic Obsidian web cockpit (`http://localhost:3000`) with a 24/7 background Telegram daemon. It captures raw friction, preserves non-destructive belief evolutions, challenges unstated premises via Socratic sparring, and auto-compiles authentic lessons into research assets, decision records, and public frameworks.

Built on an ACID SQLite core (`system/data/nirixa.db`) with zero lock-in, universal coding agent support (Google Antigravity, Cursor, Claude Code), and a 100% deterministic test suite verifying PRD dialectic invariants.

---

## The 7 Epistemic Engine Surfaces

Nirixa Episteme OS is built around 7 interconnected intellectual surfaces:

1. **Cockpit Bento & Dynamic Stream Spotlight**: Monastic 4-segment switcher (*PhD Research, Leadership Authority, Enterprise Architecture, Personal Mastery*) with real-time radial telemetry gauges, book chapter maturity trackers, and capture triage queues.
2. **Evolution Timeline**: Non-destructive belief mutation tracker. Every premise revision ($v1.0 \rightarrow v1.1 \rightarrow v2.0$) preserves its complete provenance hash, evidence anchor, and visual diff.
3. **Challenges Deck**: Socratic adversarial debate arena. Spars against Socratic, Empirical, and First-Principles personas to defend core premises and track epistemic conviction.
4. **Discoveries Deck**: Unprompted AI discovery surface. Autonomously detects latent patterns across orphan captures and allows 1-click canonization into book chapters.
5. **Jarvis Command Modal (`Cmd+K` / `Ctrl+K`)**: Global cognitive command dispatcher for natural language synthesis, lineage tracing, premise challenges, and instant navigation.
6. **Writing Studio**: Editorial canvas with Newsreader typography, distraction-free drafting, deep-linked Original Thought Asset (OTA) lineage sidebars, and paper citations.
7. **Orbit Graph**: Interactive D3 knowledge topology visualizing living computational question primitives, PageRank authority scores, and bidirectional lineage trees.

---

<table>
<tr><td width="30%"><b>Full-Stack Episteme Web Cockpit</b></td><td>Awwwards-caliber Monastic Obsidian &amp; Warm Tungsten design system (Next.js 16 + Tailwind) running locally on Port 3000 with real-time SQLite telemetry.</td></tr>
<tr><td><b>Mobile Telegram Gateway</b></td><td>Zero-friction Telegram text and voice capture, interactive inline buttons, 1-click approvals, and bidirectional IDE execution with zero latency.</td></tr>
<tr><td><b>Non-Destructive Belief Evolution</b></td><td>Beliefs and premises are never overwritten. Every mutation records its trigger, rationale, timestamp, and visual diff.</td></tr>
<tr><td><b>Socratic Sparring &amp; Premise Defense</b></td><td>The AI does not flatter or autocomplete. It probes unstated premises, tests edge cases, and calculates conviction scores.</td></tr>
<tr><td><b>DB-First SQLite Core</b></td><td>Single ACID SQLite database with vector embeddings and FTS5 search. Full thought ancestry and lineage tracking.</td></tr>
<tr><td><b>Verified PRD Invariants</b></td><td>10 / 10 automated test scenarios (<code>npm test</code>) verifying zero-loss triage, unprompted discovery, and longitudinal self-inquiry.</td></tr>
</table>

---

## Quick Install

### 1-Click Unified Launch (Windows)

Simply double-click or run:
```powershell
.\start_os.bat
```
This automatically boots the Next.js Episteme Cockpit on `http://localhost:3000` and starts the silent background Telegram listener daemon.

---

### Manual Setup (Linux, macOS, WSL2, Windows)

```bash
git clone https://github.com/Monish-Nallagondalla/Nirixa.git
cd Nirixa

# 1. Python Environment & Listener
cp system/config/.env.example system/config/.env
pip install -r requirements.txt

# 2. Episteme OS Next.js Cockpit
cd apps/episteme
npm install
npm run dev
```
Open **`http://localhost:3000`** in your browser to enter the Monastic Episteme Cockpit.

---

### Running the PRD Dialectic Invariants Test Suite

Verify all 10 dialectic scenarios (zero-loss triage, belief mutations, unprompted discovery, and longitudinal self-inquiry):

```bash
cd apps/episteme
npm test
```

---

### Connecting Your Telegram Gateway (2 Minutes)

1. Open Telegram, search for `@BotFather`, send `/newbot`, and copy your **API Token**.
2. Search for `@userinfobot`, click Start, and copy your numerical **Chat ID**.
3. Add both to `system/config/.env`:
   ```env
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```
4. Start the listener:
   ```bash
   python system/scripts/telegram_listener.py
   ```

[Read the Full Quickstart Guide](docs/getting-started/QUICKSTART.md)

---

## Operating Commands Quick Reference

```bash
.\start_os.bat                               # Unified 1-click stack (Web Cockpit + Telegram daemon)
python system/scripts/telegram_listener.py   # Start real-time background mobile listener
python system/scripts/send_status.py         # Dispatch live hardware & OS telemetry dashboard
python system/scripts/sync.py                # Sync mobile inbox & run 7-day chat cleanup
npm test (in apps/episteme)                  # Run 10 PRD scenario dialectic invariant tests
```

Full documentation is available in the **[Documentation Hub](docs/README.md)**.

---

## Universal Coding Agent Integration

When you clone Nirixa OS and open it in your preferred IDE, your coding agent immediately guides you through the 3-minute setup interview:

* **Google Antigravity**: Automatically loads `.agents/skills/user-onboarding/` and workspace rules.
* **Cursor**: Automatically reads `.cursorrules`.
* **Claude Code**: Automatically reads `CLAUDE.md`.

[Read the Full Onboarding Protocol](docs/getting-started/ONBOARDING_PROTOCOL.md)

---

## CLI vs Messaging Quick Reference

Nirixa OS operates across two synchronized interfaces: the local IDE/CLI runtime and the Telegram mobile gateway.

| Action | Local CLI / IDE | Telegram Mobile Gateway |
| :--- | :--- | :--- |
| Capture thought or friction | Save to `inbox/` or speak in IDE chat | Send text or 10-second voice note |
| Hardware & DB telemetry | `python system/scripts/send_status.py` | Tap `[ System Status ]` button |
| Socratic sparring | Interactive chat pairing in Antigravity | Real-time Socratic thesis pushback |
| Check reminders | Query `reminders` table in `nirixa.db` | Tap `[ Check Reminders ]` button |
| Put host machine to sleep | Trigger sleep script | Tap `[ Put Laptop to Sleep ]` button |
| Compile public assets | Run publisher script | Tap `[ Auto-Compile Assets ]` button |

---

## Dual Operating Frameworks

```
┌───────────────────────────────────────────────┬───────────────────────────────────────────────┐
│     MODE A: PERSONAL CHIEF OF STAFF           │     MODE B: COMPANY LIVING WIKI & PLAYBOOK    │
├───────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ - Mission (Career, Products, Outputs)         │ - Company Vision, Values & Strategic Moat     │
│ - Mastery (Deep Inquiry, Books, Research)     │ - Living Engineering Standards & PR Rules     │
│ - Money (Revenue, Assets, Freedom)            │ - Post-Mortem Scars Vault (Outage Invariants) │
│ - Mind (Health, Clarity, Vitality)            │ - Async Standup & Dependency Blocker Radar    │
│                                               │                                               │
│ [docs/frameworks/PERSONAL_COMPASS.md]         │ [docs/company/README.md]                      │
└───────────────────────────────────────────────┴───────────────────────────────────────────────┘
```

---

## Operating Blueprint: Daily Cycle

A complete 24-hour walkthrough demonstrating an AI Tech Lead operating Nirixa OS:
* **09:00 AM**: Deterministic Morning Executive Briefing on Telegram.
* **02:30 PM**: `[MISSION]` Voice note capture on distributed system deadlocks.
* **06:00 PM**: `[MASTERY]` Socratic sparring on deterministic state machines vs LLM drift.
* **08:30 PM**: `[MIND]` Health and evening equilibrium tracking.
* **Sunday Review**: 1-Click auto-compilation of scars into LinkedIn visual documents and technical RFCs.

Full blueprint: **[docs/guides/LEADER_BLUEPRINT.md](docs/guides/LEADER_BLUEPRINT.md)**

---

## Progressive Enlightenment Model

You do not need to understand complex architecture on Day 1. Nirixa OS guides you through a 30-day cognitive adoption journey:

```
  ┌─────────────────────────┐
  │   DAY 1: UTILITY        │  -> 2-Min Telegram setup. Send voice notes, get reminders & briefings.
  └───────────┬─────────────┘
              │
              ▼
  ┌─────────────────────────┐
  │   DAY 7: REFLECTION     │  -> AI surfaces recurring friction. First Socratic sparring on phone.
  └───────────┬─────────────┘
              │
              ▼
  ┌─────────────────────────┐
  │   DAY 30: COMPOUNDING   │  -> Auto-compiles public assets/playbooks. Teaches custom skills.
  └─────────────────────────┘
```

Full details: **[docs/getting-started/PROGRESSIVE_ENLIGHTENMENT.md](docs/getting-started/PROGRESSIVE_ENLIGHTENMENT.md)**

---

## Architecture

```mermaid
graph TD
    User["User / Team (Mobile & IDE Gateway)"] -->|"Voice / Text Note"| Daemon["Runtime Daemon (Zero-LLM Fast Path)"]
    Daemon -->|"Classify & Store"| DB[("SQLite Core (nirixa.db)")]
    DB --> OperatingMode{"Operating Mode Engine"}
    OperatingMode -->|"Personal Mode"| Q["4-Quadrant / 3-Horizon Framework"]
    OperatingMode -->|"Company Mode"| W["Living Engineering Playbook & Scars"]
    Q & W --> Compounding["Compounding Engine<br/>(Visual Documents, RFCs, Post-Mortems)"]
    Compounding --> Proactive["Proactive Briefings & Blocker Alerts"]
    Proactive --> User
```

---

## Documentation Index

| Section | Link | What is Covered |
| :--- | :--- | :--- |
| **Getting Started** | [Quickstart](docs/getting-started/QUICKSTART.md) | Install -> setup -> first mobile capture in 2 minutes |
| **Onboarding** | [Onboarding Protocol](docs/getting-started/ONBOARDING_PROTOCOL.md) | Universal agent setup across Antigravity, Cursor, and Claude Code |
| **Adoption** | [Progressive Enlightenment](docs/getting-started/PROGRESSIVE_ENLIGHTENMENT.md) | 30-Day cognitive adoption ladder |
| **Frameworks** | [Personal Compass](docs/frameworks/PERSONAL_COMPASS.md) | 4-Quadrant holistic balance model (Mission, Mastery, Money, Mind) |
| **Execution** | [3-Horizon Engine](docs/frameworks/HORIZON_ENGINE.md) | 3-Horizon execution framework (North Star -> Friction -> Sprint) |
| **Epistemology** | [Original Thought Assets](docs/frameworks/ORIGINAL_THOUGHT_ASSETS.md) | The 15 Core OTAs, question objects, and thought lineage |
| **Daily Blueprint**| [Operating Blueprint](docs/guides/LEADER_BLUEPRINT.md) | 24-Hour operating cycle of an AI Tech Lead |
| **Mobile Gateway** | [Telegram Gateway Guide](docs/guides/TELEGRAM_GATEWAY.md) | Voice notes, telemetry, callbacks, and remote sleep control |
| **Custom Skills**  | [Creating Custom Skills](docs/guides/CREATING_CUSTOM_SKILLS.md) | Building specialized domain skills, habits, and drills |
| **24/7 Cloud**     | [Oracle Cloud VPS Guide](docs/guides/ORACLE_CLOUD_DEPLOYMENT.md) | Running 24/7 on Oracle Always-Free Compute with systemd |
| **Company Wiki**   | [Company Wiki Hub](docs/company/README.md) | Team operating system, living playbooks, and async standups |
| **Architecture**   | [System Architecture](docs/reference/ARCHITECTURE.md) | SQLite Core, Zero-LLM Fast Path, and Socratic engine |
| **CLI Reference**  | [CLI Playbook](docs/reference/CLI_PLAYBOOK.md) | Complete CLI commands and daemon scripts reference |
| **Configuration**  | [Configuration Reference](docs/reference/CONFIGURATION.md) | Complete `.env` variables and model providers reference |

---

## License

MIT — see [LICENSE](LICENSE).