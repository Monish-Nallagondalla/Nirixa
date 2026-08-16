---
name: user-onboarding
description: Reverse-engineered, progressive onboarding (Inform -> Confirm -> Build) guiding individuals and companies to launch their Personal Chief of Staff or Living Company Playbook across Antigravity, Cursor, and Claude Code.
---
# Universal Onboarding Protocol (`user-onboarding`)

Use this skill when a user clones the repository, runs their first setup, or asks: *"How do I get started?"*, *"Set up my OS"*, or *"Onboard me"*.

---

## ⚡ The 3-Stage "Inform ➔ Confirm ➔ Build" Protocol

```
Stage 1: INFORM ────────► Stage 2: CONFIRM ────────► Stage 3: BUILD
(Select Mode & Framework)   (Interactive Seed Q&A)     (Personalized Provisioning)
```

---

## Step-by-Step Execution Guide

### Stage 1: INFORM (Choose Operating Mode)
Ask the user in chat:
> *"Welcome to Nirixa OS! Let's set up your system in under 3 minutes. Are you configuring this for:"*
> 1. **👤 Personal Chief of Staff** (Life Goals, Socratic Thinking, Career, Mobile Capture)
> 2. **🏛️ Company Living Wiki & Playbook** (Engineering Standards, Post-Mortem Scars, Async Standups)
> 3. **🛠️ Custom Hybrid Setup**

---

### Stage 2: CONFIRM (Socratic Seed Interview)

#### If Choice 1: Personal Chief of Staff
Present the two life models:
* **Option A: 4-Quadrant Compass** (*Mission, Mastery, Money, Mind*) — Best for holistic life balance.
* **Option B: 3-Horizon Engine** (*North Star, Friction Radar, Weekly Top 3*) — Best for high-velocity sprints.

Ask 3-4 concise seed questions based on their selection:
* *Goal/Mission*: What are your 1-2 core targets this year?
* *Knowledge/Mastery*: What deep skills or questions are you exploring?
* *Health/Mind*: What is your non-negotiable energy habit?

#### If Choice 2: Company Living Wiki & Playbook
Ask 3-4 team alignment questions:
* *Company Mission*: What is the product and technical thesis of the team?
* *Engineering Standards*: What are 1-2 critical architecture invariants (e.g. DB-first, strict TypeScript)?
* *Primary Friction*: What is the biggest recent production or communication bottleneck?

#### Confirmation Preview:
Generate an immediate preview:
> *"Here is your proposed Operating Blueprint. Does this accurately represent your priorities, or would you like to tweak anything before we lock it in?"*

---

### Stage 3: BUILD (Deterministic Provisioning)
Once the user confirms:
1. **Provision Documentation**:
   * Personal Compass: Populates `docs/PERSONAL_COMPASS.md` or `docs/HORIZON_ENGINE.md`.
   * Company Wiki: Populates `docs/company/ENGINEERING_PLAYBOOK.md` and `docs/company/POST_MORTEMS_AND_SCARS.md`.
2. **Seed Database Core**: Writes initial profile and goals into `system/data/nirixa.db`.
3. **Connect Mobile/Chat Gateway**:
   * Guides user to paste `TELEGRAM_BOT_TOKEN` / `TELEGRAM_CHAT_ID` into `system/config/.env`.
4. **Dispatches First Live Briefing**:
   * Sends the user's first interactive briefing matched to their chosen mode.
5. **Educates on Progressive Enlightenment**:
   * Introduces the Day 1 ➔ Day 7 ➔ Day 30 cognitive journey ([`docs/PROGRESSIVE_ENLIGHTENMENT.md`](file:///c:/Users/MONISH/OneDrive/Documents/My-Os/docs/PROGRESSIVE_ENLIGHTENMENT.md)).
