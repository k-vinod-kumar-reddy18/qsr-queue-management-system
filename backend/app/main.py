from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app import models  # register models
from app.api.routes import auth, videos, dashboard, alerts, settings as settings_routes, evidence

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Additive table creation: never drops existing tables. Production deployments should use reviewed Alembic migrations.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True,
                   allow_methods=["*"], allow_headers=["*"])
api = "/api/v1"
app.include_router(auth.router, prefix=api)
app.include_router(videos.router, prefix=api)
app.include_router(dashboard.router, prefix=api)
app.include_router(alerts.router, prefix=api)
app.include_router(settings_routes.router, prefix=api)
app.include_router(evidence.router, prefix=api)

@app.get("/")
def root():
    return {"name": settings.app_name, "docs": "/docs", "api_prefix": api}

@app.get("/health")
def health():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {"status": "healthy", "database": "reachable"}

@app.websocket("/ws/metrics")
async def metrics_socket(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_json({"type": "connected", "message": "Metrics WebSocket connected; poll REST for authoritative values."})
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "heartbeat"})
    except WebSocketDisconnect:
        pass
