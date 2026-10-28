$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
$Python = Join-Path $ProjectRoot ".venv311\Scripts\python.exe"
$env:PYTHONPATH = "$ProjectRoot\backend;$ProjectRoot"
Write-Host "Starting QSR analytics worker. Keep this window open." -ForegroundColor Cyan
& $Python -m app.worker
