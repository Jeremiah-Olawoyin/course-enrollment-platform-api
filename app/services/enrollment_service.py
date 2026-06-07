from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repository.enrollment_repository import EnrollmentRepository
from app.repository.course_repository import CourseRepository
from app.repository.audit_repository import AuditRepository
from app.models.user import User

class EnrollmentService:
    @staticmethod
    def enroll_student(db: Session, user: User, course_id: int) -> "Enrollment":
        course = CourseRepository.get_by_id(db, course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        if not course.is_active:
            raise HTTPException(status_code=400, detail="Cannot enroll in inactive course")
        if EnrollmentRepository.get_by_user_and_course(db, user.id, course_id):
            raise HTTPException(status_code=400, detail="Already enrolled in this course")
        current_count = EnrollmentRepository.get_enrollment_count(db, course_id)
        if current_count >= course.capacity:
            raise HTTPException(status_code=400, detail="Course is full")
        enrollment = EnrollmentRepository.create(db, user.id, course_id)
        AuditRepository.create(db, enrollment.id, user.id, course_id, "enroll")
        return enrollment

    @staticmethod
    def deregister_student(db: Session, user: User, enrollment_id: int) -> None:
        enrollment = EnrollmentRepository.get_by_id(db, enrollment_id)
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        if enrollment.user_id != user.id:
            raise HTTPException(status_code=403, detail="Cannot deregister from another student's enrollment")
        AuditRepository.create(db, enrollment_id, user.id, enrollment.course_id, "deregister")
        EnrollmentRepository.delete(db, enrollment)

    @staticmethod
    def admin_remove_enrollment(db: Session, enrollment_id: int, admin_id: int = None) -> None:
        enrollment = EnrollmentRepository.get_by_id(db, enrollment_id)
        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        AuditRepository.create(db, enrollment_id, admin_id or 0, enrollment.course_id, "admin_remove")
        EnrollmentRepository.delete(db, enrollment)