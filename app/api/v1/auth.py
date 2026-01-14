from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Any

from app.core import security
from app.db.session import get_db
from app.db.models import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.api import deps
from app.services import auth_service
from pydantic import BaseModel

router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/register", response_model=UserResponse)
def register_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    
    hashed_password = security.get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/me", response_model=UserResponse)
def read_users_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return current_user

class TwoFASetup(BaseModel):
    secret: str
    uri: str

class TwoFAEnable(BaseModel):
    secret: str
    code: str

@router.post("/2fa/setup", response_model=TwoFASetup)
def setup_2fa(
    current_user: User = Depends(deps.get_current_user),
):
    secret = auth_service.generate_totp_secret()
    uri = auth_service.get_totp_uri(secret, current_user.email)
    return {"secret": secret, "uri": uri}

@router.post("/2fa/enable", response_model=UserResponse)
def enable_2fa(
    payload: TwoFAEnable,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
):
    if not auth_service.verify_totp(payload.secret, payload.code):
        raise HTTPException(status_code=400, detail="Invalid 2FA code")
    
    current_user.totp_secret = payload.secret
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

