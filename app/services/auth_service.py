from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.repository.user_repository import UserRepository
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.schemas.user import Token
from app.schemas.user import UserCreate
from app.models.user import User

class AuthService:
    @staticmethod
    def register(db: Session, data: UserCreate) -> User:
        if UserRepository.get_by_email(db, data.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if UserRepository.get_by_name(db, data.name):
            raise HTTPException(status_code=400, detail="Name already taken")
        if data.role not in ("student", "admin"):
            raise HTTPException(status_code=400, detail="Invalid role. Must be 'student' or 'admin'")
        return UserRepository.create(db, data)

    @staticmethod
    def login(db: Session, email: str, password: str) -> Token:
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        token = create_access_token(
            data={"sub": user.email, "role": user.role},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return Token(access_token=token, token_type="bearer")

    @staticmethod
    def get_profile(user: User) -> User:
        return user