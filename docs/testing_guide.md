# Testing guide
- Unit tests: password hashing/token decode.
- API smoke test: `/health`, `/docs`, login, summary, video upload.
- Analytics: compare detected people and queue counts with manually reviewed frames.
- Queue region: inspect polygon overlay for each camera angle.
- Alert logic: test queue threshold, waiting threshold, cooldown, acknowledgement/resolution, and evidence retrieval.
- Performance: record CPU, model version, input resolution/FPS, processed frames, average FPS, processing duration, and alert latency.
- GPU acceptance is only valid on the actual compatible NVIDIA deployment target.
