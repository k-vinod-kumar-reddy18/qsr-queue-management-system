import cv2
import numpy as np

# Provisional normalized polygon. Must be adjusted for each camera/video.
DEFAULT_QUEUE_POLYGON = [(0.20, 0.35), (0.80, 0.35), (0.95, 0.95), (0.05, 0.95)]

def point_in_polygon(x, y, polygon_normalized, width, height):
    pts = np.array([(int(px * width), int(py * height)) for px, py in polygon_normalized], dtype=np.int32)
    return cv2.pointPolygonTest(pts, (float(x), float(y)), False) >= 0

def draw_polygon(frame, polygon_normalized, label="QUEUE REGION"):
    h, w = frame.shape[:2]
    pts = np.array([(int(px*w), int(py*h)) for px, py in polygon_normalized], dtype=np.int32)
    cv2.polylines(frame, [pts], True, (255, 180, 0), 2)
    cv2.putText(frame, label, tuple(pts[0]), cv2.FONT_HERSHEY_SIMPLEX, .6, (255,180,0), 2)
