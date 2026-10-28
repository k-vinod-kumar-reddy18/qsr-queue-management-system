# NVIDIA DeepStream and RTSP deployment

The main application currently provides CPU-first recorded-video analytics using OpenCV and Ultralytics. This folder documents the target NVIDIA deployment boundary; it is not a claim that DeepStream is already running.

Before enabling DeepStream, confirm:
- NVIDIA GPU/Jetson model and OS.
- NVIDIA driver, CUDA/TensorRT and DeepStream versions.
- Supported YOLO export format and parser/plugin requirements.
- Camera RTSP reachability and credentials.
- Whether the chosen tracker and region logic are supported by the deployed pipeline.

Build and validate the NVIDIA image on the target host using the official NVIDIA DeepStream container for the supported platform/version. Do not expect a standard Windows Docker Desktop CPU environment to run DeepStream. The `Dockerfile.deepstream` is a documented scaffold, not a portable build recipe until the SDK version is selected.

RTSP URLs should be provided through secrets/environment configuration and never committed. Use reconnect logic and surface camera health. The CPU path and DeepStream path should write the same queue measurement, alert, and evidence records through a documented adapter.
