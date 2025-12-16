import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

from app.db import base  # noqa: E402
from app.db.session import SessionLocal, get_session, engine  # noqa: E402
import app.db.models.planning  # noqa: F401, E402
from app.main import app  # noqa: E402
from app.services.registry import db  # noqa: E402


def _override_get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def clean_database() -> None:
    db.reset()
    base.Base.metadata.drop_all(bind=engine)
    base.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="session")
def client() -> TestClient:
    app.dependency_overrides[get_session] = _override_get_session
    base.Base.metadata.create_all(bind=engine)
    return TestClient(app)


@pytest.fixture()
def session() -> SessionLocal:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
