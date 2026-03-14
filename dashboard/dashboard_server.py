#!/usr/bin/env python3
"""
My-OS Local Dashboard Server - Read-Only Telemetry & Analytics Backend
Serves single-page HTML frontend and provides read-only JSON API endpoints reading directly from system/data/nirixa.db.
"""

import os
import sys
import json
import sqlite3
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.insert(0, os.path.join(workspace_root, "system", "engine"))

import db
import accountability

PORT = 8000

class DashboardRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=script_dir, **kwargs)

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/api/stats":
            try:
                stats_data = self.get_dashboard_stats()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(stats_data).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path == "/api/record_post_metric":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            try:
                data = json.loads(body.decode("utf-8"))
                metric_name = data.get("metric_name", "linkedin_performance")
                val = float(data.get("value", 0))
                db_path = db.get_db_path(workspace_root)
                db.record_product_metric(metric_name, val, db_path=db_path)
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "message": "Metric recorded"}).encode("utf-8"))
            except Exception as e:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))
        else:
            self.send_error(404)

    def get_dashboard_stats(self):
        db_path = db.get_db_path(workspace_root)
        db.init_db(db_path)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Panel 1: Status Strip
        cursor.execute("SELECT timestamp FROM system_audits WHERE metric_name = 'daemon_heartbeat' ORDER BY id DESC LIMIT 1")
        row_hb = cursor.fetchone()
        daemon_alive = False
        daemon_detail = "Offline"

        try:
            import psutil
            for proc in psutil.process_iter(['name', 'cmdline']):
                try:
                    proc_name = (proc.info.get('name') or '').lower()
                    cmdline = proc.info.get('cmdline') or []
                    cmd_str = " ".join([str(c) for c in cmdline if c]).lower()
                    if "python" in proc_name and ("daemon.py" in cmd_str or "telegram_daemon.py" in cmd_str) and "dashboard_server" not in cmd_str:
                        daemon_alive = True
                        daemon_detail = f"Live Process (PID {proc.pid})"
                        break
                except Exception:
                    continue
        except Exception:
            pass

        if not daemon_alive and row_hb:
            try:
                ts_clean = str(row_hb[0]).split("+")[0].replace("Z", "")
                last_hb = datetime.datetime.fromisoformat(ts_clean)
                diff_min = (datetime.datetime.now() - last_hb).total_seconds() / 60.0
                daemon_detail = f"Last Heartbeat ({round(diff_min, 1)}m ago)"
            except Exception:
                pass

        cursor.execute("SELECT detail FROM eval_results WHERE eval_name = 'eval_suite_rollup' ORDER BY id DESC LIMIT 1")
        row_eval = cursor.fetchone()
        eval_pass_rate = "N/A"
        if row_eval:
            val = row_eval[0]
            if ":" in val:
                eval_pass_rate = val.split(":")[1].split("(")[0].strip()
            else:
                eval_pass_rate = val

        cursor.execute("SELECT MAX(created_at) FROM otas WHERE status = 'published'")
        row_pub = cursor.fetchone()
        days_since_publish = "N/A"
        if row_pub and row_pub[0]:
            try:
                pub_clean = str(row_pub[0]).split("+")[0].replace("Z", "")
                last_pub = datetime.datetime.fromisoformat(pub_clean)
                days_diff = (datetime.datetime.now() - last_pub).days
                days_since_publish = f"{days_diff}d ago"
            except Exception:
                days_since_publish = "Recent"

        # Panel 2: Accountability & Nudges
        acct = accountability.AccountabilityEngine(workspace_root=workspace_root)
        stale_drafts = acct.check_stale_drafts()
        overdue_reminders = acct.check_overdue_reminders()
        
        cursor.execute("""
        SELECT r.id, r.message, r.remind_at FROM reminders r
        WHERE r.status = 'pending' AND r.message LIKE '%24h Engagement Follow-Up%'
        """)
        pub_no_followup = [{"id": r[0], "text": r[1], "due": r[2]} for r in cursor.fetchall()]

        # Panel 3: Content & LinkedIn
        cursor.execute("SELECT status, COUNT(*) FROM otas GROUP BY status")
        ota_counts = {r[0]: r[1] for r in cursor.fetchall()}

        cursor.execute("SELECT metric_name, value, timestamp FROM product_metrics ORDER BY id DESC LIMIT 10")
        recent_product_metrics = [{"metric": r[0], "value": r[1], "ts": r[2]} for r in cursor.fetchall()]

        # Panel 4: System Health
        cursor.execute("SELECT subsystem, status, detail FROM eval_results WHERE eval_name != 'eval_suite_rollup' ORDER BY id DESC LIMIT 8")
        subsystem_evals = [{"subsystem": r[0], "status": r[1], "detail": r[2]} for r in cursor.fetchall()]

        cursor.execute("SELECT metric_name, metric_value, timestamp FROM system_audits WHERE metric_name IN ('daemon_crash', 'daemon_restart', 'reasoning_backend_fallback') ORDER BY id DESC LIMIT 10")
        audit_events = [{"event": r[0], "value": r[1], "ts": r[2]} for r in cursor.fetchall()]

        # Panel 5: Personal Growth
        cursor.execute("SELECT period, dimension, score, note, timestamp FROM self_assessments ORDER BY id DESC LIMIT 10")
        self_assessments = [{"period": r[0], "dimension": r[1], "score": r[2], "note": r[3], "ts": r[4]} for r in cursor.fetchall()]

        # Panel 6: Evolution Snapshots
        cursor.execute("SELECT snapshot_date, active_skill_count, table_count, rule_count, eval_pass_rate, total_otas, total_captures FROM capability_snapshots ORDER BY id ASC")
        snapshots = [{"date": r[0], "skills": r[1], "tables": r[2], "rules": r[3], "pass_rate": r[4], "otas": r[5], "captures": r[6]} for r in cursor.fetchall()]

        # Panel 7: Inbox & Captures
        cursor.execute("SELECT COUNT(*) FROM raw_captures WHERE status = 'unread'")
        unprocessed_count = cursor.fetchone()[0]

        cursor.execute("SELECT id, timestamp, source, raw_text FROM raw_captures ORDER BY id DESC LIMIT 10")
        recent_captures = [{"id": r[0], "ts": r[1], "source": r[2], "text": r[3]} for r in cursor.fetchall()]

        conn.close()

        return {
            "status_strip": {
                "daemon_alive": daemon_alive,
                "daemon_detail": daemon_detail,
                "eval_pass_rate": eval_pass_rate,
                "pending_nudges_count": len(stale_drafts) + len(overdue_reminders),
                "days_since_publish": days_since_publish
            },
            "accountability": {
                "stale_drafts": stale_drafts,
                "overdue_reminders": overdue_reminders,
                "pub_no_followup": pub_no_followup
            },
            "content": {
                "ota_counts": ota_counts,
                "recent_product_metrics": recent_product_metrics
            },
            "system_health": {
                "subsystem_evals": subsystem_evals,
                "audit_events": audit_events
            },
            "personal_growth": {
                "self_assessments": self_assessments
            },
            "evolution": {
                "snapshots": snapshots
            },
            "inbox": {
                "unprocessed_count": unprocessed_count,
                "recent_captures": recent_captures
            }
        }

def run_server():
    server_address = ("", PORT)
    httpd = HTTPServer(server_address, DashboardRequestHandler)
    print(f"==================================================")
    print(f"  MY-OS TELEMETRY & ANALYTICS DASHBOARD RUNNING")
    print(f"==================================================")
    print(f"Access Dashboard locally at: http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Dashboard Server...")

if __name__ == "__main__":
    run_server()
