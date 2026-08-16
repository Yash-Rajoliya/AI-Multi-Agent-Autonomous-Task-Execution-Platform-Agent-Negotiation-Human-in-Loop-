from pydantic import BaseSettings
from functools import lru_cache


class RuntimeConfig(BaseSettings):
    ENV: str = "dev"
    MAX_CONCURRENT_AGENTS: int = 10
    EXECUTION_TIMEOUT: int = 30

    SANDBOX_ENABLED: bool = True
    TOOL_TIMEOUT: int = 10

    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache()
def get_config() -> RuntimeConfig:
    return RuntimeConfig()