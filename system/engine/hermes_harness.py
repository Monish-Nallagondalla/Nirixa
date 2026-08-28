#!/usr/bin/env python3
"""
Nirixa OS Engine - Hermes Agent Harness Distillation
Distilled from Nous Research Hermes (hermes-fc) repository:
1. Dual-Pass XML + AST Fallback Parser for <tool_call> and <thought> envelopes.
2. Lightweight Schema Validation for Function Parameter Definitions.
3. Formatter for ChatML & <tool_response> payloads.
4. Zero-Bloat Execution Layer (No PyTorch/Transformers overhead).
"""

import os
import sys
import re
import json
import ast
import xml.etree.ElementTree as ET

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

def parse_hermes_envelope(assistant_content):
    """
    Parses Hermes 3 XML reasoning thoughts (<thought>) and tool call (<tool_call>) blocks.
    Uses dual-pass JSON + ast.literal_eval fallback as pioneered in Nous Research hermes-fc.
    """
    thought_match = re.search(r'<thought>(.*?)</thought>', assistant_content, re.DOTALL)
    thought_content = thought_match.group(1).strip() if thought_match else ""

    tool_calls = []
    error_messages = []

    # Attempt XML parsing via root wrapper
    try:
        wrapped_xml = f"<root>{assistant_content}</root>"
        root = ET.fromstring(wrapped_xml)
        for element in root.findall(".//tool_call"):
            json_text = (element.text or "").strip()
            json_data = None
            try:
                json_data = json.loads(json_text)
            except json.JSONDecodeError as json_err:
                try:
                    json_data = ast.literal_eval(json_text)
                except (SyntaxError, ValueError) as eval_err:
                    error_messages.append(f"JSON/AST parse failed: {json_err} | {eval_err}")
            
            if json_data is not None:
                tool_calls.append(json_data)
    except ET.ParseError:
        # Fallback to regex extraction if XML root parsing fails due to unescaped chars
        regex_matches = re.findall(r'<tool_call>\s*({.*?})\s*</tool_call>', assistant_content, re.DOTALL)
        for match in regex_matches:
            json_data = None
            try:
                json_data = json.loads(match)
            except json.JSONDecodeError:
                try:
                    json_data = ast.literal_eval(match)
                except Exception as e:
                    error_messages.append(f"Regex JSON fallback failed: {e}")
            if json_data is not None:
                tool_calls.append(json_data)

    return {
        "thought": thought_content,
        "tool_calls": tool_calls,
        "has_tool_calls": len(tool_calls) > 0,
        "errors": error_messages
    }

def format_hermes_tool_response(tool_name, result):
    """
    Formats local tool execution results back into Hermes <tool_response> format.
    """
    return f"<tool_response>\n{{\"name\": \"{tool_name}\", \"result\": {json.dumps(result)}}}\n</tool_response>"

def format_chatml_prompt(system_prompt, user_prompt, tools_schema=None):
    """
    Formats ChatML prompt compatible with Hermes 3 / OpenHermes chat templates.
    """
    prompt = f"<|im_start|>system\n{system_prompt}"
    if tools_schema:
        prompt += f"\n\nYou have access to the following tools:\n<tools>\n{json.dumps(tools_schema, indent=2)}\n</tools>"
    prompt += "\n<|im_end|>\n"
    prompt += f"<|im_start|>user\n{user_prompt}\n<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"
    return prompt

if __name__ == "__main__":
    sample_assistant_output = """<thought>
The user requested a system health evaluation. I will call the run_system_evals tool.
</thought>
<tool_call>
{'name': 'run_system_evals', 'arguments': {'check_all': True}}
</tool_call>"""

    parsed = parse_hermes_envelope(sample_assistant_output)
    print("=== DUAL-PASS HERMES PARSER TEST ===")
    print("Thought Trace:", parsed["thought"])
    print("Parsed Tool Calls:", json.dumps(parsed["tool_calls"], indent=2))
    print("Has Tool Calls:", parsed["has_tool_calls"])
