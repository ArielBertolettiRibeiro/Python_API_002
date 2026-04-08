from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str
    debug: bool
    port: int
    app_env: str
    api_version: str
    host: str
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    access_refresh_token_expire_minutes: int
    allowed_origins: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()