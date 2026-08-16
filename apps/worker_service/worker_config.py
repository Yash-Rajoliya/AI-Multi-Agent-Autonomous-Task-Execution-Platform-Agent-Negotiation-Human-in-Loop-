from pydantic import BaseSettings, Field


class WorkerConfig(BaseSettings):
    service_name: str = "worker-service"

    queue_name: str = "task-queue"
    dead_letter_queue: str = "dlq-task-queue"

    max_retries: int = 5
    retry_backoff_base: int = 2  # exponential base

    concurrency: int = 5
    poll_interval: float = 1.0

    enable_idempotency: bool = True

    redis_url: str = Field(default="redis://localhost:6379/0")

    class Config:
        env_file = ".env"


config = WorkerConfig()