from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    app_env: str = "development"
    app_url: str = "http://localhost:3000"
    api_url: str = "http://localhost:8000"
    cors_origins: str = "http://localhost:3000"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/trendradar"
    sync_database_url: str = "postgresql://postgres:postgres@localhost:5432/trendradar"

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Supabase
    supabase_url: str = ""
    supabase_service_key: str = ""
    supabase_jwt_secret: str = ""

    # AI
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # Stripe
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""

    # Reddit
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "TrendRadar/1.0"

    # YouTube
    youtube_api_key: str = ""

    # Email
    resend_api_key: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
