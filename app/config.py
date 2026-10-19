from functools import lru_cache

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    app_name: str = "AegisOps"
    app_version: str = "2.0.0"
    environment: str = "development"
    servicenow_url: str = ""
    servicenow_username: str = ""
    servicenow_password: str = ""
    servicenow_timeout: float = 10.0
    database_url: str = "sqlite:///./aegisops.db"
    redis_url: str = "redis://localhost:6379/0"

    api_host: str = "127.0.0.1"
    api_port: int = 8000
    jwt_secret: str = ""

    log_level: str = "INFO"

    # ============================================================
    # LLM CONFIGURATION
    # ============================================================

    # Supported providers:
    #   mock   -> free deterministic development mode
    #   ollama -> free local LLM
    #   openai -> optional cloud LLM
    llm_provider: str = "mock"

    # Model used by the selected provider
    llm_model: str = "local-development"

    # Used only by OpenAI
    openai_api_key: str = ""

    # Keep temperature deterministic
    llm_temperature: float = 0.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()