#!/usr/bin/env python3
"""
Nirixa OS Engine - Database Memory Core (DB-First Architecture & Reminders & Proactive Audits)
Single-file, zero-dependency SQLite memory store (system/data/nirixa.db).
Manages raw mobile captures, conversation threads, OTAs, System Evolution logs, Reminders, and Audit Logs.
"""

import os
import sqlite3
import datetime
import json

def get_db_path(workspace_root=None):
    if not workspace_root:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    data_dir = os.path.join(workspace_root, "system", "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "nirixa.db")

def init_db(db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Raw captures table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS raw_captures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        update_id TEXT UNIQUE,
        timestamp TEXT,
        chat_id TEXT,
        raw_text TEXT,
        anonymized_text TEXT,
        source TEXT DEFAULT 'telegram',
        status TEXT DEFAULT 'unread'
    )
    """)

    # Conversation threads table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversation_threads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        user_prompt TEXT,
        agent_reply TEXT,
        timestamp TEXT
    )
    """)

    # User profile & resume context table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_profile (
        key TEXT PRIMARY KEY,
        value TEXT,
        category TEXT DEFAULT 'general',
        updated_at TEXT
    );
    """)

    # Original Thought Assets (OTAs) table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS otas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        capture_id INTEGER,
        title TEXT,
        raw_thought TEXT,
        refined_thesis TEXT,
        draft_x TEXT,
        draft_linkedin TEXT,
        status TEXT DEFAULT 'drafting',
        created_at TEXT,
        updated_at TEXT
    )
    """)

    # System Self-Evolution Logs (RL Feedback Matrix)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evolution_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        capture_id INTEGER,
        rating INTEGER,
        feedback_text TEXT,
        rule_extracted TEXT,
        created_at TEXT
    )
    """)

    # Action Tasks Kanban Table (Active / Overdue / Completed & Velocity Tracking)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS action_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT DEFAULT '',
        source TEXT DEFAULT 'ide',
        deadline TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT,
        completed_at TEXT,
        turnaround_minutes INTEGER DEFAULT 0,
        completed_before_deadline INTEGER DEFAULT 1
    );
    """)

    # Reminders Table (Zero-LLM Deterministic Store)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        message TEXT,
        remind_at TEXT,
        status TEXT DEFAULT 'pending',
        created_at TEXT
    )
    """)

    # System Audit Logs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_audits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metric_name TEXT,
        metric_value TEXT,
        timestamp TEXT
    )
    """)

    # OTA Edges Table (Resonance Graph Connections)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ota_edges (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ota_id_a INTEGER,
        ota_id_b INTEGER,
        resonance_score REAL,
        created_at TEXT
    )
    """)

    # Product Outcomes & Performance Metrics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        metric_name TEXT,
        value REAL,
        timestamp TEXT
    )
    """)

    # Track A: System Health Eval Results
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS eval_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        eval_name TEXT,
        subsystem TEXT,
        status TEXT,
        detail TEXT,
        timestamp TEXT
    )
    """)

    # Track B: Capability Snapshots (Day 1 vs Day N)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS capability_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_date TEXT,
        active_skill_count INTEGER,
        active_skill_names TEXT,
        table_count INTEGER,
        rule_count INTEGER,
        eval_pass_rate REAL,
        total_otas INTEGER,
        total_captures INTEGER,
        notes TEXT
    )
    """)

    # Track C Part 2: Monthly Self-Assessments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS self_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        period TEXT,
        dimension TEXT,
        score INTEGER,
        note TEXT,
        timestamp TEXT
    )
    """)

    # Enable sqlite-vec vector table
    try:
        import sqlite_vec
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS vec_otas USING vec0(
            ota_id INTEGER PRIMARY KEY,
            embedding float[384]
        )
        """)
    except Exception as e:
        pass

    # FTS5 Full-Text Search Virtual Tables (Hermes L3 Episodic Memory Core)
    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS raw_captures_fts USING fts5(
        raw_text,
        anonymized_text,
        content=raw_captures,
        content_rowid=id
    )
    """)

    cursor.execute("""
    CREATE VIRTUAL TABLE IF NOT EXISTS conversation_threads_fts USING fts5(
        user_prompt,
        agent_reply,
        content=conversation_threads,
        content_rowid=id
    )
    """)

    # Auto-Sync Triggers for FTS5
    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS raw_captures_ai AFTER INSERT ON raw_captures BEGIN
        INSERT INTO raw_captures_fts(rowid, raw_text, anonymized_text) VALUES (new.id, new.raw_text, new.anonymized_text);
    END;
    """)

    cursor.execute("""
    CREATE TRIGGER IF NOT EXISTS conversation_threads_ai AFTER INSERT ON conversation_threads BEGIN
        INSERT INTO conversation_threads_fts(rowid, user_prompt, agent_reply) VALUES (new.id, new.user_prompt, new.agent_reply);
    END;
    """)

    # Initial Backfill for FTS5
    cursor.execute("INSERT INTO raw_captures_fts(raw_captures_fts) VALUES('rebuild')")
    cursor.execute("INSERT INTO conversation_threads_fts(conversation_threads_fts) VALUES('rebuild')")

    conn.commit()
    conn.close()

