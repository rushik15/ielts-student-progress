from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "IELTS Student Progress Portal API"
    secret_key: str = "development-only-change-me"
    access_token_expire_minutes: int = 1440
    database_url: str = "sqlite:///./ielts_progress.db"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    bootstrap_admin_number: str = "admin001"
    bootstrap_admin_password: str = "change-me-now"
    bootstrap_admin_name: str = "Portal Admin"
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False, extra="ignore")

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
