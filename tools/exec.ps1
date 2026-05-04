# exec.ps1 — PS7 komut yonlendirici
# Kullanim: .\tools\exec.ps1 "cd path && command1 && command2"
param([string]$Command)

if (-not $Command) {
    Write-Host "Kullanim: .\tools\exec.ps1 ""cd path && command"""
    exit 1
}

& "C:\Program Files\PowerShell\7\pwsh.exe" -NoProfile -Command $Command
