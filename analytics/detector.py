from pathlib import Path
from app.core.config import settings

def load_model():
    model_path = Path(settings.model_path)
    if "yolo11" not in model_path.name.lower():
        raise ValueError(
            "This project is configured for YOLO11 only. Set MODEL_PATH to a YOLO11 weights file."
        )
    from ultralytics import YOLO
    if model_path.is_file():
        return YOLO(str(model_path))
    # Ultralytics downloads the official YOLO11n weights on first use if they are not cached.
    # This requires an internet connection on the first run; a local MODEL_PATH takes precedence.
    return YOLO("yolo11n.pt")
