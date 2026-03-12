from fastapi.testclient import TestClient


def create_user_and_login(client: TestClient, email: str, password: str = "securepassword"):
    client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Test User"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password
    })
    return response.json()["access_token"]


def test_list_users_authenticated(client: TestClient):
    token = create_user_and_login(client, "list@example.com")
    response = client.get(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_list_users_unauthenticated(client: TestClient):
    response = client.get("/api/v1/users/")
    assert response.status_code == 401


def test_get_me(client: TestClient):
    token = create_user_and_login(client, "me@example.com")
    response = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "me@example.com"


def test_get_user_by_id(client: TestClient):
    token = create_user_and_login(client, "byid@example.com")
    me = client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    ).json()
    response = client.get(
        f"/api/v1/users/{me['id']}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == me["id"]


def test_get_user_not_found(client: TestClient):
    token = create_user_and_login(client, "notfound@example.com")
    response = client.get(
        "/api/v1/users/99999",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 404


def test_delete_user_requires_admin(client: TestClient):
    token = create_user_and_login(client, "nodelete@example.com")
    response = client.delete(
        "/api/v1/users/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403