from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository.course_repository import CourseRepository
from app.schemas.user import CourseCreate, CourseUpdate

class CourseService:
    @staticmethod
    def create_course(db: Session, data: CourseCreate) -> "Course":
        if CourseRepository.get_by_code(db, data.code):
            raise HTTPException(status_code=400, detail="Course code already exists")
        if data.capacity <= 0:
            raise HTTPException(status_code=400, detail="Capacity must be greater than zero")
        return CourseRepository.create(db, data.title, data.code, data.capacity)

    @staticmethod
    def update_course(db: Session, course_id: int, data: CourseUpdate) -> "Course":
        course = CourseRepository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        if data.code and data.code != course.code:
            if CourseRepository.get_by_code(db, data.code):
                raise HTTPException(status_code=400, detail="Course code already exists")
        if data.capacity is not None and data.capacity <= 0:
            raise HTTPException(status_code=400, detail="Capacity must be greater than zero")
        return CourseRepository.update(
            db, course,
            title=data.title,
            code=data.code,
            capacity=data.capacity
        )

    @staticmethod
    def activate_course(db: Session, course_id: int, is_active: bool) -> "Course":
        course = CourseRepository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return CourseRepository.activate(db, course, is_active)

    @staticmethod
    def delete_course(db: Session, course_id: int) -> None:
        course = CourseRepository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        CourseRepository.delete(db, course)