from datetime import datetime
from pydantic import BaseModel
class VideoOut(BaseModel):
    id: int
    name: str
    filename: str
    status: str
    created_at: datetime
    latest_run_id: int | None = None
    latest_run_status: str | None = None
    latest_run_error: str | None = None
    processed_video_url: str | None = None
    model_config = {"from_attributes": True}
class AlertOut(BaseModel):
    id: int
    alert_type: str
    severity: str
    status: str
    message: str
    queue_count: int
    wait_seconds: float
    recommendation: str
    evidence_status: str
    created_at: datetime
    model_config = {"from_attributes": True}
