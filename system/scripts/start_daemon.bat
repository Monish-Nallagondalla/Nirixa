@echo off
:: Silent Background Launcher for Nirixa OS Telegram Daemon
set SCRIPT_DIR=%~dp0
set WORKSPACE_ROOT=%SCRIPT_DIR%..\..
cd /d "%WORKSPACE_ROOT%"

:: Check if already running
powershell -NoProfile -Command "$proc = Get-WmiObject Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine.Contains('telegram_daemon.py') }; if ($proc) { exit 1 } else { exit 0 }"
if %errorlevel% equ 1 (
    echo [Notice] Nirixa Telegram Daemon is already running.
    exit /b 0
)

echo Launching Nirixa Telegram Daemon in background...
start "" pythonw system/scripts/telegram_daemon.py
echo [Success] Daemon started silently!
