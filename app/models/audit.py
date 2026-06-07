from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, String, func
from app.core.db import Base

class EnrollmentAudit(Base):
    __tablename__ = "enrollment_audit"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    enrollment_id: Mapped[int] = mapped_column(ForeignKey("enrollments.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    action: Mapped[str] = mapped_column(String(50))
    timestamp: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    details: Mapped[str] = mapped_column(String(500), nullable=True)
    
    enrollment: Mapped["Enrollment"] = relationship("Enrollment")
    user: Mapped["User"] = relationship("User")