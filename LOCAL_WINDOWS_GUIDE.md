# QSR Queue Management System — Windows local run (no Docker)

## One-click start

1. Install **Python 3.11** and **Node.js LTS** if they are not already installed.
2. Open this project folder in Windows File Explorer.
3. Right-click `RUN_QSR.ps1` and choose **Run with PowerShell**, or open PowerShell in this folder and run:

   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass
   .\RUN_QSR.ps1
   ```

   The launcher creates a Python virtual environment, installs Python and frontend packages, prepares database tables, creates the first administrator only if the configured database has no users, and opens API, worker, and frontend windows. It does not use Docker and does not require activating the virtual environment.

4. Open **http://127.0.0.1:5173**. API docs are at **http://127.0.0.1:8000/docs** and health is at **http://127.0.0.1:8000/health**.
5. If the launcher asks to create an administrator, enter a password of at least 10 characters twice. Use that username/password to sign in. If an existing `.env` is configured for a database that already has a user, the launcher does not create another account.

## Database behavior

- If no `.env` exists, the launcher creates one using local SQLite (`qsr_local.db`). No PostgreSQL service is needed in this mode.
- If you already copied your working `.env` from another local copy of this project, the launcher keeps its database settings and adjusts container-only `/app/...` file paths to local paths. If that `.env` points to PostgreSQL, the PostgreSQL Windows service and named database must be available.
- `.env` contains private credentials and should not be shared or committed.

## Video detection workflow

1. Sign in and open **Video Management**.
2. Select an MP4/MOV/AVI/MKV/WEBM file and click **Upload & start detection**.
3. The API saves the uploaded source under `videos/input/` and queues a processing run automatically.
4. Keep the API, analytics worker, and frontend PowerShell windows open. The worker uses CPU-based YOLO11 person detection/tracking, records queue measurements and threshold alerts, and writes an annotated MP4 under `videos/processed/`.
5. The UI refreshes every six seconds. The run status changes from `queued` to `processing` and then `completed` or `failed`. Once completed, the annotated video player appears in Video Management. Dashboard charts and alerts populate from the measurements.

## First-run model download

The project is configured for **YOLO11n**. If `vision/models/yolo11n.pt` is absent, Ultralytics attempts to download official `yolo11n.pt` weights on first processing. An internet connection is required for this first download. The video-analysis packages, including PyTorch, can take several minutes to install. CPU processing can be slow for long/high-resolution videos.

## If something fails

- Read the error in the relevant service window; do not close the API/worker/frontend windows while using the app.
- `Failed to fetch`: confirm API health at `http://127.0.0.1:8000/health` and that all service windows remain open.
- Database error: if using PostgreSQL, check its Windows service and the database URL in `.env`. For a fresh SQLite setup, close the service windows, back up/remove `.env` only if you want to reset to the SQLite default, then rerun the launcher.
- Model download error: check internet access and try processing again.
- Stop the app by closing the three service windows (API, worker, frontend).

## Important accuracy note

The default queue polygon is only a starting region. Counts and waiting-time estimates must be validated and the polygon calibrated for the specific camera view. This is a development baseline, not a guarantee of production accuracy.
