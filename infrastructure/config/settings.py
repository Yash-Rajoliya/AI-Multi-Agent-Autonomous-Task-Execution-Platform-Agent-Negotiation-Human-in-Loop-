from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    ENV: str = "development"

    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # Redis
    REDIS_URL: str = Field(..., env="REDIS_URL")

    # Messaging
    KAFKA_BROKER: str = Field(..., env="KAFKA_BROKER")

    # LLM
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")

    # Observability
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()