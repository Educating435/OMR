from functools import lru_cache

import json

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_env: str = "development"
    app_name: str = "OMR Scanner API"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "mysql+pymysql://root:root@localhost:3306/omr_scanner"
    jwt_secret_key: str = "change-me"
    access_token_expire_minutes: int = 480
    refresh_token_expire_days: int = 30
    storage_root: str = "storage"
    cors_origins: str = "http://localhost:5173"
    android_client_id: str = "android-scanner"
    admin_client_id: str = "admin-panel"

    @computed_field
    @property
    def cors_origins_list(self) -> list[str]:
        trimmed = self.cors_origins.strip()
        if not trimmed:
            return []
        if trimmed.startswith("["):
            parsed = json.loads(trimmed)
            if isinstance(parsed, list):
                return [str(item).strip() for item in parsed if str(item).strip()]
        return [item.strip() for item in trimmed.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
