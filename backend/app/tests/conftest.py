import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")

import app.db.models.planning as _planning_models  # noqa: F401, E402
from app.db import base  # noqa: E402
from app.db.session import SessionLocal, engine, get_session  # noqa: E402
from app.main import app  # noqa: E402
from app.services.registry import db  # noqa: E402


def _override_get_session() -> Generator[Session, None, None]:
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
def session() -> Generator[Session, None, None]:
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
