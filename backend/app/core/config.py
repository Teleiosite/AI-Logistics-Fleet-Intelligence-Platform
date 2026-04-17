from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FleetIQ API"
    api_prefix: str = "/api/v1"
    environment: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@db:5432/fleetiq"
    redis_url: str = "redis://redis:6379/0"
    secret_key: str = "change-me-in-prod"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
