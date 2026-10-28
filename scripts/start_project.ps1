$ErrorActionPreference = "Stop"
if (!(Test-Path ".env")) { throw ".env not found. Run .\scripts\setup_windows.ps1 and edit .env first." }
docker compose up --build -d
if ($LASTEXITCODE -ne 0) { throw "docker compose failed" }
Write-Host "Frontend: http://localhost:5173"
Write-Host "Backend:  http://localhost:8000/docs"
