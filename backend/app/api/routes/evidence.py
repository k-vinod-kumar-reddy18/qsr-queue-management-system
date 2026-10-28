from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies import get_current_user
from app.models import Alert
from app.core.config import settings
router = APIRouter(prefix="/evidence", tags=["evidence"])
@router.get("/{evidence_id}/file")
def get_evidence(evidence_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == evidence_id).first()
    if not alert or not alert.evidence_path:
        raise HTTPException(404, "Evidence not available for this alert")
    path = Path(alert.evidence_path).resolve()
    base = Path(settings.evidence_dir).resolve()
    if base not in path.parents or not path.is_file():
        raise HTTPException(404, "Evidence file missing")
    return FileResponse(path, media_type="image/jpeg", filename=path.name)
