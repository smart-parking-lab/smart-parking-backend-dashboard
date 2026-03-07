import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from src.app.utils.database import get_db
from test.connect_database import SessionLocal, engine, Base


# Create tables if not exists (although they should exist in the real DB)
Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def db_session():
    """Returns a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client(db_session: Session):
    """Returns a FastAPI TestClient configured to use the test database session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass # The session is managed by the db_session fixture

    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up override after tests
    app.dependency_overrides.clear()


@pytest.fixture(scope="module")
def test_user_data():
    """Generates unique test user data for registration/login tests."""
    import time
    timestamp = int(time.time())
    return {
        "email": f"testuser_{timestamp}@example.com",
        "password": "Password123@!",
        "full_name": "Test User",
        "phone": f"+8498{timestamp % 10000000:07d}",
        "role_id": 1
    }
