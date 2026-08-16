# Company Living Wiki & Playbook Hub

[Documentation](../README.md) / [Company Wiki](README.md)

**An enterprise operating system transforming dormant company wikis and Notion pages into active, living engineering standards, post-mortem scars, and automated async standups.**

---

## The Enterprise Problem

In most companies, documentation is write-only: Notion pages, Confluence spaces, and architecture wikis rot within weeks of being written. When production outages occur, post-mortems are filed and promptly forgotten, leading to the same architectural failures recurring quarters later.

**Nirixa OS (Mode B)** makes documentation executable:
1. **Living Engineering Standards**: Rules in `docs/company/ENGINEERING_PLAYBOOK.md` are actively enforced by coding agents (Antigravity, Cursor, Claude Code) during pull request authoring.
2. **Post-Mortem Scars Vault**: Outages in `docs/company/POST_MORTEMS_AND_SCARS.md` automatically compile into algorithmic invariants that block risky code patterns before deployment.
3. **Async Standup Radar**: Engineers send 30-second mobile voice notes on blockers; Nirixa maps cross-team dependencies and surfaces deadlocks automatically.

---

## Directory Index

| Document | Purpose |
| :--- | :--- |
| [Engineering Playbook](ENGINEERING_PLAYBOOK.md) | Living architectural rules, PR invariants, and test coverage standards. |
| [Post-Mortem Scars Vault](POST_MORTEMS_AND_SCARS.md) | Production outage post-mortems converted into permanent algorithmic constraints. |

---

## Universal Team Onboarding

When a new engineer joins the team:
1. Clone the company repository.
2. Open in Cursor / Antigravity / Claude Code.
3. The coding agent automatically loads the team's living playbook and warns against historical production scars in real-time.
