$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot
$Python = Join-Path $ProjectRoot ".venv311\Scripts\python.exe"
$env:PYTHONPATH = "$ProjectRoot\backend;$ProjectRoot"
Write-Host "Starting QSR API at http://127.0.0.1:8000" -ForegroundColor Cyan
& $Python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000
