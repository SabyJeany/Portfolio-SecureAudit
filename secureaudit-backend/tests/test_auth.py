"""
tests/test_auth.py — Tests for authentication routes

Tests:
- POST /api/auth/register → create account
- POST /api/auth/login → login and get JWT
- GET /api/auth/me → get current user
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

# Test client — simulates HTTP requests without running a real server
client = TestClient(app)


def test_register_success():
    """
    Test successful user registration.
    Should return 201 with token and user data.
    """
    response = client.post("/api/auth/register", json={
        "email": "test_register@test.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert "user" in data
    assert data["user"]["email"] == "test_register@test.com"


def test_register_duplicate_email():
    """
    Test registration with an email that already exists.
    Should return 400 Bad Request.
    """
    # Register first time
    client.post("/api/auth/register", json={
        "email": "duplicate@test.com",
        "password": "password123"
    })

    # Try to register again with same email
    response = client.post("/api/auth/register", json={
        "email": "duplicate@test.com",
        "password": "password123"
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_login_success():
    """
    Test successful login.
    Should return 200 with token and user data.
    """
    # First register
    client.post("/api/auth/register", json={
        "email": "test_login@test.com",
        "password": "password123"
    })

    # Then login
    response = client.post("/api/auth/login", json={
        "email": "test_login@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["user"]["email"] == "test_login@test.com"


def test_login_wrong_password():
    """
    Test login with wrong password.
    Should return 401 Unauthorized.
    """
    # Register first
    client.post("/api/auth/register", json={
        "email": "test_wrong@test.com",
        "password": "password123"
    })

    # Login with wrong password
    response = client.post("/api/auth/login", json={
        "email": "test_wrong@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_unknown_email():
    """
    Test login with email that doesn't exist.
    Should return 401 Unauthorized.
    """
    response = client.post("/api/auth/login", json={
        "email": "unknown@test.com",
        "password": "password123"
    })
    assert response.status_code == 401


def test_get_me_with_valid_token():
    """
    Test GET /api/auth/me with a valid JWT token.
    Should return 200 with user data.
    """
    # Register and get token
    register_response = client.post("/api/auth/register", json={
        "email": "test_me@test.com",
        "password": "password123"
    })
    token = register_response.json()["token"]

    # Get current user
    response = client.get("/api/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "test_me@test.com"


def test_get_me_without_token():
    """
    Test GET /api/auth/me without token.
    Should return 403 Forbidden.
    """
    response = client.get("/api/auth/me")
    assert response.status_code == 403