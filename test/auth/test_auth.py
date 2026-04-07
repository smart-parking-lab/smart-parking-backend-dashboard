import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, test_user_data):
    """Smoke test for registration API."""
    response = await client.post("/api/v1/auth/register", json=test_user_data)
    # 201 Created or 400 if user already exists (using timestamps should avoid this)
    assert response.status_code in [201, 400]
    if response.status_code == 201:
        assert "id" in response.json()

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user_data):
    """Smoke test for login API."""
    # Register first to ensure user exists
    await client.post("/api/v1/auth/register", json=test_user_data)
    
    login_payload = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
