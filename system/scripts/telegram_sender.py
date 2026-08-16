import os
import sys
import json
import urllib.request
import urllib.parse
import argparse

def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    env_path = os.path.join(workspace_root, "system", "config", ".env")

    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()
    return env_vars, workspace_root

def build_opener(proxy=None):
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}))
    return urllib.request.build_opener(*handlers)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chat_id", required=True)
    parser.add_argument("--text", required=True)
    parser.add_argument("--keyboard", required=False, help="JSON string for inline keyboard")
    args = parser.parse_args()

    env_vars, root = load_config()
    token = env_vars.get("TELEGRAM_BOT_TOKEN")
    api_base = env_vars.get("TELEGRAM_API_BASE_URL", "https://api.telegram.org")
    proxy = env_vars.get("HTTPS_PROXY") or env_vars.get("HTTP_PROXY")
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN missing in .env", flush=True)
        sys.exit(1)

    url = f"{api_base.rstrip('/')}/bot{token}/sendMessage"
    opener = build_opener(proxy)
    payload = {"chat_id": args.chat_id, "text": args.text}
    if args.keyboard:
        try:
            kb = json.loads(args.keyboard)
            payload["reply_markup"] = {"inline_keyboard": kb}
        except Exception as e:
            print(f"[Warning] Failed to parse keyboard json: {e}")

    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
        with opener.open(req, timeout=10) as resp:
            print(f"Message sent successfully to {args.chat_id}")
            sys.exit(0)
    except Exception as e:
        print(f"[Error sending] {e}", flush=True)
        sys.exit(1)
