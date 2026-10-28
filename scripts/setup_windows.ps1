$ErrorActionPreference = "Stop"
if (!(Test-Path ".env")) { Copy-Item ".env.example" ".env"; Write-Host "Created .env from template. Edit it before starting." }
New-Item -ItemType Directory -Force videos/input, videos/processed, evidence/snapshots, evidence/clips, vision/models | Out-Null
Write-Host "Folders ready. Install Docker Desktop, edit .env, then run .\scripts\start_project.ps1"
