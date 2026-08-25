---
name: story-bank-harness
description: Manages Monish's persistent story bank, storing empirical scars, career milestones, and achievements for automatic retrieval when drafting authority posts (MoFu).
---

# Story Bank Harness Skill (`story-bank-harness`)

Use this skill to log, index, and query personal stories for authority posts and profile About sections.

---

## 🎯 Directives
1. **Persistent Memory**: All stories are stored in `story_bank` table in `nirixa.db`.
2. **Authority Integration**: Pull personal scars and metrics into posts to convert generic how-to articles into high-authority "How I Did It" posts.
3. **Template Recycling**: Deconstruct viral post structures into **Hook -> Story Bridge -> Educational Meat -> Mic Drop** while injecting authentic user stories.

## 🛠️ CLI Execution
```bash
python system/engine/story_bank.py
```
