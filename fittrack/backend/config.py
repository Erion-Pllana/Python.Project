"""
backend/config.py

Centralized application configuration.

Loads values from environment variables / a local .env file using
pydantic-settings. Every other backend module should import `settings`
from here rather than calling os.getenv() directly, so all configuration
stays in one place.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---- Application ----
    app_name: str = "FitTrack"
    app_env: str = "development"
    debug: bool = True

    # ---- FastAPI backend ----
    backend_host: str = "127.0.0.1"
    backend_port: int = 8000

    # ---- Streamlit frontend ----
    api_base_url: str = "http://127.0.0.1:8000"
    cors_origins: str = "http://localhost:8501,http://127.0.0.1:8501"

    # ---- MySQL database ----
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str = "fittrack_user"
    db_password: str = "change_me"
    db_name: str = "fittrack"

    # ---- Security ----
    secret_key: str = "change_this_to_a_long_random_string"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    @property
    def database_url(self) -> str:
        """SQLAlchemy connection URL for MySQL via PyMySQL."""
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()