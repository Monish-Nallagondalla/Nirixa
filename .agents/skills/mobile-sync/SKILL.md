---
name: mobile-sync
description: Sync thoughts captured on Telegram into My-OS monthly stream log (inbox/YYYY-MM-mobile-inbox.md), apply anonymization rules, and push to GitHub repository.
---

# Mobile Sync Skill (`mobile-sync`)

Use this skill whenever the user says "sync", "run sync", "check telegram", or wants to pull raw mobile thoughts into `My-OS`.

## Instructions

1. **Execute Local Sync or Start Real-Time Daemon**:
   - **Manual Batch Sync**:
     ```bash
     python system/scripts/sync.py
     ```
   - **Real-Time Bidirectional Daemon (Laptop Active)**:
     ```bash
     python system/scripts/telegram_daemon.py
     # Or launch via system/scripts/start_telegram_daemon.bat
     ```

2. **Monthly Stream Architecture**:
   All raw thoughts captured from Telegram are appended to a single, token-optimized monthly log file: `inbox/YYYY-MM-mobile-inbox.md`.

3. **Verify Anonymization**:
   Check the monthly log file to ensure company names (e.g. EY, client names) were anonymized into abstract terminology according to `system/config/config.yaml`.

4. **Git Backup Status**:
   Confirm that `git commit` and `git push` succeeded to keep the private GitHub repository up-to-date.

5. **Consolidate & Do Not Proliferate Files**:
   - **Strict Rule**: NEVER create standalone, single-thought markdown files for raw captures.
   - All raw mobile captures append ONLY to `inbox/YYYY-MM-mobile-inbox.md`.
   - Organize long-term workspace content using the **PARA framework**:
     - `projects/`: Active goal-driven projects.
     - `areas/`: Permanent responsibilities (finance, career, writing, system).
     - `resources/`: Knowledge hubs & reference standards.
     - `archive/`: Inactive historical items.
   - When mapping ideas into production, update existing central hubs (e.g., `content/linkedin/august-2026-content-calendar.md` or `docs/PLAYBOOK.md`) rather than spawning new files.

6. **Clarity Max Interactive Sparring**:
   - For major raw thoughts, ask 2–3 targeted clarifying questions to extract authentic scars and evidence before drafting.
   - Follow the mandatory 4-step post drafting protocol from `docs/PLAYBOOK.md` (Gist → To-and-Fro Sparring → Refine → Final Draft).
