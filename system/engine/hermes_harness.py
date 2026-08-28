#!/usr/bin/env python3
"""
Nirixa OS Engine - Hermes Agent Harness Distillation
Distills Nous Research Hermes 3 Agent patterns into Nirixa OS:
1. XML Tool Call & Reasoning Envelope Parsing (<thought>, <tool_call>).
2. Dynamic System Prompt & Skill Injector.
3. Zero-Bloat Local Execution Protocol.
"""

import os
import sys
import re
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

def parse_hermes_envelope(response_text):
    """
    Parses Hermes 3 XML reasoning thoughts and tool call blocks from raw model output.
    """
    thought_match = re.search(r'<thought>(.*?)</thought>', response_text, re.DOTALL)
    thought_content = thought_match.group(1).strip() if thought_match else ""
    
    tool_call_match = re.search(r'<tool_call>\s*({.*?})\s*</tool_call>', response_text, re.DOTALL)
    tool_call_data = None
    if tool_call_match:
        try:
            tool_call_data = json.loads(tool_call_match.group(1))
        except Exception:
            pass
            
    return {
        "thought": thought_content,
        "tool_call": tool_call_data,
        "has_tool_call": tool_call_data is not None
    }

def format_hermes_tool_response(tool_name, result):
    """
    Formats local execution results back into Hermes tool response format.
    """
    return f"<tool_response>\n{{\"name\": \"{tool_name}\", \"result\": {json.dumps(result)}}}\n</tool_response>"

if __name__ == "__main__":
    sample_output = """<thought>
The user wants to check system evals. I should invoke the run_system_evals tool.
</thought>
<tool_call>
{"name": "run_system_evals", "arguments": {"check_all": true}}
</tool_call>"""

    parsed = parse_hermes_envelope(sample_output)
    print("=== HERMES HARNESS TEST ===")
    print("Parsed Thought:", parsed["thought"])
    print("Parsed Tool Call:", json.dumps(parsed["tool_call"], indent=2))
    
    resp = format_hermes_tool_response("run_system_evals", {"pass_rate": 1.0, "status": "DONE"})
    print("Formatted Response:\n", resp)
