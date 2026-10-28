# QSR Queue Management System

CPU-first QSR customer counting and queue analytics starter application.

## Architecture
- `frontend/`: React + Vite + TypeScript dashboard.
- `backend/`: FastAPI, JWT authentication, SQLAlchemy, PostgreSQL, WebSockets.
- `analytics/`: OpenCV + Ultralytics YOLO11 person detection, tracking, queue regions, snapshots.
- `database/`: schema notes and additive migration guidance.
- `vision/`: NVIDIA DeepStream / RTSP compatibility guide.
- `videos/`: local input and processed video folders.
- `evidence/`: generated alert snapshots and clips.
- Docker Compose starts PostgreSQL, backend, frontend and analytics worker.

The initial implementation is designed for recorded-video CPU testing. GPU/DeepStream and RTSP must be validated on the target NVIDIA platform. Do not claim accuracy or performance before measuring them.

## Requirements
- Windows: Python 3.11 and Node.js LTS (npm included).
- A first-run internet connection to install dependencies and download YOLO11n weights if not already present.
- Docker is optional; the local Windows launcher does not use Docker.

## One-click startup on Windows (no Docker)
1. Open this project folder in PowerShell.
2. Run:
   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\RUN_QSR.ps1
   ```
3. The launcher creates `.env` if needed (SQLite by default), creates the Python environment, installs backend and analytics packages, installs frontend packages, prepares tables, and opens API, worker, and frontend windows.
4. If this is a fresh database, create the first administrator when prompted. Use that username/password to sign in.
5. Open `http://127.0.0.1:5173`. API docs: `http://127.0.0.1:8000/docs`; health: `http://127.0.0.1:8000/health`.

See [LOCAL_WINDOWS_GUIDE.md](LOCAL_WINDOWS_GUIDE.md) for database behavior, video processing, outputs, and troubleshooting.

## Optional Docker startup
The original Docker Compose configuration remains available for users who prefer Docker. It expects Docker Desktop, a configured `.env`, and database credentials. Run `docker compose up --build -d` only when intentionally using Docker.

## Default API endpoints
- `POST /api/v1/auth/login` — OAuth2-compatible form login, returns access token.
- `GET /api/v1/auth/me`
- `GET /api/v1/dashboard/summary`
- `GET/POST /api/v1/videos`
- `POST /api/v1/videos/upload`
- `POST /api/v1/videos/{video_id}/process`
- `GET /api/v1/alerts`
- `POST /api/v1/alerts/{alert_id}/acknowledge`
- `POST /api/v1/alerts/{alert_id}/resolve`
- `GET/PUT /api/v1/settings/thresholds`
- `GET /api/v1/evidence/{evidence_id}/file`
- `WS /ws/metrics` — dashboard metric notifications.

## Security and data safety
- Secrets are environment variables; `.env` is ignored by Git.
- Passwords are hashed using Argon2 via Passlib.
- JWT access tokens expire.
- Protected endpoints require authentication.
- Evidence is served through an authenticated route.
- Database tables are created additively on startup; the app never drops tables. For production, use reviewed Alembic migrations and backups.
- This is a development baseline. Configure HTTPS, production secret management, backups, retention and user provisioning before public deployment.

## Analytics notes
- YOLO class `person` detections are tracked with persistent track IDs where supported.
- Queue count is based on tracked person centers inside the configured polygon. A default polygon is only a placeholder and must be calibrated per camera.
- Waiting time is an estimate based on queue-region entry/exit observations and tracker continuity.
- Region membership cannot reliably distinguish staff from customers.
- Evidence snapshots are attached to threshold alerts when a frame is available.
- The analytics worker processes videos asynchronously. CPU performance depends on model, resolution and hardware.

## Tests
Run backend tests locally:
```powershell
python -m pip install -r backend/requirements.txt
$env:DATABASE_URL="sqlite:///./test.db"
python -m pytest backend/tests -q
```


## Automatic video detection and annotated playback

- Uploading a video automatically creates a queued processing run; you do not need to click a separate Process button.
- Keep the backend API and analytics worker running. The Video Management page refreshes statuses and displays the annotated MP4 when the run completes.
- The worker writes output videos under `videos/processed/` and the authenticated frontend fetches the result for playback.
- The configured local YOLO11 weights file is used when present. If it is absent, the detector asks Ultralytics to fetch official `yolo11n.pt` weights on first use; first-run download therefore requires internet access.
- Detection/tracking failures are shown in the video row. Counts depend on queue-region calibration and should be validated against sample footage.
