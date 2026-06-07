from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.deps import require_admin
from app.services.course_service import CourseService
from app.repository.course_repository import CourseRepository
from app.schemas.user import CourseCreate, CourseUpdate, CourseRead

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=list[CourseRead])
def get_courses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CourseRepository.get_all_active(db, skip, limit)

@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = CourseRepository.get_by_id(db, course_id)
    if not course:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.post("/", response_model=CourseRead, status_code=201)
def create_course(data: CourseCreate, db: Session = Depends(get_db), _: None = Depends(require_admin)):
    return CourseService.create_course(db, data)

@router.put("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, data: CourseUpdate, db: Session = Depends(get_db), _: None = Depends(require_admin)):
    return CourseService.update_course(db, course_id, data)

@router.delete("/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db), _: None = Depends(require_admin)):
    CourseService.delete_course(db, course_id)