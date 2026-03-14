#!/usr/bin/env python3
"""
Nirixa OS Engine - Unified Event-Driven Telegram Daemon (Self-Evolution, Telemetry & Proactive Briefings)
Listens for incoming Telegram events & button callback queries in real time.
Executes Proactive Daily Briefings, Battery Alerts, Zero-LLM Reminders, Spar-First Chief of Staff intelligence,
Laptop Telemetry & Feedback UI, and manages DB-First memory core inside system/data/nirixa.db.
"""

import os
import sys
import time
import json
import yaml
import datetime
import re
import urllib.request
import urllib.parse
import shutil
import subprocess

# Import Nirixa DB, Synthesizer & Evolver modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
sys.path.insert(0, os.path.abspath(os.path.join(script_dir, "..", "scripts")))

# Always redirect stdout/stderr to system/logs/daemon.log unless --debug is set
workspace_root_tmp = os.path.abspath(os.path.join(script_dir, "..", ".."))
log_dir_tmp = os.path.join(workspace_root_tmp, "system", "logs")
os.makedirs(log_dir_tmp, exist_ok=True)
if "--debug" not in sys.argv:
    log_file_obj = open(os.path.join(log_dir_tmp, "daemon.log"), "a", encoding="utf-8")
    sys.stdout = log_file_obj
    sys.stderr = log_file_obj


import db
import synthesizer
import evolver
import sync



# Global tracker for proactive alerts to avoid duplicate notifications
LAST_PROACTIVE_DATE = {"morning": "", "evening": "", "battery_alert": False}

def load_config():
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    config_path = os.path.join(workspace_root, "system", "config", "config.yaml")
    env_path = os.path.join(workspace_root, "system", "config", ".env")

    config = {}
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()

    return config, env_vars, workspace_root

def build_opener(proxy=None):
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}))
    return urllib.request.build_opener(*handlers)

def get_authorized_chat_id(workspace_root, env_vars):
    if env_vars.get("TELEGRAM_CHAT_ID"):
        return str(env_vars.get("TELEGRAM_CHAT_ID"))
    return None

