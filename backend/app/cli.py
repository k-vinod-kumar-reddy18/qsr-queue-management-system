import argparse, getpass
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app import models
from app.core.security import hash_password

def create_admin(username, email):
    password = getpass.getpass("Admin password (minimum 10 characters): ")
    confirm = getpass.getpass("Confirm password: ")
    if password != confirm: raise SystemExit("Passwords do not match")
    db: Session = SessionLocal()
    try:
        if db.query(models.User).filter((models.User.username == username) | (models.User.email == email)).first():
            raise SystemExit("Username or email already exists")
        user = models.User(username=username, email=email, password_hash=hash_password(password), role="admin")
        db.add(user); db.commit()
        print(f"Administrator '{username}' created.")
    finally: db.close()

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("create-admin"); p.add_argument("--username", required=True); p.add_argument("--email", required=True)
    args = parser.parse_args()
    Base.metadata.create_all(bind=engine)
    if args.command == "create-admin": create_admin(args.username, args.email)
if __name__ == "__main__": main()
