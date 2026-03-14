@echo off
:: Enable Auto-Start on Windows Startup for Nirixa OS Telegram Daemon
set SCRIPT_DIR=%~dp0
set TARGET_BAT=%SCRIPT_DIR%start_daemon.bat
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set LNK_PATH=%STARTUP_DIR%\NirixaTelegramDaemon.lnk

echo Setting up Auto-Start on Windows Login...

powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%LNK_PATH%');$s.TargetPath='%TARGET_BAT%';$s.WorkingDirectory='%SCRIPT_DIR%..\..';$s.WindowStyle=7;$s.Save()"

if exist "%LNK_PATH%" (
    echo [Success] Auto-start shortcut created successfully at:
    echo %LNK_PATH%
) else (
    echo [Error] Failed to create shortcut.
)
