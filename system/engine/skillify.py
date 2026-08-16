#!/usr/bin/env python3
"""
Nirixa OS Engine - Skillify Protocol (Inspired by GStack / Garry Tan)
Turns any completed interaction, workflow, or procedures into an immutable,
reusable .agents/skills/<name>/SKILL.md file so you never have to repeat yourself.
"""

import os
import sys
import yaml

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

def skillify_workflow(skill_name, description, directives, execution_steps, workspace_root=workspace_root):
    """
    Compiles a structured skill specification into a permanent .agents/skills/ directory.
    """
    clean_name = skill_name.strip().lower().replace(" ", "-").replace("_", "-")
    skill_dir = os.path.join(workspace_root, ".agents", "skills", clean_name)
    os.makedirs(skill_dir, exist_ok=True)
    
    skill_file = os.path.join(skill_dir, "SKILL.md")
    
    frontmatter = {
        "name": clean_name,
        "description": description.strip()
    }
    
    fm_str = yaml.dump(frontmatter, sort_keys=False).strip()
    
    content = f"---\n{fm_str}\n---\n\n# {skill_name.title()} Skill (`{clean_name}`)\n\n"
    content += f"## Core Purpose\n{description.strip()}\n\n"
    
    content += "## Invariant Directives\n"
    for d in directives:
        content += f"- {d}\n"
    content += "\n"
    
    content += "## Execution Protocol\n"
    for i, step in enumerate(execution_steps, 1):
        content += f"{i}. **{step['title']}**: {step['detail']}\n"
        
    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ [Skillify Success] Compiled skill into: {skill_file}")
    return skill_file

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        test_file = skillify_workflow(
            "test-automated-skill",
            "Auto-generated skill test via skillify protocol",
            ["Rule 1: Always verify input", "Rule 2: Execute deterministically"],
            [
                {"title": "Ingest Context", "detail": "Read from SQLite memory"},
                {"title": "Execute", "detail": "Run tool call"}
            ]
        )
        print("Skillify test passed.")
