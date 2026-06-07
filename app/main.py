from fastapi import FastAPI
from app.api.v1 import auth, users, courses, enrollments

app = FastAPI(title="Course Enrollment Platform API", version="1.0.0")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(enrollments.router, prefix="/api/v1")