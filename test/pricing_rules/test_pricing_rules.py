import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_all_pricing_rules(client: AsyncClient, fixed_user_token: str):
    """Smoke test for GET /pricing-rules API using fixed credentials."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    response = await client.get("/api/v1/pricing-rules", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
