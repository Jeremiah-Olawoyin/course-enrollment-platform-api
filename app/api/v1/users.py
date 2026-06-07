from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.deps import get_current_active_user
from app.repository.user_repository import UserRepository
from app.schemas.user import UserRead, UserReadWithEnrollments

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserRead)
def get_profile(current_user = Depends(get_current_active_user)):
    return current_user

@router.get("/me/enrollments", response_model=UserReadWithEnrollments)
def get_my_enrollments(current_user = Depends(get_current_active_user)):
    return current_user