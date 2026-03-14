#!/usr/bin/env python3
"""
Nirixa OS Engine - Hermes Procedural Trajectory Distiller (Auto-Skill Synthesizer)
Distills successful task execution trajectories into reusable agent skills in .agents/skills/
"""

import os
import sys
import yaml
import datetime

def distill_skill(skill_name, description, instructions_md, workspace_root=None):
    if not workspace_root:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    clean_name = skill_name.strip().lower().replace(" ", "-")
    skills_dir = os.path.join(workspace_root, ".agents", "skills", clean_name)
    os.makedirs(skills_dir, exist_ok=True)
    
    skill_file_path = os.path.join(skills_dir, "SKILL.md")
    
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    content = f"""---
name: {clean_name}
description: {description}
created_at: "{now_str}"
source: "hermes-trajectory-distiller"
---

# {skill_name.title()} Skill (`{clean_name}`)

{description}

## Procedures & Instructions

{instructions_md}
"""

    with open(skill_file_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"[Skill Distiller] Successfully synthesized skill at .agents/skills/{clean_name}/SKILL.md")
    return skill_file_path

if __name__ == "__main__":
    if len(sys.argv) > 2:
        distill_skill(sys.argv[1], sys.argv[2], "Automated skill procedure generated via command line.")
    else:
        print("Usage: python skill_distiller.py <skill-name> <description>")
