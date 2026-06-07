from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.models.enrollment import Enrollment

class EnrollmentRepository:
    @staticmethod
    def get_by_id(db: Session, enrollment_id: int) -> Enrollment | None:
        return db.get(Enrollment, enrollment_id)

    @staticmethod
    def get_by_user_and_course(db: Session, user_id: int, course_id: int) -> Enrollment | None:
        return db.scalars(
            select(Enrollment).where(
                Enrollment.user_id == user_id,
                Enrollment.course_id == course_id
            )
        ).first()

    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[Enrollment]:
        return db.scalars(select(Enrollment).offset(skip).limit(limit)).all()

    @staticmethod
    def get_by_course_id(db: Session, course_id: int, skip: int = 0, limit: int = 100) -> list[Enrollment]:
        return db.scalars(
            select(Enrollment).where(Enrollment.course_id == course_id).offset(skip).limit(limit)
        ).all()

    @staticmethod
    def get_enrollment_count(db: Session, course_id: int) -> int:
        return db.scalar(
            select(func.count()).select_from(Enrollment).where(Enrollment.course_id == course_id)
        )

    @staticmethod
    def create(db: Session, user_id: int, course_id: int) -> Enrollment:
        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment

    @staticmethod
    def delete(db: Session, enrollment: Enrollment) -> None:
        db.delete(enrollment)
        db.commit()