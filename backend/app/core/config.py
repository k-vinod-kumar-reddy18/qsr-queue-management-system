from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    app_name: str = "QSR Queue Management System"
    database_url: str = "sqlite:///./qsr_dev.db"
    jwt_secret_key: str = "development-only-change-this-secret"
    access_token_expire_minutes: int = 30
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    upload_dir: str = "./videos/input"
    processed_dir: str = "./videos/processed"
    evidence_dir: str = "./evidence"
    model_path: str = "./vision/models/yolo11n.pt"  # YOLO11 family only
    detection_device: str = "cpu"
    queue_alert_threshold: int = 5
    waiting_time_alert_minutes: int = 5
    alert_cooldown_seconds: int = 120
    max_upload_mb: int = 500

    @property
    def cors_origin_list(self):
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
