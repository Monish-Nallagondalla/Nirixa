@echo off
:: Process Terminator for Nirixa OS Telegram Daemon
echo Terminating Nirixa Telegram Daemon process...

powershell -Command "$procs = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*telegram_daemon.py*' }; if ($procs) { foreach ($p in $procs) { Stop-Process -Id $p.ProcessId -Force; Write-Host ('Stopped daemon PID ' + $p.ProcessId) } } else { Write-Host 'No running daemon process found.' }"

echo [Success] Daemon stopped.
