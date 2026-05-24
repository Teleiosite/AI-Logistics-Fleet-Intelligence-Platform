from functools import lru_cache

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FleetIQ API"
    api_prefix: str = "/api/v1"
    environment: str = "development"

    database_url: str = "sqlite+pysqlite:///./fleetiq.db"
    redis_url: str = "redis://redis:6379/0"

    secret_key: str = "change-me-in-prod"
    access_token_expire_minutes: int = 60

    cors_origins: list[str] = ["http://localhost:3000"]
    auto_create_tables: bool = False
    auth_rate_limit_requests: int = 10
    auth_rate_limit_window_seconds: int = 60

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @model_validator(mode="after")
    def validate_production_safety(self) -> "Settings":
        if self.environment.lower() == "production":
            if self.secret_key == "change-me-in-prod":
                raise ValueError("SECRET_KEY must be overridden in production")
            if self.auto_create_tables:
                raise ValueError("AUTO_CREATE_TABLES must be false in production")
            if not self.cors_origins:
                raise ValueError("CORS_ORIGINS must be configured in production")
        return self

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
