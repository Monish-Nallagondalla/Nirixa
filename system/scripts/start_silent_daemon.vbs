Set WshShell = CreateObject("WScript.Shell")
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
workspaceRoot = CreateObject("Scripting.FileSystemObject").GetParentFolderName(CreateObject("Scripting.FileSystemObject").GetParentFolderName(scriptDir))
cmd = "pythonw """ & workspaceRoot & "\system\scripts\telegram_daemon.py"""
WshShell.Run cmd, 0, False
