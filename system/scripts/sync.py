#!/usr/bin/env python3
"""
My-OS Local Sync Engine (Token-Optimized Monthly Stream Architecture)
Pulls mobile thoughts from Telegram Cloud Queue, applies anonymization filters,
appends them with timestamps to a monthly log file (inbox/YYYY-MM-mobile-inbox.md),
and commits/pushes to Git repository.
"""

import os
import sys
import re
import json
import yaml
import datetime
import urllib.request
import urllib.parse
import subprocess

def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "config", "config.yaml")
    env_path = os.path.join(script_dir, "..", "config", ".env")

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

    return config, env_vars

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

def build_opener(proxy=None):
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}))
    return urllib.request.build_opener(*handlers)

def fetch_telegram_updates(token, api_base="https://api.telegram.org", proxy=None):
    if not token or token == "your_telegram_bot_token_here":
        return []
    
    url = f"{api_base.rstrip('/')}/bot{token}/getUpdates"
    try:
        opener = build_opener(proxy)
        req = urllib.request.Request(url, headers={"User-Agent": "My-OS-SyncEngine/1.0"})
        with opener.open(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                return data.get("result", [])
    except Exception as e:
        print(f"[Warning] Failed to fetch Telegram updates ({api_base}): {e}")
        print("  [Hint] If network/ISP blocks api.telegram.org, set TELEGRAM_API_BASE_URL or HTTPS_PROXY in system/config/.env")
    return []

def clear_telegram_update(token, update_id, api_base="https://api.telegram.org", proxy=None):
    if not token:
        return
    url = f"{api_base.rstrip('/')}/bot{token}/getUpdates?offset={update_id + 1}"
    try:
        opener = build_opener(proxy)
        req = urllib.request.Request(url, headers={"User-Agent": "My-OS-SyncEngine/1.0"})
        with opener.open(req, timeout=5) as resp:
            pass
    except Exception:
        pass

def delete_telegram_message(token, chat_id, message_id, api_base="https://api.telegram.org", proxy=None):
    if not token or not chat_id or not message_id:
        return False
    url = f"{api_base.rstrip('/')}/bot{token}/deleteMessage"
    params = urllib.parse.urlencode({"chat_id": chat_id, "message_id": message_id}).encode("utf-8")
    try:
        opener = build_opener(proxy)
        req = urllib.request.Request(url, data=params, headers={"User-Agent": "My-OS-SyncEngine/1.0"})
        with opener.open(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("ok", False)
    except Exception:
        return False

def record_synced_message(root_path, chat_id, message_id):
    if not chat_id or not message_id:
        return
    data_dir = os.path.join(root_path, "system", "data")
    os.makedirs(data_dir, exist_ok=True)
    registry_file = os.path.join(data_dir, "synced_messages.json")
    
    registry = []
    if os.path.exists(registry_file):
        try:
            with open(registry_file, "r", encoding="utf-8") as f:
                registry = json.load(f) or []
        except Exception:
            registry = []
            
    now = datetime.datetime.now()
    registry.append({
        "chat_id": chat_id,
        "message_id": message_id,
        "synced_at": now.strftime("%Y-%m-%d %H:%M:%S"),
        "timestamp": now.timestamp()
    })
    
    with open(registry_file, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)

def process_7day_message_cleanup(token, root_path, retention_days=7, api_base="https://api.telegram.org", proxy=None):
    if not token:
        return
    data_dir = os.path.join(root_path, "system", "data")
    registry_file = os.path.join(data_dir, "synced_messages.json")
    if not os.path.exists(registry_file):
        return

    try:
        with open(registry_file, "r", encoding="utf-8") as f:
            registry = json.load(f) or []
    except Exception:
        return

    now_ts = datetime.datetime.now().timestamp()
    cutoff_sec = retention_days * 86400

    remaining = []
    deleted_count = 0

    for item in registry:
        ts = item.get("timestamp", 0)
        age_sec = now_ts - ts
        if age_sec >= cutoff_sec:
            c_id = item.get("chat_id")
            m_id = item.get("message_id")
            if c_id and m_id:
                delete_telegram_message(token, c_id, m_id, api_base=api_base, proxy=proxy)
                deleted_count += 1
        else:
            remaining.append(item)

    if deleted_count > 0:
        print(f"[Cleanup] Deleted {deleted_count} messages older than {retention_days} days from Telegram chat interface.")

    with open(registry_file, "w", encoding="utf-8") as f:
        json.dump(remaining, f, indent=2)

def append_thought_to_monthly_log(text, source="telegram", root_path="."):
    inbox_dir = os.path.join(root_path, "inbox")
    os.makedirs(inbox_dir, exist_ok=True)
    
    now = datetime.datetime.now()
    month_filename = f"{now.strftime('%Y-%m')}-mobile-inbox.md"
    file_path = os.path.join(inbox_dir, month_filename)
    
    # Initialize monthly log file if new
    if not os.path.exists(file_path):
        header = f"""# Mobile Capture Inbox - {now.strftime('%B %Y')}

> Token-optimized stream of raw thoughts, book quotes, and friction captured via mobile.

---
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(header)
            
    timestamp_str = now.strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""
### 📌 [{timestamp_str}] (Source: {source})

{text.strip()}

---
"""
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)
        
    return file_path

def run_git_sync(workspace_root, commit_prefix):
    try:
        status_output = subprocess.check_output(["git", "status", "--porcelain"], cwd=workspace_root).decode("utf-8").strip()
        if not status_output:
            print("[Git] Workspace clean, nothing to commit.")
            return

        print("[Git] Staging changes...")
        subprocess.run(["git", "add", "inbox/"], cwd=workspace_root, check=True)
        
        commit_msg = f"{commit_prefix}: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        print(f"[Git] Committing: '{commit_msg}'")
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=workspace_root, check=True)
        
        print("[Git] Pushing to remote repository...")
        subprocess.run(["git", "push"], cwd=workspace_root, check=False)
        print("[Git] Git backup complete!")
    except Exception as e:
        print(f"[Git Warning] Could not execute git push: {e}")

