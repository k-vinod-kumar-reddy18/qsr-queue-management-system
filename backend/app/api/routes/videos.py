import os, uuid
from pathlib import Path
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.core.config import settings
from app.models import VideoSource, ProcessingRun
from app.schemas.video import VideoOut

router = APIRouter(prefix="/videos", tags=["videos"])

def _video_payload(db: Session, video: VideoSource):
    latest = db.query(ProcessingRun).filter(ProcessingRun.video_id == video.id).order_by(ProcessingRun.id.desc()).first()
    return {
        "id": video.id, "name": video.name, "filename": video.filename,
        "status": video.status, "created_at": video.created_at,
        "latest_run_id": latest.id if latest else None,
        "latest_run_status": latest.status if latest else None,
        "latest_run_error": latest.error_message if latest else None,
        "processed_video_url": f"/videos/{video.id}/processed" if latest and latest.status == "completed" else None,
    }

@router.get("", response_model=list[VideoOut])
def list_videos(db: Session = Depends(get_db), user=Depends(get_current_user)):
    videos = db.query(VideoSource).order_by(VideoSource.created_at.desc()).all()
    return [_video_payload(db, video) for video in videos]

@router.post("/upload", response_model=VideoOut)
async def upload_video(file: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    allowed = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in allowed:
        raise HTTPException(400, "Unsupported video type. Upload MP4, MOV, AVI, MKV, or WEBM.")
    os.makedirs(settings.upload_dir, exist_ok=True)
    name = f"{uuid.uuid4().hex}{suffix}"
    target = Path(settings.upload_dir) / name
    size = 0
    max_bytes = settings.max_upload_mb * 1024 * 1024
    try:
        with target.open("wb") as out:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > max_bytes:
                    raise HTTPException(413, f"Video exceeds configured {settings.max_upload_mb} MB limit")
                out.write(chunk)
    except Exception:
        target.unlink(missing_ok=True)
        raise
    video = VideoSource(name=file.filename or name, filename=name, status="queued")
    db.add(video)
    db.commit()
    db.refresh(video)
    # Automatically queue analysis immediately after upload; the worker handles the long-running job.
    run = ProcessingRun(video_id=video.id, status="queued")
    db.add(run)
    db.commit()
    db.refresh(run)
    return _video_payload(db, video)

@router.post("/{video_id}/process")
def process_video(video_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    video = db.query(VideoSource).filter(VideoSource.id == video_id).first()
    if not video:
        raise HTTPException(404, "Video not found")
    latest = db.query(ProcessingRun).filter(ProcessingRun.video_id == video.id).order_by(ProcessingRun.id.desc()).first()
    if latest and latest.status in {"queued", "processing"}:
        return {"run_id": latest.id, "status": latest.status, "message": "Video is already queued or processing."}
    run = ProcessingRun(video_id=video.id, status="queued")
    video.status = "queued"
    db.add(run)
    db.commit()
    db.refresh(run)
    return {"run_id": run.id, "status": run.status, "message": "Queued for analytics worker."}

@router.get("/{video_id}/processed")
def get_processed_video(video_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    video = db.query(VideoSource).filter(VideoSource.id == video_id).first()
    if not video:
        raise HTTPException(404, "Video not found")
    run = db.query(ProcessingRun).filter(ProcessingRun.video_id == video.id, ProcessingRun.status == "completed").order_by(ProcessingRun.id.desc()).first()
    if not run:
        raise HTTPException(404, "No completed processed video is available yet")
    source = Path(settings.upload_dir) / video.filename
    output = Path(settings.processed_dir) / f"run_{run.id}_{source.stem}.mp4"
    if not output.is_file():
        raise HTTPException(404, "Processed video file is missing on disk")
    browser_output = output.with_name(f"{output.stem}_browser{output.suffix}")
    playback_file = browser_output if browser_output.is_file() else output
    return FileResponse(
        playback_file,
        media_type="video/mp4",
        filename=playback_file.name,
    )


