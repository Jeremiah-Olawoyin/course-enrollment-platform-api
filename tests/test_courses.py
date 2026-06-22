import pytest
from fastapi import status

async def get_admin_token(client):
    await client.post("/api/v1/auth/register", json={
        "name": "Admin User",
        "email": "admin@test.com",
        "password": "password123",
        "role": "admin"
    })
    response = await client.post("/api/v1/auth/token", data={
        "username": "admin@test.com",
        "password": "password123"
    })
    return response.json()["access_token"]

async def test_get_courses_empty(client):
    response = await client.get("/api/v1/courses/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

async def test_create_course_admin(client):
    token = await get_admin_token(client)
    response = await client.post("/api/v1/courses/", 
        json={"title": "Math 101", "code": "MATH101", "capacity": 30},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Math 101"
    assert data["code"] == "MATH101"
    assert data["capacity"] == 30

async def test_get_courses_with_data(client):
    token = await get_admin_token(client)
    await client.post("/api/v1/courses/",
        json={"title": "Physics 101", "code": "PHYS101", "capacity": 25},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await client.get("/api/v1/courses/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1

async def test_get_single_course(client):
    token = await get_admin_token(client)
    create_resp = await client.post("/api/v1/courses/",
        json={"title": "Chemistry", "code": "CHEM101", "capacity": 20},
        headers={"Authorization": f"Bearer {token}"}
    )
    course_id = create_resp.json()["id"]
    
    response = await client.get(f"/api/v1/courses/{course_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["code"] == "CHEM101"

async def test_create_course_duplicate_code(client):
    token = await get_admin_token(client)
    await client.post("/api/v1/courses/",
        json={"title": "Course 1", "code": "DUPLICATE", "capacity": 10},
        headers={"Authorization": f"Bearer {token}"}
    )
    response = await client.post("/api/v1/courses/",
        json={"title": "Course 2", "code": "DUPLICATE", "capacity": 10},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
