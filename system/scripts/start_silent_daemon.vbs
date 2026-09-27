Set WshShell = CreateObject("WScript.Shell")
scriptDir = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
workspaceRoot = CreateObject("Scripting.FileSystemObject").GetParentFolderName(CreateObject("Scripting.FileSystemObject").GetParentFolderName(scriptDir))
cmd = "python """ & workspaceRoot & "\system\scripts\telegram_listener.py"""
WshShell.Run cmd, 0, False
