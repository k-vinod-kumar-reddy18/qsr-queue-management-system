$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host " QSR Queue Management System - Local Windows" -ForegroundColor Cyan
Write-Host "             Docker is NOT used" -ForegroundColor Cyan
Write-Host "===============================================`n" -ForegroundColor Cyan

if (-not (Get-Command py -ErrorAction SilentlyContinue)) { throw "Python launcher 'py' was not found. Install Python 3.11 and enable the Python launcher." }
if (-not (Get-Command npm.cmd -ErrorAction SilentlyContinue)) { throw "Node.js/npm was not found. Install Node.js LTS, then reopen PowerShell." }
try { py -3.11 --version } catch { throw "Python 3.11 is required. Install Python 3.11 and retry." }

if (-not (Test-Path ".env")) {
    Copy-Item ".env.local.example" ".env"
    $bytes = New-Object byte[] 32
    [Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    $secret = ([BitConverter]::ToString($bytes)).Replace("-", "").ToLowerInvariant()
    (Get-Content ".env" -Raw).Replace("REPLACE_ME_WITH_RANDOM_SECRET", $secret) | Set-Content ".env" -Encoding ascii
    Write-Host "Created local .env using SQLite. No PostgreSQL or Docker is required." -ForegroundColor Yellow
}

# Translate container-only paths into local relative paths when a Docker-era .env was copied here.
$envText = Get-Content ".env" -Raw
$envText = $envText.Replace("/app/videos/input", "./videos/input").Replace("/app/videos/processed", "./videos/processed").Replace("/app/evidence", "./evidence").Replace("/app/vision/models/yolo11n.pt", "./vision/models/yolo11n.pt")
$envText = $envText -replace '(?m)^POSTGRES_HOST=db\s*$', 'POSTGRES_HOST=localhost'
$envText = $envText -replace '@db:', '@localhost:'
Set-Content ".env" $envText -Encoding ascii

New-Item -ItemType Directory -Force "videos/input","videos/processed","evidence/snapshots","evidence/clips","vision/models" | Out-Null
if (-not (Test-Path ".venv311\Scripts\python.exe")) {
    Write-Host "Creating Python 3.11 environment..." -ForegroundColor Cyan
    py -3.11 -m venv .venv311
}
$Python = Join-Path $ProjectRoot ".venv311\Scripts\python.exe"
$env:PYTHONPATH = "$ProjectRoot\backend;$ProjectRoot"

Write-Host "Installing backend packages..." -ForegroundColor Cyan
& $Python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "pip upgrade failed. Check your internet connection and retry." }
& $Python -m pip install -r .\backend\requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Backend dependency installation failed. The error is shown above." }
Write-Host "Installing video analytics packages (PyTorch/YOLO may take several minutes)..." -ForegroundColor Cyan
& $Python -m pip install -r .\analytics\requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Analytics dependency installation failed. The error is shown above." }

if (-not (Test-Path ".\frontend\node_modules\vite\bin\vite.js")) {
    Write-Host "Installing frontend packages..." -ForegroundColor Cyan
    Push-Location .\frontend
    try { & npm.cmd install; if ($LASTEXITCODE -ne 0) { throw "Frontend dependency installation failed." } }
    finally { Pop-Location }
}

Write-Host "Checking database connection and preparing tables..." -ForegroundColor Cyan
$bootstrap = & $Python .\scripts\bootstrap_local_db.py
if ($LASTEXITCODE -ne 0) { throw "Database setup failed. If .env points to PostgreSQL, make sure the PostgreSQL service and database are available. Otherwise remove .env and rerun to create a local SQLite database." }
if ($bootstrap -contains "NO_USERS") {
    Write-Host "No user found. Create the first administrator account now." -ForegroundColor Yellow
    & $Python -m app.cli create-admin --username admin --email admin@qsr.local
    if ($LASTEXITCODE -ne 0) { throw "Administrator creation failed. Resolve the message above and rerun the launcher." }
} else {
    Write-Host "Existing user found in the configured database; no new account was created." -ForegroundColor Green
}

Write-Host "Opening API, analytics worker, and frontend in separate PowerShell windows..." -ForegroundColor Cyan
$runner = Join-Path $ProjectRoot "scripts\run_backend_local.ps1"
$worker = Join-Path $ProjectRoot "scripts\run_worker_local.ps1"
$front = Join-Path $ProjectRoot "scripts\run_frontend_local.ps1"
Start-Process powershell.exe -ArgumentList @("-NoExit","-ExecutionPolicy","Bypass","-File",$runner)
Start-Sleep -Seconds 2
Start-Process powershell.exe -ArgumentList @("-NoExit","-ExecutionPolicy","Bypass","-File",$worker)
Start-Process powershell.exe -ArgumentList @("-NoExit","-ExecutionPolicy","Bypass","-File",$front)
Start-Sleep -Seconds 3
Write-Host "`nQSR services launched." -ForegroundColor Green
Write-Host "Frontend:  http://127.0.0.1:5173" -ForegroundColor Green
Write-Host "API docs:  http://127.0.0.1:8000/docs" -ForegroundColor Green
Write-Host "Health:    http://127.0.0.1:8000/health" -ForegroundColor Green
Write-Host "`nKeep all three service windows open. The first video run may download official YOLO11n weights and needs internet access." -ForegroundColor Yellow
Start-Process "http://127.0.0.1:5173"
