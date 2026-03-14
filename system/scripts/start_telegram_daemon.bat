@echo off
title Nirixa OS Telegram Engine Daemon
echo ==================================================
echo   STARTING NIRIXA OS TELEGRAM DAEMON (SQLITE CORE)
echo ==================================================
cd /d "%~dp0\..\.."
python system\engine\daemon.py
pause
