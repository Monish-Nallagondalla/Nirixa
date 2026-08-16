import os
import sys
import time
import json
import urllib.request
import urllib.parse
import subprocess

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

def enforce_singleton(root):
    """Ensures only ONE instance of telegram_listener runs at any time to prevent duplicate message consumption."""
    pid_file = os.path.join(root, "system", "data", "listener.pid")
    my_pid = os.getpid()
    if os.path.exists(pid_file):
        try:
            with open(pid_file, "r") as f:
                old_pid = int(f.read().strip())
            if old_pid != my_pid:
                # Terminate stale listener if still alive
                try:
                    import signal
                    os.kill(old_pid, signal.SIGTERM)
                except Exception:
                    pass
        except Exception:
            pass
    try:
        with open(pid_file, "w") as f:
            f.write(str(my_pid))
    except Exception:
        pass

def build_opener(proxy=None):
    handlers = []
    if proxy:
        handlers.append(urllib.request.ProxyHandler({'http': proxy, 'https': proxy}))
    return urllib.request.build_opener(*handlers)

# Import DB, Sync, Anonymizer, and Send Status
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from system.engine import db
from system.engine import synthesizer
from system.engine import anonymizer
from system.scripts import sync
from system.scripts import send_status

if __name__ == "__main__":
    env_vars, root = load_config()
    enforce_singleton(root)

    token = env_vars.get("TELEGRAM_BOT_TOKEN")
    api_base = env_vars.get("TELEGRAM_API_BASE_URL", "https://api.telegram.org")
    proxy = env_vars.get("HTTPS_PROXY") or env_vars.get("HTTP_PROXY")
    
    if not token:
        print("Error: TELEGRAM_BOT_TOKEN missing in .env", flush=True)
        sys.exit(1)
        
    offset_file = os.path.join(root, "system", "data", "telegram_offset.txt")
    offset = 0
    if os.path.exists(offset_file):
        try:
            with open(offset_file, "r") as f:
                offset = int(f.read().strip())
        except Exception:
            pass

    opener = build_opener(proxy)
    sender_script = os.path.join(root, "system", "scripts", "telegram_sender.py")

    # Polling Loop
    while True:
        try:
            url = f"{api_base.rstrip('/')}/bot{token}/getUpdates?offset={offset}&timeout=20"
            req = urllib.request.Request(url)
            with opener.open(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("ok"):
                    for upd in data.get("result", []):
                        offset = upd["update_id"] + 1
                        
                        # Save offset immediately so we don't process it again
                        with open(offset_file, "w") as f:
                            f.write(str(offset))

                        cbq = upd.get("callback_query")
                        if cbq:
                            cb_id = cbq.get("id")
                            cb_data = cbq.get("data", "")
                            chat_id = cbq.get("message", {}).get("chat", {}).get("id")
                            
                            # Acknowledge callback immediately
                            try:
                                ack_url = f"{api_base.rstrip('/')}/bot{token}/answerCallbackQuery"
                                ack_payload = {"callback_query_id": cb_id}
                                ack_req = urllib.request.Request(
                                    ack_url, 
                                    data=json.dumps(ack_payload).encode("utf-8"), 
                                    headers={"Content-Type": "application/json"}
                                )
                                urllib.request.urlopen(ack_req, timeout=5)
                            except Exception:
                                pass

                            # Instant Local Handling for status_0 (200ms latency)
                            if cb_data == "status_0":
                                send_status.send_status(str(chat_id))
                                print(f"[Instant Telemetry] Dispatched live status to {chat_id}", flush=True)
                                continue

                            # Instant Sleep Handling
                            if cb_data == "sys_sleep":
                                ps_cmd = 'Add-Type -Assembly System.Windows.Forms; [System.Windows.Forms.Application]::SetSuspendState("Suspend", $false, $false)'
                                subprocess.Popen(["powershell", "-Command", ps_cmd])
                                subprocess.Popen([sys.executable, sender_script, "--chat_id", str(chat_id), "--text", "Laptop is going to sleep. Good night!"])
                                print(f"[TELEGRAM_IN] chat_id={chat_id} | message=[SYSTEM_SLEEP_TRIGGERED]", flush=True)
                                sys.exit(0)

                            # Pass all other rich button events to Antigravity IDE agent
                            print(f"[TELEGRAM_IN] chat_id={chat_id} | message=[BUTTON] {cb_data}", flush=True)
                            sys.exit(0)

                        msg = upd.get("message")
                        if not msg: continue
                        chat_id = msg.get("chat", {}).get("id")
                        text = msg.get("text", "")
                        if text:
                            # DB Sync
                            try:
                                anon_text = anonymizer.apply_anonymization(text)
                                c_id = db.save_capture(upd["update_id"], chat_id, text, anon_text, source="telegram-listener") or 0
                                synthesizer.synthesize_topics(root)
                                sync.append_thought_to_monthly_log(anon_text, source="telegram", root_path=root)
                                m_id = msg.get("message_id")
                                if chat_id and m_id:
                                    sync.record_synced_message(root, chat_id, m_id)
                            except Exception as db_err:
                                print(f"[DB Sync Warning] {db_err}", flush=True)
                                
                            text_lower = text.lower()
                            if "good night" in text_lower or text_lower.strip() == "sleep":
                                kb = [[{"text": "Put Laptop to Sleep", "callback_data": "sys_sleep"}]]
                                subprocess.Popen([sys.executable, sender_script, "--chat_id", str(chat_id), "--text", "Would you like me to put the laptop to sleep?", "--keyboard", json.dumps(kb)])

                            # Print explicitly for Antigravity to parse and EXIT
                            print(f"[TELEGRAM_IN] chat_id={chat_id} | message={text}", flush=True)
                            sys.exit(0)
        except Exception as e:
            time.sleep(1)
