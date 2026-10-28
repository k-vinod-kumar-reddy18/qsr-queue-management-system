from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models import Alert
from app.schemas.video import AlertOut

router = APIRouter(prefix="/alerts", tags=["alerts"])
@router.get("", response_model=list[AlertOut])
def list_alerts(status: str | None = None, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    q = db.query(Alert)
    if status: q = q.filter(Alert.status == status)
    return q.order_by(Alert.created_at.desc()).limit(max(1, min(limit, 500))).all()

@router.post("/{alert_id}/acknowledge")
def acknowledge(alert_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert: raise HTTPException(404, "Alert not found")
    if alert.status == "open":
        alert.status = "acknowledged"; alert.acknowledged_at = datetime.now(timezone.utc); db.commit()
    return {"id": alert.id, "status": alert.status}

@router.post("/{alert_id}/resolve")
def resolve(alert_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert: raise HTTPException(404, "Alert not found")
    alert.status = "resolved"; alert.resolved_at = datetime.now(timezone.utc); db.commit()
    return {"id": alert.id, "status": alert.status}
