from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FleetIQ API"
    api_prefix: str = "/api/v1"
    environment: str = "development"

    # Default to local sqlite for easier branch-level testing.
    # Production/staging should override DATABASE_URL via environment.
    database_url: str = "sqlite+pysqlite:///./fleetiq.db"

    # Async broker/result backend for Celery tasks.
    redis_url: str = "redis://redis:6379/0"

    secret_key: str = "change-me-in-prod"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
