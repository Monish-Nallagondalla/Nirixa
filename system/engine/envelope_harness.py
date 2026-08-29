#!/usr/bin/env python3
"""
Nirixa OS Engine - Native Resilient Envelope & Tool Execution Harness
Part of the Nirixa Cognitive Operating System (Nirixa OS IP).

Core Architecture:
1. Dual-Pass Resilient Envelope Parser (XML Root + AST Literal Fallback).
2. Metacognition Trace Isolation (<thought> envelope separation).
3. Deterministic Tool Execution & Structured Response Formatting.
4. Zero-Dependency Lightweight Execution Layer.
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

def parse_reasoning_envelope(assistant_content):
    """
    Parses reasoning thoughts (<thought>) and structured tool call (<tool_call>) blocks.
    Employs a dual-pass decoder (JSON parser + AST literal fallback) to guarantee
    sub-second, fault-tolerant tool argument extraction across all model families.
    """
    thought_match = re.search(r'<thought>(.*?)</thought>', assistant_content, re.DOTALL)
    thought_content = thought_match.group(1).strip() if thought_match else ""

    tool_calls = []
    error_messages = []

    # Pass 1: Strict XML Root Wrapping
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
                    error_messages.append(f"JSON/AST extraction error: {json_err} | {eval_err}")
            
            if json_data is not None:
                tool_calls.append(json_data)
    except ET.ParseError:
        # Pass 2: Regex Extraction Fallback for unescaped tokens
        regex_matches = re.findall(r'<tool_call>\s*({.*?})\s*</tool_call>', assistant_content, re.DOTALL)
        for match in regex_matches:
            json_data = None
            try:
                json_data = json.loads(match)
            except json.JSONDecodeError:
                try:
                    json_data = ast.literal_eval(match)
                except Exception as e:
                    error_messages.append(f"Regex extraction fallback error: {e}")
            if json_data is not None:
                tool_calls.append(json_data)

    return {
        "thought": thought_content,
        "tool_calls": tool_calls,
        "has_tool_calls": len(tool_calls) > 0,
        "errors": error_messages
    }

def format_tool_response(tool_name, result):
    """
    Formats tool execution results into a standardized envelope for model context continuation.
    """
    return f"<tool_response>\n{{\"name\": \"{tool_name}\", \"result\": {json.dumps(result)}}}\n</tool_response>"

def format_structured_prompt(system_prompt, user_prompt, tools_schema=None):
    """
    Assembles high-signal system instructions, tool definitions, and user context.
    """
    prompt = f"<system>\n{system_prompt}"
    if tools_schema:
        prompt += f"\n\nAvailable Tools Schema:\n<tools>\n{json.dumps(tools_schema, indent=2)}\n</tools>"
    prompt += "\n</system>\n"
    prompt += f"<user>\n{user_prompt}\n</user>\n"
    prompt += "<assistant>\n"
    return prompt

if __name__ == "__main__":
    sample_assistant_output = """<thought>
The user requested a system health audit. I will execute the run_system_evals tool.
</thought>
<tool_call>
{'name': 'run_system_evals', 'arguments': {'check_all': True}}
</tool_call>"""

    parsed = parse_reasoning_envelope(sample_assistant_output)
    print("=== NIRIXA NATIVE ENVELOPE HARNESS TEST ===")
    print("Thought Trace:", parsed["thought"])
    print("Parsed Tool Calls:", json.dumps(parsed["tool_calls"], indent=2))
    print("Has Tool Calls:", parsed["has_tool_calls"])
    
    formatted_resp = format_tool_response("run_system_evals", {"status": "SUCCESS", "pass_rate": 1.0})
    print("Formatted Response:\n", formatted_resp)
