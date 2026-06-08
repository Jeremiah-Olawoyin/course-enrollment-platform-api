# Course Enrollment Platform API

A FastAPI-based REST API for course enrollment management with JWT authentication and role-based access control.

## Features

- User registration and authentication (JWT tokens)
- Role-based access control (student/admin)
- Course CRUD operations (admin only)
- Student enrollment with capacity enforcement
- SQLite in-memory testing support
- Audit logs for enrollment actions (admin feature)
- Rate limiting on authentication endpoints (5 requests per 60 seconds)

## Project Structure

```
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py           # Authentication endpoints
│   │       ├── users.py          # User management endpoints
│   │       ├── courses.py        # Course CRUD endpoints
│   │       └── enrollments.py    # Enrollment endpoints
│   ├── core/
│   │   ├── config.py             # Application configuration
│   │   ├── db.py                 # Database setup
│   │   ├── deps.py               # Dependency injection
│   │   ├── rate_limit.py         # Rate limiting middleware
│   │   └── security.py           # JWT and password utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # User model
│   │   ├── course.py             # Course model
│   │   ├── enrollment.py           # Enrollment model
│   │   └── audit.py              # Audit log model
│   ├── repository/
│   │   ├── user_repository.py      # User data access
│   │   ├── course_repository.py    # Course data access
│   │   ├── enrollment_repository.py # Enrollment data access
│   │   └── audit_repository.py     # Audit log data access
│   ├── schemas/
│   │   └── user.py               # Pydantic schemas
│   └── services/
│       ├── auth_service.py         # Authentication logic
│       ├── course_service.py       # Course business logic
│       └── enrollment_service.py   # Enrollment business logic
├── tests/
│   ├── conftest.py              # Test configuration
│   ├── test_auth.py             # Auth tests
│   ├── test_courses.py          # Course tests
│   └── test_enrollments.py      # Enrollment tests
├── alembic.ini                   # Alembic configuration
├── start.sh                      # Startup script with migrations
├── requirements.txt              # Python dependencies
└── README.md
```

## Setup

### Prerequisites

- Python 3.10+
- PostgreSQL (for production)

### Installation

```bash
# Clone and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Configuration

Create `.env` file with:

```
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://postgres:password@localhost:5432/course_enrollment_db
```

### Database Migration

```bash
# Initialize Alembic (if not done)
alembic init alembic

# Apply migrations to PostgreSQL
alembic upgrade head
```

## Running the Application

```bash
uvicorn app.main:app --reload --port 8000
```

API documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
pytest tests/ -v
```

Tests use SQLite in-memory database for isolation.

## Render Deployment

### Quick Deploy

1. Create PostgreSQL database on Render
2. Create Web Service and link to database
3. Environment variables are auto-set when database linked
4. Render auto-deploys on push to `main` branch

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string (auto-set via database linking) |
| `SECRET_KEY` | JWT secret key for token signing |
| `ALGORITHM` | JWT algorithm (default: HS256) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time (default: 30) |

### Live API Endpoints

- Swagger UI: `https://course-enrollment-platform-api-lpnu.onrender.com/docs`
- ReDoc: `https://course-enrollment-platform-api-lpnu.onrender.com/redoc`
- API Base: `https://course-enrollment-platform-api-lpnu.onrender.com/api/v1`