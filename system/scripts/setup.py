#!/usr/bin/env python3
"""
Nirixa OS - One-Command Automated Setup & Initialization Script
Initializes directories, creates clean SQLite database, verifies dependencies, and generates .env.
"""

import os
import sys
import shutil

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
    sys.path.insert(0, os.path.join(workspace_root, "system", "engine"))

    print("=========================================================")
    print("        🚀 NIRIXA OS - SYSTEM INITIALIZATION 🚀          ")
    print("=========================================================")
    print(f"[1/4] Workspace Root: {workspace_root}")

    # 1. Create required directories
    required_dirs = [
        os.path.join(workspace_root, "system", "data"),
        os.path.join(workspace_root, "system", "config"),
        os.path.join(workspace_root, "inbox"),
        os.path.join(workspace_root, "content", "linkedin"),
        os.path.join(workspace_root, "content", "twitter"),
        os.path.join(workspace_root, "personal"),
        os.path.join(workspace_root, "dashboard")
    ]
    for d in required_dirs:
        os.makedirs(d, exist_ok=True)
    print("[2/4] Directory hierarchy verified.")

    # 2. Setup .env file if missing
    env_file = os.path.join(workspace_root, ".env")
    env_example = os.path.join(workspace_root, ".env.example")
    if not os.path.exists(env_file) and os.path.exists(env_example):
        shutil.copyfile(env_example, env_file)
        print("[3/4] Created .env from .env.example (Please add your TELEGRAM_BOT_TOKEN and GEMINI_API_KEY).")
    else:
        print("[3/4] .env configuration file exists.")

    # 3. Initialize SQLite DB-First Core
    try:
        import db
        db_path = db.get_db_path(workspace_root)
        db.init_db(db_path)
        print(f"[4/4] SQLite DB-First Memory Core initialized at {db_path}.")
    except Exception as e:
        print(f"[Error] Database initialization failed: {e}")
        sys.exit(1)

    print("\n=========================================================")
    print("✅ NIRIXA OS INITIALIZATION COMPLETE!")
    print("---------------------------------------------------------")
    print("Next steps:")
    print("1. Edit '.env' with your Telegram Token and Gemini API Key.")
    print("2. Run 'python system/scripts/telegram_daemon.py' to start the mobile daemon.")
    print("3. Run 'python dashboard/dashboard_server.py' to launch local dashboard.")
    print("=========================================================\n")

if __name__ == "__main__":
    main()
