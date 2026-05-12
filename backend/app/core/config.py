"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings for the backend service."""

    model_config = SettingsConfigDict(
        env_file=(".env", "backend/.env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = "MW.AI Data and Systems API"
    environment: str = "local"
    log_level: str = "INFO"
    api_prefix: str = "/api/v1"

    database_url: str = "postgresql+asyncpg://mwai:mwai_password@localhost:5432/mwai_crm"
    sql_echo: bool = False

    jwt_secret_key: str = Field(default="replace-with-a-long-random-secret", min_length=16)
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    backend_cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins(self) -> list[str]:
        """Return configured CORS origins from a comma-separated env value."""
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]

    @property
    def sync_database_url(self) -> str:
        """Return a synchronous SQLAlchemy URL for Alembic migrations."""
        return self.database_url.replace("+asyncpg", "+psycopg2")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()


settings = get_settings()

