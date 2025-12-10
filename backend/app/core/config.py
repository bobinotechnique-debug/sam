from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    project_name: str = Field(default="Codex Starter", alias="PROJECT_NAME")
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

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


settings = Settings()
