import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_revenue(client: AsyncClient, fixed_user_token: str):
    """Smoke test for GET /invoices/ (Revenue) using fixed credentials."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    response = await client.get("/api/v1/invoices/", headers=headers)
    # Expected 200 if Admin, 403 if User
    assert response.status_code in [200, 403]
    if response.status_code == 200:
        data = response.json()
        assert "total_revenue" in data
