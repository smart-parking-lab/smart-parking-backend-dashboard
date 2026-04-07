import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_all_parking_slots(client: AsyncClient, fixed_user_token: str):
    """Smoke test for GET /parking-slots/ API using fixed credentials."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    response = await client.get("/api/v1/parking-slots/", headers=headers)
    assert response.status_code in [200, 403]
    if response.status_code == 200:
        assert isinstance(response.json(), list)
