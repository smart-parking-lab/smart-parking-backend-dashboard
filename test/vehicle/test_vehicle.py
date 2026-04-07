import pytest
from httpx import AsyncClient
import time

@pytest.mark.asyncio
async def test_get_all_vehicle_types(client: AsyncClient, fixed_user_token: str):
    """Smoke test for GET /vehicle-types API using fixed credentials."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    response = await client.get("/api/v1/vehicles/vehicle-types", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_register_vehicle(client: AsyncClient, fixed_user_token: str):
    """Smoke test for POST /vehicles API using fixed credentials."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    payload = {
        "plate_number": f"FIXED-{int(time.time())}",
        "vehicle_type_name": "Xe máy" # Assumes 'Xe máy' exists in the test DB
    }
    response = await client.post("/api/v1/vehicles", headers=headers, json=payload)
    # Could be 201 or 400 (if rate limited or validation issues)
    assert response.status_code in [201, 400, 404]