def is_update_processed(update_id, db_path=None):
    if not update_id:
        return False
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM raw_captures WHERE update_id = ?", (str(update_id),))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def save_capture(update_id, chat_id, raw_text, anonymized_text, source="telegram", db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        cursor.execute("""
        INSERT INTO raw_captures (update_id, timestamp, chat_id, raw_text, anonymized_text, source, status)
        VALUES (?, ?, ?, ?, ?, ?, 'unread')
        """, (str(update_id), now_str, str(chat_id), raw_text, anonymized_text, source))
        conn.commit()
        last_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        last_id = None
    finally:
        conn.close()
    return last_id

def save_thread_interaction(session_id, user_prompt, agent_reply, db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO conversation_threads (session_id, user_prompt, agent_reply, timestamp)
    VALUES (?, ?, ?, ?)
    """, (session_id, user_prompt, agent_reply, now_str))
    conn.commit()
    conn.close()

def save_ota(capture_id, title, raw_thought, refined_thesis="", draft_x="", draft_linkedin="", db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO otas (capture_id, title, raw_thought, refined_thesis, draft_x, draft_linkedin, status, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, 'refined', ?, ?)
    """, (capture_id, title, raw_thought, refined_thesis, draft_x, draft_linkedin, now_str, now_str))
    conn.commit()
    ota_id = cursor.lastrowid
    conn.close()
    return ota_id

def save_evolution_feedback(capture_id, rating, feedback_text="", rule_extracted="", db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO evolution_logs (capture_id, rating, feedback_text, rule_extracted, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (capture_id, rating, feedback_text, rule_extracted, now_str))
    conn.commit()
    conn.close()

def save_reminder(chat_id, message, remind_at_dt, db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    remind_at_str = remind_at_dt.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO reminders (chat_id, message, remind_at, status, created_at)
    VALUES (?, ?, ?, 'pending', ?)
    """, (str(chat_id), message, remind_at_str, now_str))
    conn.commit()
    rem_id = cursor.lastrowid
    conn.close()
    return rem_id, remind_at_str

