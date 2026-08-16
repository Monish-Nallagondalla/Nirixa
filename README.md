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

# Nirixa OS
<p align="center">
  <a href="https://github.com/Monish-Nallagondalla/Nirixa">Nirixa OS</a> | <a href="docs/getting-started/QUICKSTART.md">Getting Started</a> | <a href="docs/guides/LEADER_BLUEPRINT.md">Daily Blueprint</a> | <a href="docs/README.md">Documentation Hub</a>
</p>
<p align="center">
  <a href="docs/README.md"><img src="https://img.shields.io/badge/Docs-Documentation_Hub-FFD700?style=for-the-badge" alt="Documentation"></a>
  <a href="https://github.com/Monish-Nallagondalla/Nirixa/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Storage-SQLite_Core-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/Telegram-Connected-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/badge/Agents-Antigravity_%7C_Cursor_%7C_Claude-blueviolet?style=for-the-badge" alt="Agents">
</p>

**The autonomous 24/7 AI Chief of Staff and Company Living Wiki.** An agentic operating system with a closed learning loop — it captures raw voice and text friction on mobile, debates and spars on assumptions via Socratic reasoning, persists structured knowledge in an ACID SQLite core, and auto-compiles authentic lessons into living engineering playbooks, decision records, and public assets. Run it locally, on an Oracle Always-Free VPS, or alongside your coding agent in Google Antigravity, Cursor, and Claude Code. It is not tied to your IDE — talk to it from Telegram while it manages your memory, telemetry, and execution.

Use any model you want — Gemini Flash, Claude, OpenAI, or local open weights. Switch via configuration with zero code changes and zero lock-in.

<table>
<tr><td width="30%"><b>A real mobile and terminal gateway</b></td><td>Zero-friction Telegram text and voice capture, interactive inline buttons, 1-click approvals, and bidirectional IDE execution with zero latency.</td></tr>
<tr><td><b>Dual operating modes</b></td><td><b>Mode A (Personal Chief of Staff)</b>: 4-Quadrant Compass (Mission, Mastery, Money, Mind) and 3-Horizon Execution Engine.<br/><b>Mode B (Company Living Wiki)</b>: Living Engineering Playbook, Post-Mortem Scars Vault, and automated async standup dependency radar.</td></tr>
<tr><td><b>A closed Socratic learning loop</b></td><td>The AI does not flatter or autocomplete. It probes unstated premises, extracts authentic architectural scars, and evolves living Original Thought Assets (OTAs) that compound over time.</td></tr>
<tr><td><b>Zero-LLM deterministic fast path</b></td><td>Hardware telemetry, regex reminders, time-wheel briefings, and status checks run 100% deterministically at zero token cost.</td></tr>
<tr><td><b>DB-first SQLite memory core</b></td><td>Single ACID SQLite database (<code>system/data/nirixa.db</code>) with vector embeddings (sqlite-vec) and FTS5 search. Zero unorganized markdown file proliferation. Full thought ancestry and lineage tracking.</td></tr>
<tr><td><b>Universal coding agent onboarding</b></td><td>Interactive Inform -&gt; Confirm -&gt; Build interview protocol across Google Antigravity, Cursor (<code>.cursorrules</code>), and Claude Code (<code>CLAUDE.md</code>).</td></tr>
<tr><td><b>Progressive enlightenment ladder</b></td><td>30-Day cognitive adoption curve: Day 1 (Zero-effort mobile utility) -&gt; Day 7 (Socratic reflection and pattern detection) -&gt; Day 30 (Custom agent skills and self-evolving playbooks).</td></tr>
</table>

---

## Quick Install

### Linux, macOS, WSL2

```bash
git clone https://github.com/Monish-Nallagondalla/Nirixa.git
cd Nirixa
cp system/config/.env.example system/config/.env
pip install -r requirements.txt
```

### Windows (PowerShell)

```powershell
git clone https://github.com/Monish-Nallagondalla/Nirixa.git
cd Nirixa
Copy-Item system/config/.env.example system/config/.env
pip install -r requirements.txt
```

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

## Getting Started

```bash
python system/scripts/telegram_listener.py   # Start real-time background mobile listener
python system/scripts/send_status.py         # Dispatch live hardware & OS telemetry dashboard
python system/scripts/sync.py                # Sync mobile inbox & run 7-day chat cleanup
python system/engine/evolver.py             # Run self-evolution audit on feedback ratios
python system/engine/evals/run_system_evals.py # Run deterministic system evaluation suite
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