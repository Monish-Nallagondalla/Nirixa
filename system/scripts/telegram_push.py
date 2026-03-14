#!/usr/bin/env python3
"""
My-OS Telegram Push Utility
Sends a message to the user's Telegram chat.
"""
import os
import sys
import json
import urllib.request
import urllib.parse

def load_env_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, "..", "config", ".env")
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
    return env_vars

def get_chat_id():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    registry_file = os.path.join(script_dir, "..", "data", "synced_messages.json")
    if os.path.exists(registry_file):
        try:
            with open(registry_file, "r", encoding="utf-8") as f:
                registry = json.load(f)
                if registry:
                    # Return the chat_id from the most recent message
                    return registry[-1].get("chat_id")
        except Exception as e:
            print(f"[Error] Could not read synced_messages.json: {e}")
    return None

def send_message(token, chat_id, text, api_base="https://api.telegram.org", proxy=None):
    url = f"{api_base.rstrip('/')}/bot{token}/sendMessage"
    
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}))
    opener = urllib.request.build_opener(*handlers)

    # Try first with Markdown
    params_md = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=params_md, headers={"User-Agent": "My-OS-PushEngine/1.0"})
        with opener.open(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                print("[Success] Message pushed to Telegram.")
                return True
    except Exception:
        pass

    # Fallback to plain text if Markdown parsing failed
    params_plain = urllib.parse.urlencode({
        "chat_id": chat_id,
        "text": text
    }).encode("utf-8")
    
    try:
        req = urllib.request.Request(url, data=params_plain, headers={"User-Agent": "My-OS-PushEngine/1.0"})
        with opener.open(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data.get("ok"):
                print("[Success] Message pushed to Telegram (plain text fallback).")
                return True
            else:
                print(f"[Error] Telegram API error: {data}")
    except Exception as e:
        print(f"[Error] Failed to send message to Telegram ({api_base}): {e}")
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python telegram_push.py \"Your message here\"")
        sys.exit(1)
        
    message = sys.argv[1]
    
    env_vars = load_env_config()
    token = env_vars.get("TELEGRAM_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN", "")
    api_base = env_vars.get("TELEGRAM_API_BASE_URL") or os.environ.get("TELEGRAM_API_BASE_URL", "https://api.telegram.org")
    proxy = env_vars.get("HTTPS_PROXY") or os.environ.get("HTTPS_PROXY") or env_vars.get("HTTP_PROXY") or os.environ.get("HTTP_PROXY")
    
    if not token:
        print("[Error] No Telegram Bot Token found in system/config/.env!")
        sys.exit(1)
        
    chat_id = get_chat_id()
    if not chat_id:
        print("[Error] Could not determine Chat ID. Ensure you have sent at least one message to the bot.")
        sys.exit(1)
        
    send_message(token, chat_id, message, api_base=api_base, proxy=proxy)

if __name__ == "__main__":
    main()
