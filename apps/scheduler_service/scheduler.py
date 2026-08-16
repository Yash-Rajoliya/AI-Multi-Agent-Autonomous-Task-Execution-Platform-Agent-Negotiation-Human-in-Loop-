import asyncio
from datetime import datetime, timezone
from typing import Callable, Dict

from infrastructure.observability.logging import get_logger
from infrastructure.redis.redis_client import get_redis_client

from .scheduler_config import config

logger = get_logger(__name__)


class ScheduledJob:
    def __init__(self, name: str, interval: int, handler: Callable):
        self.name = name
        self.interval = interval
        self.handler = handler
        self.last_run = None
        self.is_running = False


class Scheduler:
    def __init__(self):
        self.jobs: Dict[str, ScheduledJob] = {}
        self.redis = get_redis_client()

    def register_job(self, name: str, interval: int, handler: Callable):
        self.jobs[name] = ScheduledJob(name, interval, handler)
        logger.info("Job registered", job=name, interval=interval)

    async def start(self):
        logger.info("Scheduler started")

        while True:
            now = datetime.now(timezone.utc)

            for job in self.jobs.values():
                if self._should_run(job, now):
                    asyncio.create_task(self._execute_job(job, now))

            await asyncio.sleep(config.tick_interval)

    def _should_run(self, job: ScheduledJob, now: datetime) -> bool:
        if job.is_running:
            return False

        if not job.last_run:
            return True

        return (now - job.last_run).total_seconds() >= job.interval

    async def _execute_job(self, job: ScheduledJob, scheduled_time: datetime):
        lock_key = f"{config.lock_key_prefix}:{job.name}"
        job.is_running = True
        job.last_run = scheduled_time

        if config.enable_distributed_lock:
            acquired = await self.redis.setnx(lock_key, "1")
            if not acquired:
                logger.info("Skipping job due to lock", job=job.name)
                job.is_running = False
                return

            await self.redis.expire(lock_key, job.interval)

        try:
            logger.info("Executing job", job=job.name)
            await self._run_with_retry(job)

        except Exception as e:
            logger.exception("Job execution failed after retries", job=job.name, error=str(e))
            if config.enable_distributed_lock:
                await self.redis.delete(lock_key)

        finally:
            job.is_running = False

    async def _run_with_retry(self, job: ScheduledJob):
        attempt = 1

        while attempt <= config.retry_attempts:
            try:
                await job.handler()
                return

            except Exception as e:
                if attempt >= config.retry_attempts:
                    raise e

                delay = config.retry_backoff ** (attempt - 1)

                logger.warning(
                    "Retrying job failure",
                    job=job.name,
                    attempt=attempt,
                    delay=delay,
                    error=str(e),
                )

                await asyncio.sleep(delay)
                attempt += 1