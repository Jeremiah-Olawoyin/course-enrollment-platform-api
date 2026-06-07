from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.course import Course
from app.schemas.user import CourseCreate, CourseUpdate

class CourseRepository:
    @staticmethod
    def get_by_id(db: Session, course_id: int) -> Course | None:
        return db.get(Course, course_id)

    @staticmethod
    def get_by_code(db: Session, code: str) -> Course | None:
        return db.scalars(select(Course).where(Course.code == code)).first()

    @staticmethod
    def get_all_active(db: Session, skip: int = 0, limit: int = 100) -> list[Course]:
        return db.scalars(select(Course).where(Course.is_active == True).offset(skip).limit(limit)).all()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Course]:
        return db.scalars(select(Course).offset(skip).limit(limit)).all()

    @staticmethod
    def create(db: Session, title: str, code: str, capacity: int) -> Course:
        course = Course(title=title, code=code, capacity=capacity)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def update(db: Session, course: Course, title: str | None = None, code: str | None = None, capacity: int | None = None) -> Course:
        if title is not None:
            course.title = title
        if code is not None:
            course.code = code
        if capacity is not None:
            course.capacity = capacity
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def activate(db: Session, course: Course, is_active: bool) -> Course:
        course.is_active = is_active
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def delete(db: Session, course: Course) -> None:
        db.delete(course)
        db.commit()