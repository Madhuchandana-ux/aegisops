from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration for AegisOps.

    Values can come from:
    1. Environment variables
    2. The .env file
    3. Default values defined below
    """

    app_name: str = "AegisOps"
    app_version: str = "2.0.0"
    environment: str = "development"

    api_host: str = "127.0.0.1"
    api_port: int = 8000

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings object.

    Caching prevents us from repeatedly loading
    configuration throughout the application.
    """

    return Settings()