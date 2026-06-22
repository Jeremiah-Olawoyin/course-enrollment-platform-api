import pytest
from fastapi import status

async def test_register_success(client):
    response = await client.post("/api/v1/auth/register", json={
        "name": "Test Student",
        "email": "student@test.com",
        "password": "password123",
        "role": "student"
    })
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "student@test.com"
    assert data["name"] == "Test Student"
    assert data["role"] == "student"
    assert "id" in data

async def test_register_duplicate_email(client):
    await client.post("/api/v1/auth/register", json={
        "name": "Student 1",
        "email": "dup@test.com",
        "password": "password123"
    })
    response = await client.post("/api/v1/auth/register", json={
        "name": "Student 2",
        "email": "dup@test.com",
        "password": "password123"
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST

async def test_login_success(client):
    await client.post("/api/v1/auth/register", json={
        "name": "Login Test",
        "email": "login@test.com",
        "password": "password123"
    })
    response = await client.post("/api/v1/auth/token", data={
        "username": "login@test.com",
        "password": "password123"
    })
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

async def test_login_invalid_credentials(client):
    response = await client.post("/api/v1/auth/token", data={
        "username": "nonexistent@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
