#!/usr/bin/env python3
"""
Installs the Windows Startup shortcut for Nirixa OS Silent Daemon.
"""

import os
import sys
import subprocess

script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "..", ".."))

vbs_path = os.path.join(workspace_root, "system", "scripts", "start_silent_daemon.vbs")
appdata = os.environ.get("APPDATA", "")
startup_dir = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
lnk_path = os.path.join(startup_dir, "NirixaTelegramDaemon.lnk")

ps_script = f"""
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{lnk_path}')
$Shortcut.TargetPath = 'wscript.exe'
$Shortcut.Arguments = '"{vbs_path}"'
$Shortcut.WorkingDirectory = '{workspace_root}'
$Shortcut.WindowStyle = 7
$Shortcut.Save()
"""

try:
    os.makedirs(startup_dir, exist_ok=True)
    subprocess.run(["powershell", "-Command", ps_script], check=True)
    print(f"[Success] Created Windows Startup shortcut at: {lnk_path}")
except Exception as e:
    print(f"[Error] Could not create startup shortcut: {e}")
