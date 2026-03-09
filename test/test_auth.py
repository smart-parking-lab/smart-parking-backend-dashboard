import pytest
from fastapi.testclient import TestClient

# We use fixture scopes sensibly so a single user can be shared across tests
# if order is preserved, but since tests can be run in any order, 
# we'll create the user in the register test and use it in later tests.

@pytest.fixture(scope="module")
def shared_test_data(test_user_data):
    """Stores shared state across tests in the module like tokens."""
    return {
        "user_data": test_user_data,
        "access_token": None,
        "refresh_token": None
    }


def test_register_success(client: TestClient, shared_test_data: dict):
    user_data = shared_test_data["user_data"]
    response = client.post("/api/v1/auth/register", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "role_name" in data


def test_register_duplicate_email(client: TestClient, shared_test_data: dict):
    user_data = shared_test_data["user_data"]
    # Trying to register again with same payload
    response = client.post("/api/v1/auth/register", json=user_data)
    
    # HTTP validator runs first, or DB unique checks
    assert response.status_code == 400
    assert "Email đã được sử dụng" in response.json().get("detail", "")


def test_login_success(client: TestClient, shared_test_data: dict):
    user_data = shared_test_data["user_data"]
    login_payload = {
        "email": user_data["email"],
        "password": user_data["password"]
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    
    shared_test_data["access_token"] = data["access_token"]
    shared_test_data["refresh_token"] = data["refresh_token"]


def test_login_invalid_credentials(client: TestClient, shared_test_data: dict):
    user_data = shared_test_data["user_data"]
    login_payload = {
        "email": user_data["email"],
        "password": "WrongPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=login_payload)
    
    assert response.status_code == 401
    assert "Email hoặc mật khẩu không đúng" in response.json().get("detail", "")


def test_get_me_success(client: TestClient, shared_test_data: dict):
    access_token = shared_test_data.get("access_token")
    assert access_token is not None, "Login failed, missing token"
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == shared_test_data["user_data"]["email"]


def test_get_me_unauthorized(client: TestClient):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_change_password_success(client: TestClient, shared_test_data: dict):
    access_token = shared_test_data.get("access_token")
    user_data = shared_test_data["user_data"]
    assert access_token is not None
    
    headers = {"Authorization": f"Bearer {access_token}"}
    new_password = "NewPassword123@!"
    
    payload = {
        "password": user_data["password"],
        "new_password": new_password,
        "check_password": new_password
    }
    response = client.post("/api/v1/auth/change-password", headers=headers, json=payload)
    
    assert response.status_code == 200
    assert response.json().get("message") == "Đổi mật khẩu thành công"
    
    # Update shared testing data so login works if needed later
    shared_test_data["user_data"]["password"] = new_password


def test_change_password_wrong_old(client: TestClient, shared_test_data: dict):
    access_token = shared_test_data.get("access_token")
    user_data = shared_test_data["user_data"]
    assert access_token is not None
    
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "password": "WrongOldPassword123!",
        "new_password": "NewPassword123@!V2",
        "check_password": "NewPassword123@!V2"
    }
    response = client.post("/api/v1/auth/change-password", headers=headers, json=payload)
    
    assert response.status_code == 401
    assert "Mật khẩu cũ không đúng" in response.json().get("detail", "")


def test_refresh_token_success(client: TestClient, shared_test_data: dict):
    refresh_token = shared_test_data.get("refresh_token")
    assert refresh_token is not None
    
    payload = {
        "refresh_token": refresh_token
    }
    response = client.post("/api/v1/auth/refresh", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid(client: TestClient):
    payload = {
        "refresh_token": "invalid_refresh_token_string"
    }
    response = client.post("/api/v1/auth/refresh", json=payload)
    
    assert response.status_code == 401
    assert "Refresh token không hợp lệ" in response.json().get("detail", "")
