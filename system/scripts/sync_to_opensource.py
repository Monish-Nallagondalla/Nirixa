#!/usr/bin/env python3
"""
Nirixa OS - Dual-Repo Automated Open-Source Mirror Engine
Mirrors engine code, custom skills, dashboard, and documentation from My-Os into nirixa-open-source/
while enforcing strict air-gap data security (excluding private databases, personal notes, API keys).
"""

import os
import sys
import shutil

EXCLUDE_DIRS = {
    "system/data",
    "personal",
    "archive",
    "journal",
    ".git",
    "__pycache__",
    ".pytest_cache"
}

EXCLUDE_FILES = {
    ".env",
    "nirixa.db",
    "synced_messages.json"
}

EXCLUDE_EXTENSIONS = {
    ".db",
    ".db-journal",
    ".key",
    ".pem"
}

def is_excluded(rel_path):
    rel_path_normalized = rel_path.replace("\\", "/")
    
    # Check directory exclusion
    for ex_dir in EXCLUDE_DIRS:
        if rel_path_normalized == ex_dir or rel_path_normalized.startswith(ex_dir + "/"):
            return True
            
    # Check file exclusion
    filename = os.path.basename(rel_path)
    if filename in EXCLUDE_FILES:
        return True
        
    ext = os.path.splitext(filename)[1].lower()
    if ext in EXCLUDE_EXTENSIONS:
        return True
        
    # Exclude raw inbox markdown notes (except README.md)
    if rel_path_normalized.startswith("inbox/") and filename != "README.md":
        return True
        
    return False

def mirror_to_opensource(workspace_root=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if not workspace_root:
        workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

    target_dir = os.path.join(workspace_root, "nirixa-open-source")
    os.makedirs(target_dir, exist_ok=True)

    print("=========================================================")
    print("        NIRIXA OS - DUAL-REPO MIRROR ENGINE              ")
    print("=========================================================")
    print(f"Source Workspace: {workspace_root}")
    print(f"Target OS Repo  : {target_dir}")
    print("---------------------------------------------------------")

    copied_count = 0
    skipped_count = 0

    for root, dirs, files in os.walk(workspace_root):
        # Exclude target dir itself from walk
        if "nirixa-open-source" in root:
            continue

        rel_root = os.path.relpath(root, workspace_root)
        if rel_root == ".":
            rel_root = ""

        # Filter subdirectories in-place
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(rel_root, d))]

        for file in files:
            rel_file_path = os.path.join(rel_root, file) if rel_root else file
            
            if is_excluded(rel_file_path):
                skipped_count += 1
                continue

            src_file = os.path.join(root, file)
            dest_file = os.path.join(target_dir, rel_file_path)

            os.makedirs(os.path.dirname(dest_file), exist_ok=True)
            shutil.copy2(src_file, dest_file)
            copied_count += 1

    print(f"[PASS] Mirror Complete! {copied_count} files copied to nirixa-open-source/ ({skipped_count} private data files air-gap excluded).")
    print("=========================================================\n")
    return copied_count, skipped_count

if __name__ == "__main__":
    mirror_to_opensource()
