from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1 import auth, users, courses, enrollments
from app.core.db import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Course Enrollment Platform API", version="1.0.0", lifespan=lifespan)

@app.get("/")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(enrollments.router, prefix="/api/v1")
