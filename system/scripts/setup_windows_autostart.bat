@echo off
title Setup Nirixa OS Windows Startup
echo ==================================================
echo   SETTING UP NIRIXA OS SILENT WINDOWS AUTOSTART
echo ==================================================

set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "VBS_PATH=%~dp0start_silent_daemon.vbs"

copy /y "%VBS_PATH%" "%STARTUP_DIR%\start_nirixa_daemon.vbs" >nul

echo [Success] Nirixa OS daemon added to Windows Startup folder.
echo It will now run automatically in the background whenever your laptop turns on!
echo.
pause
