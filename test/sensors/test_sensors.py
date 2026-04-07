import pytest
from httpx import AsyncClient
import uuid

@pytest.mark.asyncio
async def test_get_all_sensors(client: AsyncClient, fixed_user_token: str):
    """Smoke test for GET /sensors/ API using fixed credentials."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    response = await client.get("/api/v1/sensors/", headers=headers)
    assert response.status_code in [200, 403]
    if response.status_code == 200:
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_sensor(client: AsyncClient, fixed_user_token: str):
    """Smoke test for POST /sensors/ API with valid slot_id."""
    headers = {"Authorization": f"Bearer {fixed_user_token}"}
    
    # 1. Fetch an existing slot to get its ID
    slot_res = await client.get("/api/v1/parking-slots/", headers=headers)
    assert slot_res.status_code == 200
    slots = slot_res.json()
    assert len(slots) > 0, "Need at least one parking slot in DB for this test"
    
    slot_id = slots[0]["id"]
    
    # 2. Create the sensor using the real slot_id
    payload = {
        "sensor_code": f"SN-{uuid.uuid4().hex[:6]}",
        "slot_id": slot_id,
        "status": "offline"
    }
    response = await client.post("/api/v1/sensors/", headers=headers, json=payload)
    # Status should be 201 Created or 403 (if role permissions change)
    assert response.status_code in [201, 403]
