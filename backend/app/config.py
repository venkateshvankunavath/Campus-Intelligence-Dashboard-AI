"""Central application configuration loaded from environment variables."""
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "Campus Intelligence API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"

    # Database (defaults to local SQLite so the project runs with zero setup;
    # set DATABASE_URL to a Postgres DSN in production / docker-compose)
    database_url: str = "sqlite:///./campus.db"

    # Auth
    secret_key: str = "change-me-in-production-please"
    access_token_expire_minutes: int = 60 * 24

    # AI
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"

    # RAG
    chroma_persist_dir: str = "./.chroma"
    embedding_model: str = "all-MiniLM-L6-v2"

    # CORS
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    class Config:
        env_file = ".env"
        extra = "ignore"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
