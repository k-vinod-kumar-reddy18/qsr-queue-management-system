from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User
from app.core.security import verify_password, create_access_token
from app.dependencies import get_current_user
from app.schemas.auth import TokenOut, UserOut

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login", response_model=TokenOut)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not user.is_active or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    return TokenOut(access_token=create_access_token(user.username, user.role))

@router.get("/me", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user