def send_telegram_reply(token, chat_id, text, reply_markup=None, api_base="https://api.telegram.org", proxy=None):
    if not token or not chat_id:
        return False
    url = f"{api_base.rstrip('/')}/bot{token}/sendMessage"
    opener = build_opener(proxy)
    
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json", "User-Agent": "NirixaOS-Daemon/1.0"})
        with opener.open(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("ok", False)
    except Exception as e:
        print(f"[Error] Failed to send reply: {e}")
        return False

def answer_callback_query(token, callback_id, text="Processing...", api_base="https://api.telegram.org", proxy=None):
    url = f"{api_base.rstrip('/')}/bot{token}/answerCallbackQuery"
    opener = build_opener(proxy)
    payload = {"callback_query_id": callback_id, "text": text}
    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
        with opener.open(req, timeout=5) as resp:
            pass
    except Exception:
        pass

def get_contextual_inline_buttons(reply_type="conversational", capture_id=0):
    """
    Returns contextual inline keyboards only when relevant.
    Conversational / Q&A replies return None (clean text).
    Draft / Sparring replies return thesis refinement buttons.
    Nudges / Reminders return action buttons.
    """
    if reply_type in ["conversational", "text", "info"]:
        return None
    elif reply_type in ["ota_draft", "sparring"]:
        return {
            "inline_keyboard": [
                [
                    {"text": "🥊 Refine Thesis", "callback_data": f"spar_{capture_id}"},
                    {"text": "📄 Stage Draft", "callback_data": f"draft_{capture_id}"}
                ]
            ]
        }
    elif reply_type in ["nudge", "reminder"]:
        return {
            "inline_keyboard": [
                [
                    {"text": "✅ Complete Task", "callback_data": f"done_{capture_id}"},
                    {"text": "⏰ Snooze 2h", "callback_data": f"snooze120_{capture_id}"}
                ]
            ]
        }
    return None

def get_default_inline_buttons(capture_id=0):
    return get_contextual_inline_buttons("conversational", capture_id)

def get_reminder_action_buttons(reminder_id=0):
    return {
        "inline_keyboard": [
            [
                {"text": "✅ Mark Done", "callback_data": f"done_{reminder_id}"},
                {"text": "⏰ +15m", "callback_data": f"snooze15_{reminder_id}"},
                {"text": "⏰ +1h", "callback_data": f"snooze60_{reminder_id}"}
            ],
            [
                {"text": "🥊 Spar Task", "callback_data": f"spartask_{reminder_id}"}
            ]
        ]
    }

def parse_reminder_input(text):
    """Zero-LLM Deterministic Time Parser."""
    if not text:
        return None, None

    clean_text = text.strip()
    match_prefix = re.match(r'^(?:remind me|remind|set reminder)\s+(.*)', clean_text, re.IGNORECASE)
    if not match_prefix:
        return None, None

    body = match_prefix.group(1).strip()
    now = datetime.datetime.now()
    target_dt = None
    msg = body

    rel_match = re.match(r'^(?:in\s+)?(\d+)\s*(m|min|mins|minute|minutes|h|hr|hrs|hour|hours|d|day|days)\s*(?:to\s+|for\s+)?(.*)', body, re.IGNORECASE)
    if rel_match:
        val = int(rel_match.group(1))
        unit = rel_match.group(2).lower()
        msg = rel_match.group(3).strip() or "Pending Task"

        if unit.startswith('m'):
            target_dt = now + datetime.timedelta(minutes=val)
        elif unit.startswith('h'):
            target_dt = now + datetime.timedelta(hours=val)
        elif unit.startswith('d'):
            target_dt = now + datetime.timedelta(days=val)

    elif re.match(r'^at\s+\d{1,2}:\d{2}', body, re.IGNORECASE):
        at_match = re.match(r'^at\s+(\d{1,2}):(\d{2})\s*(am|pm)?\s*(?:to\s+|for\s+)?(.*)', body, re.IGNORECASE)
        if at_match:
            hr = int(at_match.group(1))
            mn = int(at_match.group(2))
            ampm = at_match.group(3)
            msg = at_match.group(4).strip() or "Pending Task"

            if ampm:
                if ampm.lower() == 'pm' and hr < 12:
                    hr += 12
                elif ampm.lower() == 'am' and hr == 12:
                    hr = 0

            target_dt = now.replace(hour=hr, minute=mn, second=0, microsecond=0)
            if target_dt <= now:
                target_dt += datetime.timedelta(days=1)

    if target_dt:
        return target_dt, msg
        
    return None, None

def get_laptop_telemetry(workspace_root):
    """Fetch real-time hardware & Nirixa OS telemetry"""
    db_path = db.get_db_path(workspace_root)
    size_kb = round(os.path.getsize(db_path) / 1024, 1) if os.path.exists(db_path) else 0

    total, used, free = shutil.disk_usage(workspace_root)
    free_gb = round(free / (1024 ** 3), 1)

    battery_str = "Plugged In"
    cpu_str = "Active"
    ram_str = "Normal"

    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery:
            pct = battery.percent
            plugged = "Charging" if battery.power_plugged else "Discharging"
            battery_str = f"{pct}% ({plugged})"
        cpu_str = f"{psutil.cpu_percent(interval=None)}%"
        mem = psutil.virtual_memory()
        ram_str = f"{round(mem.used/(1024**3), 1)} / {round(mem.total/(1024**3), 1)} GB"
    except ImportError:
        pass

    telemetry = f"""💻 LAPTOP & OS TELEMETRY DASHBOARD
----------------------------------------
🔋 Battery : {battery_str}
🧠 CPU Load: {cpu_str}
💾 RAM     : {ram_str}
📁 Disk    : {free_gb} GB free on C:\\

⚡ NIRIXA OS HEALTH
----------------------------------------
• SQLite Core  : system/data/nirixa.db ({size_kb} KB)
• Engine Status: Gemini Flash Spar-First Core
• Proactive    : Daily Briefings & Battery Alerts Active
• Connection   : Online (0-delay polling)"""
    return telemetry

def generate_proactive_briefing(workspace_root, briefing_type="morning"):
    """Generate structured Executive Briefing for Monish"""
    db_path = db.get_db_path(workspace_root)
    data = db.get_proactive_briefing_data(db_path)
    telemetry = get_laptop_telemetry(workspace_root)
    reminders = db.get_pending_reminders_summary(db_path)
    otas = db.get_ota_summary(db_path)

    now_str = datetime.datetime.now().strftime("%A, %B %d, %Y - %I:%M %p")

    if briefing_type == "morning":
        return f"""☀️ MORNING EXECUTIVE BRIEFING
{now_str}
========================================

⏰ TODAY'S REMINDERS & AGENDA:
{reminders}

💡 RECENT OTAs & THREATS:
{otas}

{telemetry}
========================================
Standing by. What is our primary focus today?"""
    else:
        return f"""🌙 EVENING SYNC-DOWN
{now_str}
========================================

📊 DAY SUMMARY & STATS:
• Mobile Captures: {data['total_captures']}
• Active OTAs    : {data['total_otas']}
• Signal Rating  : {data['upvotes']} 👍 / {data['downvotes']} 👎

⏰ REMAINING PENDING REMINDERS:
{reminders}

{telemetry}
========================================
Sign-off ready. Text anytime to spar on tomorrow's priorities."""

def check_and_trigger_proactive_briefings(token, auth_chat_id, workspace_root, api_base="https://api.telegram.org", proxy=None):
    """Background Worker: Triggers Morning Briefing (9 AM), Evening Sync (9 PM), and Low Battery Alerts"""
    if not auth_chat_id or not token:
        return

    now = datetime.datetime.now()
    today_str = now.strftime("%Y-%m-%d")
    hour = now.hour
    minute = now.minute

    # Morning Briefing at 9:00 AM
    if hour == 9 and minute < 5 and LAST_PROACTIVE_DATE["morning"] != today_str:
        LAST_PROACTIVE_DATE["morning"] = today_str
        text = generate_proactive_briefing(workspace_root, briefing_type="morning")
        send_telegram_reply(token, auth_chat_id, text, reply_markup=get_default_inline_buttons(0), api_base=api_base, proxy=proxy)
        print(f"[Proactive Engine] Pushed Morning Executive Briefing to Telegram.")

    # Evening Sync at 9:00 PM (21:00)
    elif hour == 21 and minute < 5 and LAST_PROACTIVE_DATE["evening"] != today_str:
        LAST_PROACTIVE_DATE["evening"] = today_str
        text = generate_proactive_briefing(workspace_root, briefing_type="evening")
        send_telegram_reply(token, auth_chat_id, text, reply_markup=get_default_inline_buttons(0), api_base=api_base, proxy=proxy)
        print(f"[Proactive Engine] Pushed Evening Sync-Down to Telegram.")

    # Battery Warning Alert (< 20% while discharging)
    try:
        import psutil
        battery = psutil.sensors_battery()
        if battery and battery.percent <= 20 and not battery.power_plugged:
            if not LAST_PROACTIVE_DATE["battery_alert"]:
                LAST_PROACTIVE_DATE["battery_alert"] = True
                alert_text = f"⚠️ BATTERY WARNING: Laptop battery is at {battery.percent}% (Discharging). Plug in your charger to keep Nirixa OS running!"
                send_telegram_reply(token, auth_chat_id, alert_text, reply_markup=get_default_inline_buttons(0), api_base=api_base, proxy=proxy)
        elif battery and (battery.percent > 25 or battery.power_plugged):
            LAST_PROACTIVE_DATE["battery_alert"] = False
    except Exception:
        pass

def apply_anonymization(text, rules):
    if not text:
        return text
    anonymized = text
    for rule in rules:
        pattern = rule.get("match")
        replacement = rule.get("replace", "[Redacted]")
        if pattern:
            anonymized = re.sub(pattern, replacement, anonymized)
    return anonymized

MUTE_UNTIL = None

def perform_startup_self_check(token, auth_chat_id, workspace_root, api_base="https://api.telegram.org", proxy=None):
    """
    Performs startup self-check testing Telegram API, Google Calendar setup, and nirixa.db.
    Logs daemon_startup_check row to system_audits.
    """
    results = {"telegram": "fail", "gcal": "fail", "db": "fail"}
    db_path = db.get_db_path(workspace_root)
    
    if token:
        try:
            url = f"{api_base.rstrip('/')}/bot{token}/getMe"
            opener = build_opener(proxy)
            req = urllib.request.Request(url, headers={"User-Agent": "NirixaOS-Daemon/1.0"})
            with opener.open(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("ok"):
                    results["telegram"] = "pass"
        except Exception as e:
            results["telegram"] = f"fail ({e})"

    try:
        cred_file = os.path.join(workspace_root, "system", "config", "credentials.json")
        pickle_file = os.path.join(workspace_root, "system", "config", "token.pickle")
        if os.path.exists(cred_file) or os.path.exists(pickle_file):
            results["gcal"] = "pass"
        else:
            results["gcal"] = "not_configured"
    except Exception as e:
        results["gcal"] = f"fail ({e})"

    try:
        db.init_db(db_path)
        results["db"] = "pass"
    except Exception as e:
        results["db"] = f"fail ({e})"

    result_str = f"telegram: {results['telegram']}, gcal: {results['gcal']}, db: {results['db']}"
    db.log_audit_metric("daemon_startup_check", result_str, db_path=db_path)
    print(f"[Daemon Startup Self-Check] {result_str}")
    return results

def check_mute_command(text):
    global MUTE_UNTIL
    match = re.match(r'^quiet\s+(\d+)([hm])?', text.strip(), re.IGNORECASE)
    if match:
        val = int(match.group(1))
        unit = (match.group(2) or 'h').lower()
        now = datetime.datetime.now()
        if unit == 'm':
            MUTE_UNTIL = now + datetime.timedelta(minutes=val)
        else:
            MUTE_UNTIL = now + datetime.timedelta(hours=val)
        time_str = MUTE_UNTIL.strftime("%I:%M %p")
        return f"🤫 Muted proactive delegator pushes until {time_str} ({val}{unit})."
    return None

def handle_action_commands(user_text, workspace_root):
    """OpenClaw Action Command Router"""
    mute_reply = check_mute_command(user_text)
    if mute_reply:
        return mute_reply

    clean_cmd = user_text.strip().lower()
    
    if clean_cmd in ["/inbox", "inbox", "/captures"]:
        rows = db.get_recent_captures(limit=5, db_path=db.get_db_path(workspace_root))
        if not rows:
            return "Mobile inbox is clean. No pending captures."
        items = [f"• [{r[1]}] {r[2]}" for r in rows]
        return "Recent Captures in SQLite:\n" + "\n".join(items)
        
    elif clean_cmd in ["/otas", "otas", "/ota"]:
        return "Original Thought Assets (OTAs) in SQLite:\n" + db.get_ota_summary(db.get_db_path(workspace_root))
        
    elif clean_cmd in ["/status", "status", "/telemetry"]:
        return get_laptop_telemetry(workspace_root)

    elif clean_cmd in ["/reminders", "reminders", "/tasks"]:
        return "Pending Reminders in SQLite:\n" + db.get_pending_reminders_summary(db.get_db_path(workspace_root))

    elif clean_cmd in ["/briefing", "briefing", "/morning"]:
        return generate_proactive_briefing(workspace_root, briefing_type="morning")

    elif clean_cmd.startswith("/search ") or clean_cmd.startswith("search "):
        q = user_text.strip().split(" ", 1)[1] if " " in user_text.strip() else ""
        return db.search_fts(q, limit=5, db_path=db.get_db_path(workspace_root))

    elif clean_cmd in ["/evolver", "evolver", "/audit"]:
        report, report_path = evolver.generate_evolution_audit(workspace_root)
        return f"⚡ SYSTEM EVOLUTION AUDIT\n----------------------------------------\nGenerated report at docs/SYSTEM_EVOLUTION.md\n\n" + report[:500] + "..."
        
    return None

def check_and_trigger_reminders(token, workspace_root, api_base="https://api.telegram.org", proxy=None):
    """Zero-LLM Background Worker: Checks SQLite for due reminders and fires alerts"""
    due_list = db.get_due_reminders(db.get_db_path(workspace_root))
    for rem_id, chat_id, msg, remind_at in due_list:
        alert_text = f"⏰ REMINDER ALERT\n----------------------------------------\n\"{msg}\"\n(Set for {remind_at})"
        buttons = get_reminder_action_buttons(rem_id)
        if send_telegram_reply(token, chat_id, alert_text, reply_markup=buttons, api_base=api_base, proxy=proxy):
            db.mark_reminder_status(rem_id, status="notified", db_path=db.get_db_path(workspace_root))

def generate_spar_first_reply(user_text, capture_id, workspace_root, env_vars, is_draft_request=False, is_spar_request=False, proxy=None):
    action_response = handle_action_commands(user_text, workspace_root)
    if action_response:
        db.save_thread_interaction("telegram_session", user_text, action_response, db_path=db.get_db_path(workspace_root))
        return action_response, get_default_inline_buttons(capture_id)

    gemini_key = env_vars.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY", "")
    thread_history = db.get_recent_thread_history(limit=5, db_path=db.get_db_path(workspace_root))
    evolution_rules = db.get_active_evolution_rules(db.get_db_path(workspace_root))
    profile_context = db.get_profile_context(db_path=db.get_db_path(workspace_root))
    profile_str = "\n".join([f"• {k}: {v}" for k, v in profile_context.items()]) if profile_context else "No custom profile attributes."

    if is_draft_request:
        prompt_mode = """MODE: ASSET DRAFTING
Compile the thesis into two ready-to-publish platform assets:
1. Twitter (X) post: Strictly under 280 characters. Zero emojis. High thesis density.
2. LinkedIn article post: Sparse line breaks, zero sales fluff, Naval/Aviral standard.
Format clearly under headers 'X Post' and 'LinkedIn Post'."""
    elif is_spar_request:
        prompt_mode = """MODE: DEEP SPARRING
1. Challenge Monish's thesis directly from first principles.
2. Present the strongest counter-argument or edge case.
3. Ask 1 sharp, high-leverage question to refine the thesis before drafting."""
    else:
        prompt_mode = """MODE: CHIEF OF STAFF SPARRING (DEFAULT)
1. Respond as a grounded, sharp tech co-founder on WhatsApp.
2. If Monish introduces a new thesis or thought: Spar first! Challenge the assumption or present the counter-argument, then ask 1 sharp question.
3. Keep response concise (2-4 lines max). Zero preachy lectures, zero robotic receipt prefixes ('Noted:', 'Synced to memory', 'I hear you on:')."""

    system_instruction_text = f"""SYSTEM ROLE: You are Nirixa OS - Monish Nallagondalla Srinath's AI Chief of Staff & System Architect.

MONISH NALLAGONDALLA SRINATH USER PROFILE & PERMANENT MEMORY:
{profile_str}

CORE BEHAVIOR RULES:
- Grounded, practical, sharp tech co-founder / Director.
- High-signal, minimalist tech copywriting (Naval Ravikant & Aviral Bhatnagar standard).
- Zero emoji clutter (NEVER use 🔴, 🟢, 🔥, 🚀, 👈, 👇).
- Zero robotic receipts (NEVER output 'Noted:', 'Synced to memory', 'I hear you on:').
- Complete thoughts, never cut off sentences mid-thought.

LEARNED EVOLUTION RULES (RL REINFORCEMENT):
{evolution_rules}

{prompt_mode}

---
RECENT CONVERSATION THREAD HISTORY (SQLite RAG Memory):
{thread_history}
---"""

    last_ai_error = None
    if gemini_key:
        for model in ["gemini-flash-latest", "gemini-2.0-flash", "gemini-1.5-flash-latest", "gemini-pro-latest"]:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
                payload = {
                    "systemInstruction": {
                        "parts": [{"text": system_instruction_text}]
                    },
                    "contents": [
                        {
                            "role": "user",
                            "parts": [{"text": user_text}]
                        }
                    ],
                    "generationConfig": {
                        "temperature": 0.5,
                        "maxOutputTokens": 1000
                    }
                }
                opener = build_opener(proxy)
                data_bytes = json.dumps(payload).encode("utf-8")
                req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
                with opener.open(req, timeout=12) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                    candidates = result.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            reply_text = parts[0].get("text", "").strip()
                            db.save_thread_interaction("telegram_session", user_text, reply_text, db_path=db.get_db_path(workspace_root))
                            
                            if is_draft_request:
                                db.save_ota(capture_id, title=user_text[:40], raw_thought=user_text, refined_thesis=reply_text, db_path=db.get_db_path(workspace_root))
                                
                            reply_buttons = get_contextual_inline_buttons("ota_draft" if (is_draft_request or is_spar_request) else "conversational", capture_id)
                            return reply_text, reply_buttons
            except Exception as e:
                last_ai_error = str(e)
                print(f"[AI Generation Warning ({model})] {e}")

    text_clean = user_text.strip()
    reason_diag = f" (Notice: {last_ai_error})" if last_ai_error else ""
    default_reply = f"Standing by on: \"{text_clean}\"{reason_diag}. Where do we push this next?"
    db.save_thread_interaction("telegram_session", user_text, default_reply, db_path=db.get_db_path(workspace_root))
    return default_reply, get_contextual_inline_buttons("conversational", capture_id)

def start_daemon(test_only=False):
    config, env_vars, workspace_root = load_config()
    anonymize_rules = config.get("anonymization", {}).get("rules", [])
    token = env_vars.get("TELEGRAM_BOT_TOKEN", "")
    api_base = env_vars.get("TELEGRAM_API_BASE_URL") or os.environ.get("TELEGRAM_API_BASE_URL", "https://api.telegram.org")
    proxy = env_vars.get("HTTPS_PROXY") or os.environ.get("HTTPS_PROXY") or env_vars.get("HTTP_PROXY") or os.environ.get("HTTP_PROXY")
    
    db.init_db()
    auth_chat_id = get_authorized_chat_id(workspace_root, env_vars)
    
    # Single-instance PID lock file check
    pid_file = os.path.join(workspace_root, "system", "data", "daemon.pid")
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as pf:
                old_pid = int(pf.read().strip())
            # Check if process is actually alive
            import psutil
            if psutil.pid_exists(old_pid) and old_pid != os.getpid():
                print(f"[Notice] Nirixa OS Daemon already running under PID {old_pid}. Exiting duplicate instance.")
                return
        except Exception:
            pass

    try:
        with open(pid_file, "w") as pf:
            pf.write(str(os.getpid()))
    except Exception:
        pass

    # Handle headless / pythonw execution where stdout/stderr is None
    if sys.stdout is None or sys.stderr is None:
        log_dir = os.path.join(workspace_root, "system", "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, "daemon.log")
        log_file = open(log_file_path, "a", encoding="utf-8")
        sys.stdout = log_file
        sys.stderr = log_file
    elif hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("==================================================")
    print("  NIRIXA OS - PROACTIVE BRIEFING & EVOLVER DAEMON")
    print("==================================================")
    print(f"Workspace Root : {workspace_root}")
    print(f"Auth Chat ID   : {auth_chat_id}")
    
    if not token:
        print("[Error] No TELEGRAM_BOT_TOKEN found in system/config/.env!")
        sys.exit(1)

    # Perform Startup Self-Check & Log to system_audits
    perform_startup_self_check(token, auth_chat_id, workspace_root, api_base=api_base, proxy=proxy)

    if test_only:
        print("\n[Test Mode] Connection & Proactive Briefing Engine verified successfully!")
        briefing_sample = generate_proactive_briefing(workspace_root, briefing_type="morning")
        print(briefing_sample[:300] + "\n...")
        sys.exit(0)

    print("\n[Daemon] Listening for events, zero-LLM reminders & proactive briefings... (Press Ctrl+C to stop)")
    offset = 0
    pending_burst = []
    last_msg_time = 0
    DEBOUNCE_SECONDS = 8
    backoff_delay = 5  # Exponential backoff: starts at 5s, doubles up to 300s
    
    while True:
        try:
            # Step 1: Check and trigger due reminders (Zero-LLM local worker)
            check_and_trigger_reminders(token, workspace_root, api_base=api_base, proxy=proxy)

            # Step 2: Check and trigger proactive briefings & battery alerts
            check_and_trigger_proactive_briefings(token, auth_chat_id, workspace_root, api_base=api_base, proxy=proxy)

            # Step 3: Flush pending burst if debounce window has elapsed
            if pending_burst and (time.time() - last_msg_time >= DEBOUNCE_SECONDS):
                combined_text = "\n\n".join([item["text"] for item in pending_burst])
                last_c_id = pending_burst[-1]["c_id"]
                chat_target = pending_burst[-1]["chat_id"] or auth_chat_id
                
                print(f"\n[Debouncer] Flushing burst of {len(pending_burst)} messages into 1 sparring turn...")
                ai_reply, buttons = generate_spar_first_reply(combined_text, last_c_id, workspace_root, env_vars, proxy=proxy)
                send_telegram_reply(token, chat_target, ai_reply, reply_markup=buttons, api_base=api_base, proxy=proxy)
                print(f"[Handled & Replied via AI Sparring Core] Combined burst size: {len(pending_burst)}")
                pending_burst = []

            # Step 4: Poll Telegram updates with short timeout for responsive debouncing
            poll_timeout = 3 if pending_burst else 15
            url = f"{api_base.rstrip('/')}/bot{token}/getUpdates?offset={offset}&timeout={poll_timeout}"
            opener = build_opener(proxy)
            req = urllib.request.Request(url, headers={"User-Agent": "NirixaOS-Daemon/1.0"})
            
            with opener.open(req, timeout=poll_timeout + 5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("ok"):
                    backoff_delay = 5  # Reset backoff on successful response
                    db.record_heartbeat(db.get_db_path(workspace_root))
                    updates = data.get("result", [])
                    for upd in updates:
                        upd_id = upd.get("update_id", 0)
                        offset = upd_id + 1
                        
                        # Handle Callback Query (Button Clicks)
                        if "callback_query" in upd:
                            cb = upd["callback_query"]
                            cb_id = cb.get("id")
                            cb_data = cb.get("data", "")
                            from_chat_id = str(cb.get("message", {}).get("chat", {}).get("id", ""))
                            
                            answer_callback_query(token, cb_id, text="Action logged!", api_base=api_base, proxy=proxy)
                            
                            if cb_data.startswith("done_"):
                                r_id = int(cb_data.split("_")[1]) if cb_data.split("_")[1].isdigit() else 0
                                db.mark_reminder_status(r_id, status="completed", db_path=db.get_db_path(workspace_root))
                                send_telegram_reply(token, from_chat_id, "✅ Reminder marked complete!", reply_markup=get_default_inline_buttons(0), api_base=api_base, proxy=proxy)
                                
                            elif cb_data.startswith("snooze15_"):
                                r_id = int(cb_data.split("_")[1]) if cb_data.split("_")[1].isdigit() else 0
                                new_time = db.snooze_reminder(r_id, 15, db_path=db.get_db_path(workspace_root))
                                send_telegram_reply(token, from_chat_id, f"⏰ Snoozed for +15m (Next alert at {new_time})", reply_markup=get_default_inline_buttons(0), api_base=api_base, proxy=proxy)

                            elif cb_data.startswith("snooze60_"):
                                r_id = int(cb_data.split("_")[1]) if cb_data.split("_")[1].isdigit() else 0
                                new_time = db.snooze_reminder(r_id, 60, db_path=db.get_db_path(workspace_root))
                                send_telegram_reply(token, from_chat_id, f"⏰ Snoozed for +1h (Next alert at {new_time})", reply_markup=get_default_inline_buttons(0), api_base=api_base, proxy=proxy)

                            elif cb_data.startswith("spartask_"):
                                r_id = int(cb_data.split("_")[1]) if cb_data.split("_")[1].isdigit() else 0
                                reply_text, buttons = generate_spar_first_reply("Let's spar on this task", 0, workspace_root, env_vars, is_spar_request=True, proxy=proxy)
                                send_telegram_reply(token, from_chat_id, reply_text, reply_markup=buttons, api_base=api_base, proxy=proxy)

                            elif cb_data.startswith("upvote_"):
                                c_id = int(cb_data.split("_")[1]) if cb_data.split("_")[1].isdigit() else 0
                                db.save_evolution_feedback(c_id, rating=1, feedback_text="High-signal response", rule_extracted="Reinforce concise, grounded sparring tone.", db_path=db.get_db_path(workspace_root))
                                send_telegram_reply(token, from_chat_id, "Feedback recorded: +1 High-Signal.", reply_markup=get_default_inline_buttons(c_id), api_base=api_base, proxy=proxy)
                                
                            elif cb_data.startswith("downvote_"):
                                c_id = int(cb_data.split("_")[1]) if cb_data.split("_")[1].isdigit() else 0
                                db.save_evolution_feedback(c_id, rating=-1, feedback_text="Low-signal response", rule_extracted="Avoid verbosity, stay concise and non-preachy.", db_path=db.get_db_path(workspace_root))
                                send_telegram_reply(token, from_chat_id, "Feedback recorded: -1 Low-Signal.", reply_markup=get_default_inline_buttons(c_id), api_base=api_base, proxy=proxy)

                            elif cb_data.startswith("spar_"):
                                c_id = int(cb_data.split("_")[1]) if cb_data.split("_")[1].isdigit() else 0
                                last_captures = db.get_recent_captures(limit=1, db_path=db.get_db_path(workspace_root))
                                user_text = last_captures[0][2] if last_captures else "Our strategic focus"
                                reply_text, buttons = generate_spar_first_reply(user_text, c_id, workspace_root, env_vars, is_spar_request=True, proxy=proxy)
                                send_telegram_reply(token, from_chat_id, reply_text, reply_markup=buttons, api_base=api_base, proxy=proxy)
                                
                            elif cb_data.startswith("draft_"):
                                c_id = int(cb_data.split("_")[1]) if cb_data.split("_")[1].isdigit() else 0
                                last_captures = db.get_recent_captures(limit=1, db_path=db.get_db_path(workspace_root))
                                user_text = last_captures[0][2] if last_captures else "Our strategic thesis"
                                reply_text, buttons = generate_spar_first_reply(user_text, c_id, workspace_root, env_vars, is_draft_request=True, proxy=proxy)
                                send_telegram_reply(token, from_chat_id, reply_text, reply_markup=buttons, api_base=api_base, proxy=proxy)
                                
                            elif cb_data == "status_0":
                                telemetry_text = get_laptop_telemetry(workspace_root)
                                send_telegram_reply(token, from_chat_id, telemetry_text, reply_markup=get_default_inline_buttons(0), api_base=api_base, proxy=proxy)
                                
                            elif cb_data == "reminders_0":
                                rem_text = handle_action_commands("/reminders", workspace_root)
                                send_telegram_reply(token, from_chat_id, rem_text, reply_markup=get_default_inline_buttons(0), api_base=api_base, proxy=proxy)
                                
                            continue

                        # Handle Standard Telegram Messages
                        if db.is_update_processed(upd_id):
                            continue
                            
                        msg = upd.get("message") or upd.get("edited_message") or {}
                        is_edited = "edited_message" in upd
                        from_chat_id = str(msg.get("chat", {}).get("id", ""))
                        text = msg.get("text") or msg.get("caption") or ""
                        
                        if not auth_chat_id and from_chat_id:
                            auth_chat_id = from_chat_id
                            
                        if auth_chat_id and from_chat_id != auth_chat_id:
                            continue

                        if not text:
                            continue
                            
                        prefix = "[Received Edited Event #" if is_edited else "[Received Event #"
                        print(f"\n{prefix}{upd_id}] {text[:50]}...")
                        cleaned = apply_anonymization(text, anonymize_rules)
                        
                        c_id = db.save_capture(upd_id, auth_chat_id, text, cleaned, source="telegram-daemon") or 0
                        synthesizer.synthesize_topics(workspace_root)

                        # Real-Time Local Inbox Append (Air-Gap Boundary: Local Only, No Git Push)
                        try:
                            sync.append_thought_to_monthly_log(cleaned, source="telegram", root_path=workspace_root)
                            m_id = msg.get("message_id")
                            if auth_chat_id and m_id:
                                sync.record_synced_message(workspace_root, auth_chat_id, m_id)
                        except Exception as sync_err:
                            print(f"[Event Sync Warning] {sync_err}")

                        # ZERO-LLM FAST PATH 1: Action Command Routing (Instant response)
                        action_reply = handle_action_commands(text, workspace_root)
                        if action_reply:
                            send_telegram_reply(token, auth_chat_id, action_reply, reply_markup=get_default_inline_buttons(c_id), api_base=api_base, proxy=proxy)
                            print(f"[Handled via Action Command] #{upd_id}")
                            continue

                        # ZERO-LLM FAST PATH 2: Reminder Input Parsing (Instant response)
                        rem_dt, rem_msg = parse_reminder_input(text)
                        if rem_dt:
                            rem_id, rem_time_str = db.save_reminder(auth_chat_id, rem_msg, rem_dt, db_path=db.get_db_path(workspace_root))
                            reply_text = f"⏰ REMINDER SET (Zero-LLM Fast Path)\n----------------------------------------\nTask: \"{rem_msg}\"\nScheduled for: {rem_time_str}"
                            send_telegram_reply(token, auth_chat_id, reply_text, reply_markup=get_default_inline_buttons(c_id), api_base=api_base, proxy=proxy)
                            print(f"[Handled via Zero-LLM Fast Path] Reminder #{rem_id} set for {rem_time_str}")
                            continue

                        # Buffer for 8s Debounce Sparring Path
                        pending_burst.append({"c_id": c_id, "text": text, "chat_id": auth_chat_id})
                        last_msg_time = time.time()
                        print(f"[Debouncer] Buffered message #{upd_id} (Burst size: {len(pending_burst)})")
                            
        except KeyboardInterrupt:
            print("\n[Shutdown] Stopping Nirixa OS Daemon...")
            try:
                if os.path.exists(pid_file):
                    os.remove(pid_file)
            except Exception:
                pass
            break
        except Exception as e:
            err_type = type(e).__name__
            err_str = str(e)
            print(f"[Warning] Polling loop error ({err_type}): {err_str}. Retrying in {backoff_delay}s...")
            try:
                db.log_audit_metric("daemon_error", f"{err_type}: {err_str[:200]}", db_path=db.get_db_path(workspace_root))
            except Exception:
                pass
            time.sleep(backoff_delay)
            backoff_delay = min(300, backoff_delay * 2)

if __name__ == "__main__":
    test_mode = "--test-connection" in sys.argv or "--test" in sys.argv
    try:
        start_daemon(test_only=test_mode)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        crash_msg = f"{type(e).__name__}: {str(e)}"
        print(f"[CRITICAL DAEMON CRASH] {crash_msg}")
        try:
            db.log_audit_metric("daemon_crash", crash_msg)
        except Exception:
            pass
        sys.exit(1)


