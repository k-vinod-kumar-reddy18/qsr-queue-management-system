"""Create local QSR tables safely and report whether a user already exists."""
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app import models

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    has_user = db.query(models.User.id).first() is not None
print("ADMIN_EXISTS" if has_user else "NO_USERS")
