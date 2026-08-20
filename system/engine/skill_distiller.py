#!/usr/bin/env python3
"""
Nirixa OS Engine - Autonomous Skill Trajectory Distiller
Inspired by NousResearch Hermes Agent.
Evaluates multi-step execution logs or thread trajectories and automatically distills
reusable patterns into standard .agents/skills/<skill-name>/SKILL.md format.
"""

import os
import sys
import json
import datetime

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from system.engine import db

def distill_skill_from_trajectory(skill_name, description, workflow_steps, category="custom", workspace_root=workspace_root):
    """
    Distills a trajectory of execution steps into a clean markdown skill file.
    """
    skills_dir = os.path.join(workspace_root, ".agents", "skills", skill_name)
    os.makedirs(skills_dir, exist_ok=True)
    skill_file = os.path.join(skills_dir, "SKILL.md")

    now_str = datetime.datetime.now().strftime("%Y-%m-%d")

    steps_md = ""
    for idx, step in enumerate(workflow_steps, 1):
        steps_md += f"### Step {idx}: {step.get('title', f'Phase {idx}')}\n"
        if step.get("description"):
            steps_md += f"{step['description']}\n\n"
        if step.get("command"):
            steps_md += f"```bash\n{step['command']}\n```\n\n"

    skill_content = f"""---
name: {skill_name}
description: {description}
category: {category}
created_at: {now_str}
distilled_by: nirixa-skill-distiller
---

# {skill_name.replace('-', ' ').title()} Skill

[Documentation](../../../docs/README.md) / [Skills](SKILL.md) / [{skill_name.title()}](SKILL.md)

**{description}**

---

## Autonomous Execution Trajectory

{steps_md}
---

## Verification & Compliance
* All execution steps must yield zero exit codes.
* Verify results with `python system/engine/evals/run_system_evals.py`.
"""

    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(skill_content)

    # Register distilled skill in database
    db.save_capture(
        f"skill_distill_{skill_name}", "system",
        f"Distilled new agent skill: {skill_name}",
        f"Distilled new agent skill: {skill_name}",
        source="skill-distiller"
    )

    print(f"[Skill Distiller] Successfully compiled skill into {skill_file}")
    return skill_file

if __name__ == "__main__":
    test_steps = [
        {"title": "Inspect Environment", "description": "Verify database schema and environment variables.", "command": "python system/engine/db.py"},
        {"title": "Run System Evals", "description": "Execute Track A regression test suite.", "command": "python system/engine/evals/run_system_evals.py"}
    ]
    distill_skill_from_trajectory("auto-health-check", "Autonomously audits system health and database integrity.", test_steps)
