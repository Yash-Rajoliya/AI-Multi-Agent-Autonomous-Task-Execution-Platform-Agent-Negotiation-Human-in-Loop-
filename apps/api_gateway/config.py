from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "AI Autonomous Agent Platform"
    DEBUG: bool = False

    # Security
    JWT_SECRET: str = "super-secret"
    JWT_ALGORITHM: str = "HS256"

    # Infra
    REDIS_URL: str
    DATABASE_URL: str

    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 100

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()