$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location (Join-Path $ProjectRoot "frontend")
Write-Host "Starting QSR frontend at http://127.0.0.1:5173" -ForegroundColor Cyan
& npm.cmd run dev -- --host 127.0.0.1
