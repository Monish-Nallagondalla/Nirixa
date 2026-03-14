@echo off
:: Disable Auto-Start and Stop Nirixa OS Telegram Daemon
set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set LNK_PATH=%STARTUP_DIR%\NirixaTelegramDaemon.lnk

echo Removing Auto-Start shortcut...

if exist "%LNK_PATH%" (
    del /f /q "%LNK_PATH%"
    echo [Success] Auto-start shortcut removed.
) else (
    echo [Notice] Shortcut was not present in Startup folder.
)

call "%~dp0stop_daemon.bat"
