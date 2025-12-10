import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.registry import db


@pytest.fixture(autouse=True)
def reset_database() -> None:
    db.reset()


@pytest.fixture(scope="session")
def client() -> TestClient:
    return TestClient(app)
