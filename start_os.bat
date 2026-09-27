@echo off
title Nirixa Episteme OS - Master Launcher
cls
echo =========================================================
echo            NIRIXA EPISTEME OS - MASTER LAUNCHER          
echo =========================================================
echo [1/2] Starting Silent Background Telegram Mobile Listener...
wscript.exe "%~dp0system\scripts\start_silent_daemon.vbs"

echo [2/2] Launching Episteme OS Studio on Port 3000...
start "" "http://localhost:3000"
cd /d "%~dp0apps\episteme"
npm run dev

pause
