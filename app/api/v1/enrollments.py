from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.deps import require_admin, require_student
from app.services.enrollment_service import EnrollmentService
from app.repository.enrollment_repository import EnrollmentRepository
from app.schemas.user import EnrollmentCreate, EnrollmentRead
from app.models.user import User

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentRead, status_code=201)
def enroll(
    data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student)
):
    return EnrollmentService.enroll_student(db, current_user, data.course_id)

@router.delete("/{enrollment_id}", status_code=204)
def deregister(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student)
):
    EnrollmentService.deregister_student(db, current_user, enrollment_id)

@router.get("/", response_model=list[EnrollmentRead])
def get_all_enrollments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin)
):
    return EnrollmentRepository.get_all(db, skip, limit)

@router.get("/course/{course_id}", response_model=list[EnrollmentRead])
def get_enrollments_by_course(
    course_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin)
):
    return EnrollmentRepository.get_by_course_id(db, course_id, skip, limit)

@router.delete("/admin/{enrollment_id}", status_code=204)
def admin_remove_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin)
):
    EnrollmentService.admin_remove_enrollment(db, enrollment_id)