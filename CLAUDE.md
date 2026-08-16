# Claude Code Agent Instructions for Nirixa OS (My-OS)

## Overview
Nirixa OS is an open-source 24/7 AI Chief of Staff and Company Living Wiki built around local SQLite memory (`nirixa.db`), mobile Telegram capture, and universal coding agent execution.

---

## 🚀 Onboarding Protocol (First Run Detection)
If the workspace is newly cloned or unconfigured, proactively trigger the **Inform ➔ Confirm ➔ Build** onboarding flow:
1. **Inform**: Ask whether they are building a **Personal Chief of Staff** (4-Quadrant Compass or 3-Horizon Engine) or a **Company Living Wiki & Playbook**.
2. **Confirm**: Run a 3-question seed interview to capture their core milestones/standards, then show a confirmation preview.
3. **Build**: Write the configuration to `docs/PERSONAL_COMPASS.md`, `docs/HORIZON_ENGINE.md`, or `docs/company/ENGINEERING_PLAYBOOK.md`, and seed `system/data/nirixa.db`.

---

## 🎯 Coding & Behavioral Standards
- **Collaborative Q&A First**: Debate and align on approach before executing large refactors.
- **High-Signal Tech Copywriting**: Strict, sparse, intellectual clarity. Zero emoji clutter.
- **Zero File Proliferation**: Centralize thoughts in SQLite DB and hub markdown files.
- **Zero-LLM Fast Path**: Prefer deterministic regex and local Python logic for telemetry, reminders, and daily briefing time-wheels.
