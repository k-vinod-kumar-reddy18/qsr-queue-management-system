# Architecture

```text
React/Vite dashboard
   | REST + WebSocket
FastAPI service ---------------- PostgreSQL
   |                                 |
Video source + analytics worker ---- measurements, runs, alerts
   |
OpenCV + YOLO person detection + tracking
   |
Queue polygon -> queue count/wait estimates -> thresholds -> snapshot evidence

Future deployment adapter:
RTSP camera -> NVIDIA DeepStream/TensorRT on compatible NVIDIA edge host
             -> same persistence/alert contract
```

The queue polygon is a placeholder until calibrated against each camera. Queue wait is an estimate based on tracking continuity. A region polygon alone cannot reliably distinguish staff from customers.
