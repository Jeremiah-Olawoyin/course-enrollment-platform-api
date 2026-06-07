from pydantic import BaseModel, EmailStr
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: str | None = None
    role: str | None = None

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True

class UserReadWithEnrollments(UserRead):
    enrollments: list["EnrollmentRead"] = []

class CourseCreate(BaseModel):
    title: str
    code: str
    capacity: int

class CourseUpdate(BaseModel):
    title: str | None = None
    code: str | None = None
    capacity: int | None = None

class CourseRead(BaseModel):
    id: int
    title: str
    code: str
    capacity: int
    is_active: bool
    
    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    course_id: int

class EnrollmentRead(BaseModel):
    id: int
    user_id: int
    course_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class EnrollmentReadWithDetails(EnrollmentRead):
    user: UserRead
    course: CourseRead