def main():
    dry_run = "--dry-run" in sys.argv or "--status" in sys.argv
    config, env_vars = load_config()
    
    workspace_root = config.get("paths", {}).get("workspace_root", "c:/Users/MONISH/OneDrive/Documents/My-Os")
    anonymize_rules = config.get("anonymization", {}).get("rules", [])
    commit_prefix = config.get("git", {}).get("commit_prefix", "feat(sync): mobile capture stream")
    bot_token = env_vars.get("TELEGRAM_BOT_TOKEN", "")
    api_base = env_vars.get("TELEGRAM_API_BASE_URL") or os.environ.get("TELEGRAM_API_BASE_URL", "https://api.telegram.org")
    proxy = env_vars.get("HTTPS_PROXY") or os.environ.get("HTTPS_PROXY") or env_vars.get("HTTP_PROXY") or os.environ.get("HTTP_PROXY")

    print("==================================================")
    print("  MY-OS STREAM MOBILE SYNC ENGINE (TOKEN-OPTIMIZED)")
    print("==================================================")
    print(f"Workspace Root : {workspace_root}")
    print(f"Dry Run Mode   : {dry_run}")
    print(f"API Base Endpoint: {api_base}")
    if proxy:
        print(f"Using Proxy    : {proxy}")
    
    if not bot_token:
        print("\n[Notice] Telegram Bot Token not set in system/config/.env yet.")
        return

    updates = fetch_telegram_updates(bot_token, api_base=api_base, proxy=proxy)
    if not updates:
        print("\n[Sync] No new thoughts in Telegram queue.")
        return

    print(f"\n[Sync] Found {len(updates)} pending updates in Telegram queue!")
    synced_count = 0
    max_update_id = 0

    retention_days = config.get("telegram", {}).get("cleanup_retention_days", 7)
    auto_delete = config.get("telegram", {}).get("auto_delete_synced_messages", False)

    for upd in updates:
        upd_id = upd.get("update_id", 0)
        max_update_id = max(max_update_id, upd_id)
        
        msg = upd.get("message", {})
        text = msg.get("text") or msg.get("caption") or ""
        
        if not text and "voice" in msg:
            text = "[Voice Note Received] (Voice note saved in Telegram chat)"

        if text:
            cleaned_text = apply_anonymization(text, anonymize_rules)
            
            if not dry_run:
                saved_path = append_thought_to_monthly_log(cleaned_text, source="telegram-bot", root_path=workspace_root)
                print(f" Appended to: {os.path.basename(saved_path)}")
                synced_count += 1
                if "chat" in msg and "message_id" in msg:
                    chat_id = msg["chat"].get("id")
                    msg_id = msg.get("message_id")
                    record_synced_message(workspace_root, chat_id, msg_id)
                    if auto_delete:
                        delete_telegram_message(bot_token, chat_id, msg_id, api_base=api_base, proxy=proxy)
            else:
                print(f" [Dry Run] Would append: {cleaned_text[:50]}...")

    if not dry_run and max_update_id > 0:
        clear_telegram_update(bot_token, max_update_id, api_base=api_base, proxy=proxy)
        print(f"\n[Sync] Successfully appended {synced_count} entries to monthly stream log and cleared Telegram queue!")
        if "--push" in sys.argv or "--git" in sys.argv:
            run_git_sync(workspace_root, commit_prefix)

    # Always check 7-day rolling cleanup
    process_7day_message_cleanup(bot_token, workspace_root, retention_days=retention_days, api_base=api_base, proxy=proxy)

if __name__ == "__main__":
    main()
