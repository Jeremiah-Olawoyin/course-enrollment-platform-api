from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.deps import get_current_active_user
from app.core.rate_limit import get_rate_limiter
from app.services.auth_service import AuthService
from app.schemas.user import Token
from app.schemas.user import UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["Authentication"])

check_rate_limit = get_rate_limiter()

@router.post("/register", response_model=UserRead, status_code=201, dependencies=[Depends(check_rate_limit)])
def register(data: UserCreate, db: Session = Depends(get_db)):
    return AuthService.register(db, data)

@router.post("/token", response_model=Token, dependencies=[Depends(check_rate_limit)])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    email = form_data.username
    return AuthService.login(db, email, form_data.password)

@router.get("/me", response_model=UserRead)
def get_me(current_user = Depends(get_current_active_user)):
    return current_user