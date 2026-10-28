from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import Alert
from app.core.config import settings

def create_threshold_alert(db: Session, run_id: int, queue_count: int, wait_seconds: float, frame=None):
    now = datetime.now(timezone.utc)
    conditions = []
    if queue_count >= settings.queue_alert_threshold:
        conditions.append(("queue_threshold", f"Queue contains {queue_count} tracked people.",
                           "Consider assigning additional staff; a manager should confirm."))
    if wait_seconds >= settings.waiting_time_alert_minutes * 60:
        conditions.append(("waiting_threshold", f"Estimated wait reached {wait_seconds/60:.1f} minutes.",
                           "Review service capacity and consider opening another counter."))
    created = []
    for alert_type, message, recommendation in conditions:
        recent = db.query(Alert).filter(
            Alert.run_id == run_id, Alert.alert_type == alert_type, Alert.status != "resolved"
        ).order_by(Alert.created_at.desc()).first()
        if recent and (now - recent.created_at.replace(tzinfo=timezone.utc)).total_seconds() < settings.alert_cooldown_seconds:
            continue
        path = None
        evidence_status = "capture_failed"
        if frame is not None:
            try:
                import cv2, os
                os.makedirs(settings.evidence_dir + "/snapshots", exist_ok=True)
                path = f"{settings.evidence_dir}/snapshots/alert_run{run_id}_{alert_type}_{int(now.timestamp())}.jpg"
                if cv2.imwrite(path, frame):
                    evidence_status = "saved"
                else:
                    path = None
            except Exception:
                path = None
        alert = Alert(run_id=run_id, alert_type=alert_type, message=message, queue_count=queue_count,
                      wait_seconds=wait_seconds, recommendation=recommendation,
                      evidence_path=path, evidence_status=evidence_status)
        db.add(alert)
        created.append(alert)
    db.commit()
    return created