def get_due_reminders(db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT id, chat_id, message, remind_at FROM reminders WHERE status = 'pending' AND remind_at <= ?", (now_str,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def mark_reminder_status(reminder_id, status="completed", db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("UPDATE reminders SET status = ? WHERE id = ?", (status, reminder_id))
    conn.commit()
    conn.close()

def snooze_reminder(reminder_id, minutes, db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    new_dt = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
    new_str = new_dt.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE reminders SET remind_at = ?, status = 'pending' WHERE id = ?", (new_str, reminder_id))
    conn.commit()
    conn.close()
    return new_str

def get_pending_reminders_summary(db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, message, remind_at FROM reminders WHERE status = 'pending' ORDER BY remind_at ASC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "No pending reminders."
    return "\n".join([f"• [{r[2]}] {r[1]}" for r in rows])

def get_proactive_briefing_data(db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM reminders WHERE status = 'pending'")
    pending_reminders = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM otas")
    total_otas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM raw_captures")
    total_captures = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(CASE WHEN rating > 0 THEN 1 ELSE 0 END), SUM(CASE WHEN rating < 0 THEN 1 ELSE 0 END) FROM evolution_logs")
    upvotes, downvotes = cursor.fetchone()
    upvotes = upvotes or 0
    downvotes = downvotes or 0

    conn.close()
    return {
        "pending_reminders": pending_reminders,
        "total_otas": total_otas,
        "total_captures": total_captures,
        "upvotes": upvotes,
        "downvotes": downvotes
    }

def get_recent_thread_history(limit=5, db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT user_prompt, agent_reply, timestamp FROM conversation_threads ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    formatted = []
    for u, a, ts in reversed(rows):
        formatted.append(f"Monish: {u}\nChief of Staff: {a}")
    return "\n\n".join(formatted) if formatted else "No prior thread history."

def get_active_evolution_rules(db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT rule_extracted FROM evolution_logs WHERE rule_extracted IS NOT NULL AND rule_extracted != '' ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "- Always maintain grounded, non-preachy co-founder tone.\n- Keep responses short (1-3 lines) unless requested otherwise."
    return "\n".join([f"- {r[0]}" for r in rows])

def get_recent_captures(limit=5, db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, anonymized_text, source FROM raw_captures ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_ota_summary(db_path=None):
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, status, created_at FROM otas ORDER BY id DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "No OTAs created yet."
    return "\n".join([f"• OTA #{r[0]}: {r[1]} [{r[2]}]" for r in rows])

def search_fts(query_text, limit=5, db_path=None):
    """Sub-millisecond BM25 FTS5 Full-Text Search Core (Hermes L3 Episodic Recall)"""
    if not query_text:
        return "Please specify a search term."
    if not db_path:
        db_path = get_db_path()
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Clean query string for FTS5 syntax safety
    clean_q = ' OR '.join([f'"{w}"' for w in query_text.replace('"', '').split() if len(w) > 1])
    if not clean_q:
        clean_q = f'"{query_text}"'
        
    results = []
    
    # 1. Search Raw Captures
    try:
        cursor.execute("""
        SELECT r.id, r.timestamp, r.anonymized_text, rank
        FROM raw_captures_fts f
        JOIN raw_captures r ON f.rowid = r.id
        WHERE raw_captures_fts MATCH ?
        ORDER BY rank LIMIT ?
        """, (clean_q, limit))
        for r in cursor.fetchall():
            results.append(f"📌 Captures [{r[1]}] (ID:{r[0]}): {r[2]}")
    except Exception as e:
        print(f"[FTS Search Warning Captures] {e}")

    # 2. Search Conversation Threads
    try:
        cursor.execute("""
        SELECT c.id, c.timestamp, c.user_prompt, c.agent_reply, rank
        FROM conversation_threads_fts f
        JOIN conversation_threads c ON f.rowid = c.id
        WHERE conversation_threads_fts MATCH ?
        ORDER BY rank LIMIT ?
        """, (clean_q, limit))
        for c in cursor.fetchall():
            results.append(f"💬 Thread [{c[1]}]: User: {c[2][:50]}... | System: {c[3][:50]}...")
    except Exception as e:
        print(f"[FTS Search Warning Threads] {e}")
        
    conn.close()
    
    if not results:
        return f"No records matching search query: '{query_text}'"
        
    return f"⚡ FTS5 MEMORY SEARCH RESULTS ('{query_text}'):\n" + "\n\n".join(results)

def log_audit_metric(metric_name, metric_value, db_path=None):
    """Writes an audit entry to the system_audits table."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO system_audits (metric_name, metric_value, timestamp)
    VALUES (?, ?, ?)
    """, (metric_name, str(metric_value), now_str))
    conn.commit()
    conn.close()

def record_heartbeat(db_path=None):
    """Records daemon_heartbeat timestamp in system_audits."""
    log_audit_metric("daemon_heartbeat", "alive", db_path)

def get_daily_delegator_pushes(db_path=None):
    """Returns the count of delegator pushes sent in the current calendar day."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    today_prefix = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor.execute("""
    SELECT COUNT(*) FROM evolution_logs
    WHERE rule_extracted = 'delegator_push' AND created_at LIKE ?
    """, (f"{today_prefix}%",))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def log_delegator_push_outcome(task_text, outcome, db_path=None):
    """Logs a delegator push and its outcome (sent, acted_on, dismissed, timed_out) into evolution_logs."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO evolution_logs (capture_id, rating, feedback_text, rule_extracted, created_at)
    VALUES (0, 0, ?, 'delegator_push', ?)
    """, (f"Outcome: {outcome} | Details: {task_text}", now_str))
    conn.commit()
    conn.close()

def get_7day_delegator_dismissal_rate(db_path=None):
    """Calculates the dismissal rate of delegator pushes over the trailing 7 days."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cutoff_str = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    cursor.execute("""
    SELECT feedback_text FROM evolution_logs
    WHERE rule_extracted = 'delegator_push' AND created_at >= ?
    """, (cutoff_str,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return 0.0
    dismissed = sum(1 for r in rows if "Outcome: dismissed" in r[0] or "Outcome: timed_out" in r[0])
    return dismissed / len(rows)

def record_self_assessment(period, dimension, score, note="", db_path=None):
    """Records a monthly 1-5 scale self-assessment in self_assessments."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO self_assessments (period, dimension, score, note, timestamp)
    VALUES (?, ?, ?, ?, ?)
    """, (period, dimension, int(score), note, now_str))
    conn.commit()
    conn.close()

def get_self_assessments(period=None, db_path=None):
    """Retrieves self-assessment records."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if period:
        cursor.execute("SELECT period, dimension, score, note, timestamp FROM self_assessments WHERE period = ?", (period,))
    else:
        cursor.execute("SELECT period, dimension, score, note, timestamp FROM self_assessments ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

def record_product_metric(metric_name, value, db_path=None):
    """Records a numerical product outcome metric in product_metrics."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO product_metrics (metric_name, value, timestamp)
    VALUES (?, ?, ?)
    """, (metric_name, float(value), now_str))
    conn.commit()
    conn.close()

def update_ota_status(ota_id, new_status, db_path=None):
    """Updates OTA status in otas table. If status changes to 'published', schedules 24h engagement check."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT title FROM otas WHERE id = ?", (ota_id,))
    row = cursor.fetchone()
    title = row[0] if row else f"OTA #{ota_id}"

    cursor.execute("UPDATE otas SET status = ? WHERE id = ?", (new_status, ota_id))
    conn.commit()
    conn.close()

    if new_status.lower() == "published":
        workspace_root = os.path.abspath(os.path.join(os.path.dirname(db_path), "..", ".."))
        try:
            import accountability
            acct = accountability.AccountabilityEngine(workspace_root=workspace_root)
            acct.schedule_publish_engagement_check(ota_id, title)
        except Exception as e:
            print(f"[DB Warning] Could not schedule engagement check for published OTA #{ota_id}: {e}")

        try:
            import sync
            sync.run_git_sync(workspace_root, commit_prefix=f"feat(publish): published OTA #{ota_id} ('{title[:30]}')")
        except Exception as e:
            print(f"[DB Warning] Publish Git sync failed: {e}")

def set_profile_key(key, value, category="general", db_path=None):
    """Inserts or updates a key-value profile attribute in user_profile table."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().isoformat()
    cursor.execute("""
    INSERT INTO user_profile (key, value, category, updated_at)
    VALUES (?, ?, ?, ?)
    ON CONFLICT(key) DO UPDATE SET value=excluded.value, category=excluded.category, updated_at=excluded.updated_at
    """, (key, str(value), category, now_str))
    conn.commit()
    conn.close()

def get_profile_context(category=None, db_path=None):
    """Returns a dict of stored user_profile attributes."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT key, value FROM user_profile WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT key, value FROM user_profile")
    rows = cursor.fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}

def get_user_profile(workspace_root=None):
    """Convenience accessor for Monish's complete profile and financial baseline."""
    db_path = get_db_path(workspace_root)
    ctx = get_profile_context(db_path=db_path)
    return {
        "monthly_salary": int(ctx.get("monthly_salary", 67000)),
        "monthly_rent": int(ctx.get("monthly_rent", 15000)),
        "monthly_parents": int(ctx.get("monthly_parents", 10000)),
        "monthly_living_estimate": int(ctx.get("monthly_living_estimate", 15000)),
        "liquid_armor_balance": int(ctx.get("liquid_armor_balance", 20000)),
        "user_name": ctx.get("user_name", "Monish Nallagondalla"),
        "wife_name": ctx.get("wife_name", "Harshitha"),
        "user_dob": ctx.get("user_dob", "1996-01-09"),
        "wife_dob": ctx.get("wife_dob", "1997-04-14")
    }

def add_action_task(title, deadline_str=None, source="ide", description="", db_path=None):
    """Inserts a new actionable task with a deadline."""
    if not db_path:
        db_path = get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not deadline_str:
        # Default: 24h from now
        deadline_str = (datetime.datetime.now() + datetime.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M:%S")
        
    cursor.execute("""
    INSERT INTO action_tasks (title, description, source, deadline, status, created_at)
    VALUES (?, ?, ?, ?, 'pending', ?)
    """, (title.strip(), description.strip(), source, deadline_str, now_str))
    task_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return task_id

def get_action_tasks_grouped(db_path=None):
    """
    Retrieves all tasks, auto-evaluates overdue status against current time,
    groups into active, overdue, completed, and calculates velocity metrics.
    """
    if not db_path:
        db_path = get_db_path()
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("SELECT id, title, description, source, deadline, status, created_at, completed_at, turnaround_minutes, completed_before_deadline FROM action_tasks ORDER BY id DESC")
    rows = cursor.fetchall()
    
    active = []
    overdue = []
    completed = []
    
    for r in rows:
        tid, title, desc, src, dline, stat, cat, comp_at, t_min, on_time = r
        task_obj = {
            "id": tid, "title": title, "description": desc, "source": src,
            "deadline": dline, "status": stat, "created_at": cat,
            "completed_at": comp_at, "turnaround_minutes": t_min,
            "completed_before_deadline": on_time
        }
        
        if stat == "completed":
            completed.append(task_obj)
        else:
            # Check if deadline passed
            if dline and dline < now_str:
                task_obj["status"] = "overdue"
                overdue.append(task_obj)
            else:
                active.append(task_obj)
                
    conn.close()
    
    total_completed = len(completed)
    on_time_count = sum(1 for c in completed if c.get("completed_before_deadline") == 1)
    on_time_pct = round((on_time_count / total_completed * 100), 1) if total_completed > 0 else 100.0
    avg_turnaround_hrs = round(sum(c.get("turnaround_minutes", 0) for c in completed) / (total_completed * 60), 1) if total_completed > 0 else 0.0
    
    return {
        "active": active,
        "overdue": overdue,
        "completed": completed[:15],
        "velocity_metrics": {
            "total_completed": total_completed,
            "completed_on_time_pct": on_time_pct,
            "avg_turnaround_hours": avg_turnaround_hrs,
            "velocity_score": f"{on_time_pct}% On-Time"
        }
    }

def complete_action_task(task_id, db_path=None):
    """
    Marks task as completed, computes exact turnaround minutes,
    evaluates whether it beat the deadline, and logs velocity to Track C.
    """
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    now_dt = datetime.datetime.now()
    now_str = now_dt.strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute("SELECT created_at, deadline FROM action_tasks WHERE id = ?", (task_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False
        
    created_at_str, deadline_str = row
    turnaround_mins = 60
    if created_at_str:
        try:
            c_dt = datetime.datetime.fromisoformat(created_at_str)
            turnaround_mins = max(1, int((now_dt - c_dt).total_seconds() / 60))
        except Exception:
            pass
            
    completed_before_deadline = 1
    if deadline_str and deadline_str < now_str:
        completed_before_deadline = 0
        
    cursor.execute("""
    UPDATE action_tasks
    SET status = 'completed', completed_at = ?, turnaround_minutes = ?, completed_before_deadline = ?
    WHERE id = ?
    """, (now_str, turnaround_mins, completed_before_deadline, task_id))
    conn.commit()
    conn.close()
    return True

def delete_action_task(task_id, db_path=None):
    """Permanently removes a task."""
    if not db_path:
        db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM action_tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return True

if __name__ == "__main__":
    init_db()
    print("[Nirixa DB Core] Initialized DB-First memory core at system/data/nirixa.db")


