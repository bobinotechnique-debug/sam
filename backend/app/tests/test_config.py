import pytest

from app.core.config import Settings


def test_plain_sqlite_path_is_normalized(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "data/test.db")

    settings = Settings()

    assert settings.sqlalchemy_database_uri == "sqlite:///data/test.db"


def test_invalid_database_url_raises(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "not a url")

    with pytest.raises(ValueError):
        Settings().sqlalchemy_database_uri
