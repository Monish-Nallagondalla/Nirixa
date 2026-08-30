#!/usr/bin/env python3
"""
Nirixa OS Engine - Natural Language Deadline & Implicit Task Parser
Parses relative and absolute time expressions from Telegram messages, IDE chats, and dashboard inputs.
Handles edge cases: 'in 2 hours', 'in 45 mins', 'by tomorrow 9pm', 'tonight', 'Sunday night', 'next Monday 10am', etc.
"""

import os
import sys
import re
import datetime

def parse_target_datetime(text, base_dt=None):
    """
    Parses a natural language time expression and returns a target datetime.
    """
    if base_dt is None:
        base_dt = datetime.datetime.now()
        
    text_lower = text.lower().strip()
    
    # 1. Relative minutes / hours: "in 45 mins", "in 2 hours", "in 30m", "in 1h"
    rel_match = re.search(r'in\s+(\d+)\s*(mins?|minutes?|m|hours?|hrs?|h|days?|d)', text_lower)
    if rel_match:
        qty = int(rel_match.group(1))
        unit = rel_match.group(2)
        if unit.startswith('m') and not unit.startswith('mo'):
            return base_dt + datetime.timedelta(minutes=qty)
        elif unit.startswith('h'):
            return base_dt + datetime.timedelta(hours=qty)
        elif unit.startswith('d'):
            return base_dt + datetime.timedelta(days=qty)
            
    # 2. "tonight" (Default: 22:00 / 10 PM today)
    if "tonight" in text_lower:
        hour = 22
        minute = 0
        target = base_dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if target <= base_dt:
            target += datetime.timedelta(days=1)
        return target
        
    # 3. "tomorrow morning" (09:00), "tomorrow night" (21:00), "tomorrow"
    if "tomorrow" in text_lower:
        tmrw = base_dt + datetime.timedelta(days=1)
        if "morning" in text_lower:
            return tmrw.replace(hour=9, minute=0, second=0, microsecond=0)
        elif "night" in text_lower or "evening" in text_lower:
            return tmrw.replace(hour=21, minute=0, second=0, microsecond=0)
        elif "afternoon" in text_lower:
            return tmrw.replace(hour=14, minute=0, second=0, microsecond=0)
            
        # Check specific time like "tomorrow 9pm", "tomorrow at 5:30 pm"
        time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text_lower.split("tomorrow")[1])
        if time_match:
            hr = int(time_match.group(1))
            mn = int(time_match.group(2) or 0)
            ampm = (time_match.group(3) or "").lower()
            if ampm == "pm" and hr < 12:
                hr += 12
            elif ampm == "am" and hr == 12:
                hr = 0
            return tmrw.replace(hour=hr, minute=mn, second=0, microsecond=0)
        return tmrw.replace(hour=18, minute=0, second=0, microsecond=0) # default 6 PM
        
    # 4. Day of the week: "sunday night", "monday 9pm", "by friday"
    weekdays = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }
    for day_name, day_num in weekdays.items():
        if day_name in text_lower:
            days_ahead = (day_num - base_dt.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7 # next week's day if mentioned
            target_date = base_dt + datetime.timedelta(days=days_ahead)
            
            hr = 21 # default 9 PM for "night"
            mn = 0
            if "morning" in text_lower:
                hr = 9
            elif "afternoon" in text_lower:
                hr = 14
                
            time_match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text_lower)
            if time_match:
                parsed_hr = int(time_match.group(1))
                parsed_mn = int(time_match.group(2) or 0)
                parsed_ampm = (time_match.group(3) or "").lower()
                if parsed_ampm == "pm" and parsed_hr < 12:
                    parsed_hr += 12
                elif parsed_ampm == "am" and parsed_hr == 12:
                    parsed_hr = 0
                hr, mn = parsed_hr, parsed_mn
                
            return target_date.replace(hour=hr, minute=mn, second=0, microsecond=0)
            
    # Default fallback: 24 hours from now
    return base_dt + datetime.timedelta(hours=24)

def parse_task_and_deadline(text, base_dt=None):
    """
    Extracts a clean task title and calculates the exact target deadline timestamp.
    """
    if base_dt is None:
        base_dt = datetime.datetime.now()
        
    raw_clean = text.strip()
    
    # Strip common command prefixes
    clean_title = re.sub(r'^(todo:|task:|add task:|remind me to|we need to|please)\s*', '', raw_clean, flags=re.IGNORECASE)
    
    # Extract deadline substring if present
    target_dt = parse_target_datetime(text, base_dt=base_dt)
    
    # Clean trailing time phrases from title for a crisp task title
    clean_title = re.sub(r'\s+(by|in|at|before|on)\s+(tomorrow|tonight|sunday|monday|tuesday|wednesday|thursday|friday|saturday|\d+\s*(?:mins?|hours?|hrs?|days?|am|pm)).*$', '', clean_title, flags=re.IGNORECASE).strip()
    
    if not clean_title:
        clean_title = raw_clean
        
    return {
        "title": clean_title,
        "deadline_iso": target_dt.strftime("%Y-%m-%d %H:%M:%S"),
        "deadline_human": target_dt.strftime("%b %d, %Y at %I:%M %p")
    }

def detect_implicit_task(text):
    """
    Determines if a raw text/speech capture contains an implicit action task.
    """
    lower = text.lower()
    task_triggers = [
        "we need to", "i need to", "todo:", "task:", "remind me to",
        "finish this by", "finalize this by", "complete by", "have to finish",
        "schedule", "deadline", "by tomorrow", "by sunday", "by tonight"
    ]
    return any(trigger in lower for trigger in task_triggers)

if __name__ == "__main__":
    sample_tests = [
        "we need to finalize all 6 posts by Sunday night",
        "todo: review wealth buffer in 2 hours",
        "remind me to check GROWW portfolio by tomorrow 9pm",
        "finish reading Karpathy wiki paper by tonight"
    ]
    print("=== DEADLINE PARSER TEST SUITE ===")
    for t in sample_tests:
        parsed = parse_task_and_deadline(t)
        print(f"Input: \"{t}\"")
        print(f" -> Title   : {parsed['title']}")
        print(f" -> Deadline: {parsed['deadline_human']} ({parsed['deadline_iso']})\n")
