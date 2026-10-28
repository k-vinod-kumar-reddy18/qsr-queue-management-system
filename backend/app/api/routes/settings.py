from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import require_admin
from app.core.config import settings
from app.models import AppSetting
router = APIRouter(prefix="/settings", tags=["settings"])
class Thresholds(BaseModel):
    queue_alert_threshold: int = Field(5, ge=1, le=500)
    waiting_time_alert_minutes: int = Field(5, ge=1, le=240)
@router.get("/thresholds")
def get_thresholds(db: Session = Depends(get_db), user=Depends(require_admin)):
    values = {x.key: x.value for x in db.query(AppSetting).all()}
    return {"queue_alert_threshold": int(values.get("queue_alert_threshold", settings.queue_alert_threshold)),
            "waiting_time_alert_minutes": int(values.get("waiting_time_alert_minutes", settings.waiting_time_alert_minutes))}
@router.put("/thresholds")
def update_thresholds(body: Thresholds, db: Session = Depends(get_db), user=Depends(require_admin)):
    for key, value in body.model_dump().items():
        item = db.query(AppSetting).filter(AppSetting.key == key).first()
        if item: item.value = str(value)
        else: db.add(AppSetting(key=key, value=str(value)))
    db.commit()
    return body.model_dump()
