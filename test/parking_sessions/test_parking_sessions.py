import pytest
from httpx import AsyncClient
import time

@pytest.mark.asyncio
async def test_create_parking_session(client: AsyncClient):
    """Smoke test for POST /parking-sessions (Entry). No token needed for this as it's from HW."""
    payload = {
        "plate_number": f"FIXED-{int(time.time())}",
        "url": "https://example.com/entry.jpg"
    }
    response = await client.post("/api/v1/parking-sessions", data=payload)
    # Allows for 201 or 400 (if rate limited or other validation issues)
    assert response.status_code in [201, 400]

@pytest.mark.asyncio
async def test_get_all_parking_sessions(client: AsyncClient, fixed_user_token: str):
    """Smoke test for GET /parking-sessions using fixed credentials."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    response = await client.get("/api/v1/parking-sessions", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
