import asyncio
from typing import Callable, Awaitable

from infrastructure.observability.logging import get_logger
from .worker_config import config

logger = get_logger(__name__)


class RetryManager:
    def __init__(self):
        self.max_retries = config.max_retries

    async def execute_with_retry(
        self,
        task_id: str,
        func: Callable[[], Awaitable[None]],
        attempt: int = 1,
    ):
        try:
            await func()

        except Exception as e:
            if attempt >= self.max_retries:
                logger.error(
                    "Max retries reached",
                    task_id=task_id,
                    attempts=attempt,
                )
                raise

            delay = config.retry_backoff_base ** attempt
            logger.warning(
                "Retrying task",
                task_id=task_id,
                attempt=attempt,
                delay=delay,
            )

            await asyncio.sleep(delay)
            await self.execute_with_retry(task_id, func, attempt + 1)