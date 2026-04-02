from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_name: str = "OMR Scanner API"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False
    database_url: str = "sqlite:///./omr_scanner.db"
    jwt_secret_key: str = "change-me"
    jwt_refresh_secret_key: str = "change-me-too"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 30
    storage_root: str = "uploads"
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])
    allow_credentials: bool = True
    default_page_size: int = 20
    max_page_size: int = 100
    rate_limit_enabled: bool = False
    rate_limit_default: str = "120/minute"
    auto_create_schema: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
