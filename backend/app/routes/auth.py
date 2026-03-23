from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database.database import get_db
from app.schemas.schemas import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import AuthService
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = AuthService.create_user(db, user.username, user.email, user.password)
    return new_user

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, user_credentials.username, user_credentials.password)
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = AuthService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.get("/me", response_model=UserResponse)
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    scheme, token = authorization.split()
    payload = AuthService.verify_token(token)
    username = payload.get("sub")
    user = AuthService.get_user_by_username(db, username)
    return user
    
    return user
