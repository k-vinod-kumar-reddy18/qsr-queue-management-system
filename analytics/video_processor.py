import os, time
from pathlib import Path
import cv2
from app.core.config import settings
from app.models import ProcessingRun
from app.services.alerts import create_threshold_alert
from app.services.queue_service import save_measurement, save_event
from analytics.detector import load_model
from analytics.region_manager import DEFAULT_QUEUE_POLYGON, point_in_polygon, draw_polygon
from analytics.waiting_time import QueueWaitTracker
from analytics.tracker import get_track_id

def process_video(input_path: str, output_path: str, db, run_id: int):
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input video not found: {input_path}")
    model = load_model()
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError("OpenCV could not open input video")
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    if not writer.isOpened():
        cap.release()
        raise RuntimeError("Could not create output video; check FFmpeg/codec support")
    wait_tracker = QueueWaitTracker()
    frames, elapsed_total, last_sample = 0, 0.0, -1.0
    try:
        while True:
            ok, frame = cap.read()
            if not ok: break
            start = time.perf_counter()
            video_seconds = frames / fps
            result = model.track(frame, persist=True, classes=[0], device=settings.detection_device, verbose=False)[0]
            active_ids, count, max_wait = [], 0, 0.0
            if result.boxes is not None:
                for i, box in enumerate(result.boxes):
                    coords = box.xyxy[0].cpu().numpy().astype(int)
                    x1, y1, x2, y2 = coords.tolist()
                    cx, cy = (x1+x2)//2, (y1+y2)//2
                    tid = get_track_id(box, i)
                    inside = point_in_polygon(cx, cy, DEFAULT_QUEUE_POLYGON, width, height)
                    wait = wait_tracker.update(tid, inside, video_seconds)
                    if inside:
                        count += 1; active_ids.append(tid); max_wait = max(max_wait, wait)
                    cv2.rectangle(frame, (x1,y1), (x2,y2), (40,220,90) if inside else (80,180,255), 2)
                    cv2.putText(frame, f"ID {tid}", (x1, max(20,y1-8)), cv2.FONT_HERSHEY_SIMPLEX, .55, (255,255,255), 2)
            draw_polygon(frame, DEFAULT_QUEUE_POLYGON)
            cv2.putText(frame, f"Queue count: {count} | video time: {video_seconds:.1f}s", (20,35),
                        cv2.FONT_HERSHEY_SIMPLEX, .8, (255,255,255), 2)
            writer.write(frame)
            elapsed = time.perf_counter() - start
            elapsed_total += elapsed; frames += 1
            if video_seconds - last_sample >= 2.0:
                measured_fps = 1.0 / elapsed if elapsed > 0 else 0.0
                avg_wait = wait_tracker.average_active_wait(active_ids, video_seconds)
                save_measurement(db, run_id, video_seconds, count, avg_wait, measured_fps)
                create_threshold_alert(db, run_id, count, max_wait, frame)
                last_sample = video_seconds
    finally:
        cap.release(); writer.release()
    return {"frames_processed": frames, "source_frames": total,
            "average_fps": round(frames / elapsed_total, 2) if elapsed_total else 0,
            "output_path": output_path}
