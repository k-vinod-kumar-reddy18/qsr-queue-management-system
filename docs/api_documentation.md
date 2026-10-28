# API documentation
Interactive OpenAPI docs: `/docs`.

Authentication: send `Authorization: Bearer <access_token>` to protected routes. Login expects `application/x-www-form-urlencoded` fields `username` and `password`.

Endpoints:
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`
- `GET /api/v1/dashboard/summary`
- `GET /api/v1/dashboard/history`
- `GET /api/v1/videos`
- `POST /api/v1/videos/upload`
- `POST /api/v1/videos/{video_id}/process`
- `GET /api/v1/alerts`
- `POST /api/v1/alerts/{alert_id}/acknowledge`
- `POST /api/v1/alerts/{alert_id}/resolve`
- `GET/PUT /api/v1/settings/thresholds` (admin only)
- `GET /api/v1/evidence/{evidence_id}/file`
- `GET /health`
- `WS /ws/metrics`
