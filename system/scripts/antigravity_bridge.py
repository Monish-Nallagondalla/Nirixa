import os
import sys
import time
import json
import urllib.request
import urllib.parse
import threading

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

def send_message(token, chat_id, text, api_base, proxy):
    url = f"{api_base.rstrip('/')}/bot{token}/sendMessage"
    opener = build_opener(proxy)
    payload = {"chat_id": chat_id, "text": text}
    try:
        data_bytes = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
        with opener.open(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[Error sending] {e}", flush=True)

def telegram_poller(token, api_base, proxy):
    offset = 0
    opener = build_opener(proxy)
    while True:
        try:
            url = f"{api_base.rstrip('/')}/bot{token}/getUpdates?offset={offset}&timeout=10"
            req = urllib.request.Request(url)
            with opener.open(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("ok"):
                    for upd in data.get("result", []):
                        offset = upd["update_id"] + 1
                        msg = upd.get("message")
                        if not msg: continue
                        chat_id = msg.get("chat", {}).get("id")
                        text = msg.get("text", "")
                        if text:
                            # Print explicitly for Antigravity to parse
                            print(f"[TELEGRAM_IN] chat_id={chat_id} | message={text}", flush=True)
        except Exception as e:
            time.sleep(2)

def stdin_listener(token, api_base, proxy):
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                chat_id = data.get("chat_id")
                text = data.get("text")
                if chat_id and text:
                    send_message(token, chat_id, text, api_base, proxy)
                    print(f"[Bridge] Sent reply to {chat_id}", flush=True)
            except json.JSONDecodeError:
                print(f"[Bridge Error] Invalid JSON received on stdin: {line}", flush=True)
        except Exception as e:
            print(f"[Bridge Error] stdin listener exception: {e}", flush=True)
            break

if __name__ == "__main__":
    # Disable buffering to ensure we print immediately
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except AttributeError:
        pass # python < 3.7
    
    env_vars, root = load_config()
    token = env_vars.get("TELEGRAM_BOT_TOKEN")
    api_base = env_vars.get("TELEGRAM_API_BASE_URL", "https://api.telegram.org")
    proxy = env_vars.get("HTTPS_PROXY") or env_vars.get("HTTP_PROXY")
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN missing in .env", flush=True)
        sys.exit(1)
        
    print("[Bridge] Started Antigravity Telegram Bridge. Waiting for messages...", flush=True)
    
    t1 = threading.Thread(target=telegram_poller, args=(token, api_base, proxy), daemon=True)
    t2 = threading.Thread(target=stdin_listener, args=(token, api_base, proxy), daemon=True)
    
    t1.start()
    t2.start()
    
    while True:
        time.sleep(1)
