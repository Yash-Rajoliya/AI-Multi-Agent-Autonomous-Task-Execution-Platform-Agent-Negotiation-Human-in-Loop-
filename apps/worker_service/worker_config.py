from pydantic import BaseSettings


class WorkerConfig(BaseSettings):
    service_name: str = "worker-service"

    max_retries: int = 3
    retry_backoff_seconds: float = 2.0
    enable_dlq: bool = True
    dlq_name: str = "dead-letter-queue"

    class Config:
        env_file = ".env"


config = WorkerConfig()