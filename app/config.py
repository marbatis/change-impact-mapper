from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./impact_mapper.db"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def normalized_database_url(self) -> str:
        if self.database_url.startswith("postgres://"):
            return self.database_url.replace("postgres://", "postgresql://", 1)
        return self.database_url


@lru_cache
def get_settings() -> Settings:
    return Settings()
