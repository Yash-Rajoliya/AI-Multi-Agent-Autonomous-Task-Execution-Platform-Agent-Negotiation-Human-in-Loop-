import asyncio
from datetime import datetime
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
            now = datetime.utcnow()

            for job in self.jobs.values():
                if self._should_run(job, now):
                    asyncio.create_task(self._execute_job(job))

            await asyncio.sleep(config.tick_interval)

    def _should_run(self, job: ScheduledJob, now: datetime):
        if not job.last_run:
            return True

        return (now - job.last_run).total_seconds() >= job.interval

    async def _execute_job(self, job: ScheduledJob):
        lock_key = f"{config.lock_key_prefix}:{job.name}"

        if config.enable_distributed_lock:
            acquired = await self.redis.setnx(lock_key, "1")
            if not acquired:
                logger.info("Skipping job due to lock", job=job.name)
                return

            await self.redis.expire(lock_key, job.interval)

        try:
            logger.info("Executing job", job=job.name)

            await self._run_with_retry(job)

            job.last_run = datetime.utcnow()

        except Exception as e:
            logger.exception("Job execution failed", job=job.name, error=str(e))

        finally:
            if config.enable_distributed_lock:
                await self.redis.delete(lock_key)

    async def _run_with_retry(self, job: ScheduledJob):
        attempt = 1

        while attempt <= config.retry_attempts:
            try:
                await job.handler()
                return

            except Exception as e:
                if attempt == config.retry_attempts:
                    raise

                delay = config.retry_backoff ** attempt

                logger.warning(
                    "Retrying job",
                    job=job.name,
                    attempt=attempt,
                    delay=delay,
                )

                await asyncio.sleep(delay)
                attempt += 1