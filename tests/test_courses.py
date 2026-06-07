import pytest
from fastapi import status

def get_admin_token(client):
    client.post("/api/v1/auth/register", json={
        "name": "Admin User",
        "email": "admin@test.com",
        "password": "password123",
        "role": "admin"
    })
    response = client.post("/api/v1/auth/token", data={
        "username": "admin@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]

def test_get_courses_empty(client):
    response = client.get("/api/v1/courses/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_create_course_admin(client):
    token = get_admin_token(client)
    response = client.post("/api/v1/courses/", 
        json={"title": "Math 101", "code": "MATH101", "capacity": 30},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Math 101"
    assert data["code"] == "MATH101"
    assert data["capacity"] == 30

def test_get_courses_with_data(client):
    token = get_admin_token(client)
    client.post("/api/v1/courses/",
        json={"title": "Physics 101", "code": "PHYS101", "capacity": 25},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.get("/api/v1/courses/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

def test_get_single_course(client):
    token = get_admin_token(client)
    create_resp = client.post("/api/v1/courses/",
        json={"title": "Chemistry", "code": "CHEM101", "capacity": 20},
        headers={"Authorization": f"Bearer {token}"}
    )
    course_id = create_resp.json()["id"]
    
    response = client.get(f"/api/v1/courses/{course_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["code"] == "CHEM101"

def test_create_course_duplicate_code(client):
    token = get_admin_token(client)
    client.post("/api/v1/courses/",
        json={"title": "Course 1", "code": "DUPLICATE", "capacity": 10},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = client.post("/api/v1/courses/",
        json={"title": "Course 2", "code": "DUPLICATE", "capacity": 10},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST