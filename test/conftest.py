import sys
import os
import asyncio
import pytest
from unittest.mock import MagicMock

# Define and add project paths to sys.path at the very beginning
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SRC_DIR = os.path.join(ROOT_DIR, 'src')

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from httpx import AsyncClient, ASGITransport
# Use 'app' prefix consistently with the application's internal imports.
# This prevents double-importing modules when 'src' is in sys.path.
from app.utils.supabase import AsyncSession
from app.main import app
from app.utils.database import get_db
from test.connect_database import SessionLocal, engine
from app.utils.mqtt_client import mqtt_client

# Mock MQTT Client to prevent real network calls during tests
@pytest.fixture(scope="session", autouse=True)
def mock_mqtt():
    mqtt_client.connect = MagicMock()
    mqtt_client.disconnect = MagicMock()
    mqtt_client.send_payment_start = MagicMock()
    mqtt_client.open_servo = MagicMock()
    mqtt_client._publish_control = MagicMock()
    return mqtt_client

@pytest.fixture(scope="function")
async def db_session():
    """Returns an asynchronous database session."""
    async with SessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
async def client(db_session: AsyncSession):
    """Returns an asynchronous FastAPI TestClient (httpx.AsyncClient)."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def fixed_user_token(client: AsyncClient):
    """Logs in with the specific credentials provided by the user and returns the token."""
    login_payload = {
        "email": "dangviethung@gmail.com",
        "password": "Dangviethung@21"
    }
    response = await client.post("/api/v1/auth/login", json=login_payload)
    if response.status_code == 200:
        return response.json()["access_token"]
    
    # If login fails, try to register it first (in case it's a new environment)
    # but based on the request, it likely already exists.
    register_payload = {
        **login_payload,
        "full_name": "Dang Viet Hung",
        "phone": "0987654321",
        "role_id": "e34be2cc-e5a1-49fc-89bd-f80309dcc655" # Admin role
    }
    await client.post("/api/v1/auth/register", json=register_payload)
    response = await client.post("/api/v1/auth/login", json=login_payload)
    return response.json().get("access_token")

@pytest.fixture(scope="function")
def test_user_data():
    """Generates unique test user data for registration/login tests."""
    import time
    timestamp = int(time.time())
    return {
        "email": f"testuser_{timestamp}@example.com",
        "password": "Password123@!",
        "full_name": "Test User",
        "phone": f"+8498{timestamp % 10000000:07d}",
        "role_id": "d4c52c93-3750-4cff-8534-b3da8978aa3c" # Actual 'User' role ID
    }
