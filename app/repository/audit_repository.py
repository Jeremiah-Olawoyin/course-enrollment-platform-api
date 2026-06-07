from sqlalchemy.orm import Session
from app.models.audit import EnrollmentAudit

class AuditRepository:
    @staticmethod
    def create(db: Session, enrollment_id: int, user_id: int, course_id: int, action: str, details: str = None) -> EnrollmentAudit:
        audit = EnrollmentAudit(
            enrollment_id=enrollment_id,
            user_id=user_id,
            course_id=course_id,
            action=action,
            details=details
        )
        db.add(audit)
        db.commit()
        db.refresh(audit)
        return audit
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> list[EnrollmentAudit]:
        return db.query(EnrollmentAudit).offset(skip).limit(limit).all()