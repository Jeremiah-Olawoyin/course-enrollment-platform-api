import pytest
from fastapi import status
from app.core.rate_limit import auth_rate_limit_store

async def get_student_token(client):
    response = await client.post("/api/v1/auth/register", json={
        "name": "Student",
        "email": "student@test.com",
        "password": "password123",
        "role": "student"
    })
    response = await client.post("/api/v1/auth/token", data={
        "username": "student@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]

async def get_admin_token(client):
    auth_rate_limit_store.clear()
    await client.post("/api/v1/auth/register", json={
        "name": "Admin",
        "email": "admin@test.com",
        "password": "password123",
        "role": "admin"
    })
    response = await client.post("/api/v1/auth/token", data={
        "username": "admin@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]

async def create_course(client, admin_token):
    response = await client.post("/api/v1/courses/",
        json={"title": "Enrollment Test", "code": "ENTEST", "capacity": 2},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    return response.json()["id"]

async def test_enroll_student_success(client):
    auth_rate_limit_store.clear()
    admin_token = await get_admin_token(client)
    auth_rate_limit_store.clear()
    student_token = await get_student_token(client)
    course_id = await create_course(client, admin_token)
    
    response = await client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user_id"] is not None
    assert response.json()["course_id"] == course_id

async def test_enroll_duplicate(client):
    auth_rate_limit_store.clear()
    admin_token = await get_admin_token(client)
    auth_rate_limit_store.clear()
    student_token = await get_student_token(client)
    course_id = await create_course(client, admin_token)
    
    await client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    
    response = await client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

async def test_enroll_course_full(client):
    auth_rate_limit_store.clear()
    admin_token = await get_admin_token(client)
    course_id = await create_course(client, admin_token)
    
    for i in range(3):
        auth_rate_limit_store.clear()
        await client.post("/api/v1/auth/register", json={
            "name": f"Student {i}",
            "email": f"student{i}@test.com",
            "password": "password123",
            "role": "student"
        })
        auth_rate_limit_store.clear()
        token_resp = await client.post("/api/v1/auth/token", data={
            "username": f"student{i}@test.com",
            "password": "password123"
        })
        student_token = token_resp.json()["access_token"]
        
        if i < 2:
            await client.post("/api/v1/enrollments/",
                json={"course_id": course_id},
                headers={"Authorization": f"Bearer {student_token}"}
            )
    
    response = await client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {await get_student_token(client)}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

async def test_deregister_own_enrollment(client):
    auth_rate_limit_store.clear()
    admin_token = await get_admin_token(client)
    auth_rate_limit_store.clear()
    student_token = await get_student_token(client)
    course_id = await create_course(client, admin_token)
    
    enroll_resp = await client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    enrollment_id = enroll_resp.json()["id"]
    
    response = await client.delete(f"/api/v1/enrollments/{enrollment_id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
