# Creating Custom Agent Skills

[Documentation](../README.md) / [Guides](LEADER_BLUEPRINT.md) / [Custom Skills](CREATING_CUSTOM_SKILLS.md)

**How to extend Nirixa OS by creating your own specialized agent skills, domain workflows, and procedural routines across Google Antigravity, Cursor, and Claude Code.**

---

## 1. The Skills Architecture

Nirixa OS follows the standard Agent Skills specification (`.agents/skills/<skill_name>/SKILL.md`). Every skill provides structured domain expertise that your coding agent loads on demand.

```
.agents/skills/
├── user-onboarding/
│   └── SKILL.md
├── content-stylist/
│   └── SKILL.md
├── your-custom-skill/
│   ├── SKILL.md
│   └── scripts/           # Optional helper scripts
```

---

## 2. Structure of a `SKILL.md` File

Every skill contains YAML frontmatter followed by clear, actionable instructions:

```markdown
---
name: fitness-coach
description: Tracks daily workout routines, progressive overload metrics, and post-workout recovery.
---

# Fitness Coach Skill

## Trigger Conditions
Activate this skill whenever the user logs workout metrics, asks for training split advice, or sends a [MIND] health update.

## Workflow Rules
1. Extract workout exercises, sets, reps, and weights.
2. Calculate total training volume.
3. Compare against last week's records in SQLite database (`nirixa.db`).
4. Provide immediate constructive feedback on recovery and progressive overload.
```

---

## 3. Example Use Cases for Custom Skills

* **Fitness & Nutrition Coach**: Automate calorie tracking and workout split recommendations.
* **Music & DJ Mentor**: Hardware drill sheets, BPM transition calculators, and setlist planning.
* **Code Review Auditor**: Automatically evaluate pull requests against your company's security invariants.
* **Financial Ledger Advisor**: Summarize monthly SaaS expenses and capital allocation.

---

## 4. Activating Your Skill

Once you create the folder inside `.agents/skills/<skill_name>/SKILL.md`:
* **In Google Antigravity**: Automatically indexed and available to the agent.
* **In Cursor**: Referenced automatically via `.cursorrules`.
* **In Claude Code**: Loaded whenever the domain keywords are mentioned.
