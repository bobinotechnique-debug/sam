from collections.abc import Sequence

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL, make_url
from sqlalchemy.exc import ArgumentError


class Settings(BaseSettings):
    project_name: str = Field(default="Codex Starter", alias="PROJECT_NAME")
    project_version: str = Field(default="0.4.0", alias="PROJECT_VERSION")
    database_url: str = Field(
        default="postgresql://app_user:change_me@db:5432/app_db",
        alias="DATABASE_URL",
    )
    secret_key: str = Field(default="change_me", alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=60, alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    postgres_host: str = Field(default="db", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(default="app_db", alias="POSTGRES_DB")
    postgres_user: str = Field(default="app_user", alias="POSTGRES_USER")
    postgres_password: str = Field(default="change_me", alias="POSTGRES_PASSWORD")
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173"], alias="CORS_ORIGINS"
    )

    @property
    def sqlalchemy_database_uri(self) -> str:
        """Return a validated SQLAlchemy database URL.

        If ``database_url`` is empty, build it from the individual PostgreSQL
        settings. When a URL is provided but invalid, raise a clear error
        instead of letting SQLAlchemy fail with a generic parse exception.
        """

        if self.database_url and self.database_url.strip():
            try:
                make_url(self.database_url)
            except ArgumentError as exc:
                raise ValueError(
                    "DATABASE_URL is invalid; expected a full SQLAlchemy URL"
                ) from exc

            return self.database_url

        return URL.create(
            drivername="postgresql+psycopg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        ).render_as_string(hide_password=False)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | Sequence[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]

        if isinstance(value, Sequence):
            return list(value)

        raise TypeError("cors_origins must be a string or a sequence of strings")

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


settings = Settings()
