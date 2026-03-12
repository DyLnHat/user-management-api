from fastapi.testclient import TestClient


def test_register_success(client: TestClient):
    response = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "securepassword",
        "full_name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "hashed_password" not in data


def test_register_duplicate_email(client: TestClient):
    payload = {
        "email": "duplicate@example.com",
        "password": "securepassword",
        "full_name": "Test User"
    }
    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


def test_register_short_password(client: TestClient):
    response = client.post("/api/v1/auth/register", json={
        "email": "short@example.com",
        "password": "123",
        "full_name": "Test User"
    })
    assert response.status_code == 400


def test_login_success(client: TestClient):
    client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "password": "securepassword",
        "full_name": "Test User"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient):
    client.post("/api/v1/auth/register", json={
        "email": "wrong@example.com",
        "password": "securepassword",
        "full_name": "Test User"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401


def test_login_nonexistent_user(client: TestClient):
    response = client.post("/api/v1/auth/login", json={
        "email": "ghost@example.com",
        "password": "securepassword"
    })
    assert response.status_code == 401