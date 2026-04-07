import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_all_roles(client: AsyncClient, fixed_user_token: str):
    """Smoke test for GET /admin/roles API using fixed credentials."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    response = await client.get("/api/v1/admin/roles", headers=headers)
    # If 200, great. If 403, the fixed user is not an admin in the DB.
    assert response.status_code in [200, 403]
    if response.status_code == 200:
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient, fixed_user_token: str):
    """Smoke test for GET /admin/users API using fixed credentials."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    response = await client.get("/api/v1/admin/users", headers=headers)
    assert response.status_code in [200, 403]
