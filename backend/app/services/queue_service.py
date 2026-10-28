from sqlalchemy.orm import Session
from app.models import QueueMeasurement, QueueEvent
def save_measurement(db: Session, run_id: int, video_seconds: float, queue_count: int, average_wait_seconds: float, fps: float):
    row = QueueMeasurement(run_id=run_id, video_seconds=video_seconds, queue_count=queue_count,
                           average_wait_seconds=average_wait_seconds, fps=fps)
    db.add(row)
    db.commit()
    return row
def save_event(db: Session, run_id: int, track_id: int, event_type: str, video_seconds: float, wait_seconds=None):
    row = QueueEvent(run_id=run_id, track_id=track_id, event_type=event_type,
                     video_seconds=video_seconds, wait_seconds=wait_seconds)
    db.add(row)
    db.commit()
    return row
