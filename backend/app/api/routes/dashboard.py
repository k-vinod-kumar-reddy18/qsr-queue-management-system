from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models import Alert, VideoSource, ProcessingRun, QueueMeasurement

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/summary")
def summary(db: Session = Depends(get_db), user=Depends(get_current_user)):
    latest = db.query(QueueMeasurement).order_by(QueueMeasurement.id.desc()).first()
    open_alerts = db.query(func.count(Alert.id)).filter(Alert.status == "open").scalar() or 0
    videos = db.query(func.count(VideoSource.id)).scalar() or 0
    running = db.query(func.count(ProcessingRun.id)).filter(ProcessingRun.status == "processing").scalar() or 0
    return {
        "queue_count": latest.queue_count if latest else 0,
        "average_wait_seconds": latest.average_wait_seconds if latest else 0,
        "fps": latest.fps if latest else 0,
        "active_alerts": open_alerts,
        "videos": videos,
        "processing_runs": running,
        "camera_status": "recorded-video mode",
        "analytics_status": "idle" if not running else "processing"
    }

@router.get("/history")
def history(limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    limit = max(1, min(limit, 1000))
    rows = db.query(QueueMeasurement).order_by(QueueMeasurement.id.desc()).limit(limit).all()
    return [{"id": x.id, "run_id": x.run_id, "video_seconds": x.video_seconds, "queue_count": x.queue_count,
             "average_wait_seconds": x.average_wait_seconds, "fps": x.fps, "created_at": x.created_at} for x in reversed(rows)]
