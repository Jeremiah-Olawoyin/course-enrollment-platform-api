import pytest
from fastapi import status
from app.core.rate_limit import auth_rate_limit_store

def get_student_token(client):
    response = client.post("/api/v1/auth/register", json={
        "name": "Student",
        "email": "student@test.com",
        "password": "password123",
        "role": "student"
    })
    response = client.post("/api/v1/auth/token", data={
        "username": "student@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]

def get_admin_token(client):
    auth_rate_limit_store.clear()
    client.post("/api/v1/auth/register", json={
        "name": "Admin",
        "email": "admin@test.com",
        "password": "password123",
        "role": "admin"
    })
    response = client.post("/api/v1/auth/token", data={
        "username": "admin@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]

def create_course(client, admin_token):
    response = client.post("/api/v1/courses/",
        json={"title": "Enrollment Test", "code": "ENTEST", "capacity": 2},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    return response.json()["id"]

def test_enroll_student_success(client):
    auth_rate_limit_store.clear()
    admin_token = get_admin_token(client)
    auth_rate_limit_store.clear()
    student_token = get_student_token(client)
    course_id = create_course(client, admin_token)
    
    response = client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["user_id"] is not None
    assert response.json()["course_id"] == course_id

def test_enroll_duplicate(client):
    auth_rate_limit_store.clear()
    admin_token = get_admin_token(client)
    auth_rate_limit_store.clear()
    student_token = get_student_token(client)
    course_id = create_course(client, admin_token)
    
    client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    
    response = client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_enroll_course_full(client):
    auth_rate_limit_store.clear()
    admin_token = get_admin_token(client)
    course_id = create_course(client, admin_token)
    
    for i in range(3):
        auth_rate_limit_store.clear()
        client.post("/api/v1/auth/register", json={
            "name": f"Student {i}",
            "email": f"student{i}@test.com",
            "password": "password123",
            "role": "student"
        })
        auth_rate_limit_store.clear()
        token_resp = client.post("/api/v1/auth/token", data={
            "username": f"student{i}@test.com",
            "password": "password123"
        })
        student_token = token_resp.json()["access_token"]
        
        if i < 2:
            client.post("/api/v1/enrollments/",
                json={"course_id": course_id},
                headers={"Authorization": f"Bearer {student_token}"}
            )
    
    response = client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {get_student_token(client)}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_deregister_own_enrollment(client):
    auth_rate_limit_store.clear()
    admin_token = get_admin_token(client)
    auth_rate_limit_store.clear()
    student_token = get_student_token(client)
    course_id = create_course(client, admin_token)
    
    enroll_resp = client.post("/api/v1/enrollments/",
        json={"course_id": course_id},
        headers={"Authorization": f"Bearer {student_token}"}
    )
    enrollment_id = enroll_resp.json()["id"]
    
    response = client.delete(f"/api/v1/enrollments/{enrollment_id}",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT