from __future__ import annotations

from functools import lru_cache
from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    groq_api_key: str
    internal_api_key: str
    max_file_size_mb: int
    allowed_file_types: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    def allowed_file_type_set(self) -> Set[str]:
        return {item.strip().lower() for item in self.allowed_file_types.split(",") if item.strip()}


@lru_cache
def get_settings() -> Settings:
    return Settings()
