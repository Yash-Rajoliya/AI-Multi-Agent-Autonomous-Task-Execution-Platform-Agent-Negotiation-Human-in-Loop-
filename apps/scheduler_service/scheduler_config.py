from pydantic import BaseSettings


class SchedulerConfig(BaseSettings):
    service_name: str = "scheduler-service"

    enable_distributed_lock: bool = True
    lock_key_prefix: str = "scheduler-lock"

    retry_attempts: int = 3
    retry_backoff: int = 2

    tick_interval: int = 5  # seconds

    redis_url: str = "redis://localhost:6379/2"

    class Config:
        env_file = ".env"


config = SchedulerConfig()