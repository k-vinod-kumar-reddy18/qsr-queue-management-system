import os, time, traceback
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app import models
from app.models import ProcessingRun, VideoSource
from app.core.config import settings
from app.core.logging import logger
from analytics.video_processor import process_video

def main():
    Base.metadata.create_all(bind=engine)
    logger.info("QSR analytics worker started; waiting for queued runs")
    while True:
        db: Session = SessionLocal()
        try:
            run = db.query(ProcessingRun).filter(ProcessingRun.status == "queued").order_by(ProcessingRun.id).first()
            if not run:
                time.sleep(2); continue
            run.status = "processing"; run.started_at = datetime.now(timezone.utc); db.commit()
            video = db.query(VideoSource).filter(VideoSource.id == run.video_id).first()
            if video:
                video.status = "processing"
                db.commit()
            try:
                source = Path(settings.upload_dir) / video.filename
                output = Path(settings.processed_dir) / f"run_{run.id}_{source.stem}.mp4"
                result = process_video(str(source), str(output), db, run.id)
                run = db.query(ProcessingRun).filter(ProcessingRun.id == run.id).first()
                run.status = "completed"; run.completed_at = datetime.now(timezone.utc)
                run.fps = result.get("average_fps", 0); run.frames_processed = result.get("frames_processed", 0)
                video.status = "processed"; db.commit()
                logger.info("run %s completed: %s", run.id, result)
            except Exception as exc:
                db.rollback()
                run = db.query(ProcessingRun).filter(ProcessingRun.id == run.id).first()
                if run:
                    run.status = "failed"; run.error_message = str(exc)[:2000]; run.completed_at = datetime.now(timezone.utc)
                    video = db.query(VideoSource).filter(VideoSource.id == run.video_id).first()
                    if video:
                        video.status = "failed"
                    db.commit()
                logger.exception("run failed")
        except Exception:
            logger.exception("worker loop error"); time.sleep(3)
        finally:
            db.close()
if __name__ == "__main__": main()
