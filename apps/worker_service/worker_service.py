import asyncio
from typing import Dict, Any, Callable, Awaitable
from infrastructure.observability.logging import get_logger

from .worker_config import config
from .dead_letter_queue import DeadLetterQueue

logger = get_logger(__name__)


class WorkerService:
    def __init__(self, task_processor: Callable[[Dict[str, Any]], Awaitable[None]]):
        self.processor = task_processor
        self.dlq = DeadLetterQueue(config.dlq_name) if config.enable_dlq else None

    async def process_task(self, task: Dict[str, Any]):
        task_id = task.get("id", "unknown")
        attempts = 0

        while attempts < config.max_retries:
            try:
                attempts += 1
                logger.info(
                    "Processing task attempt",
                    task_id=task_id,
                    attempt=attempts,
                    max_retries=config.max_retries,
                )
                await self.processor(task)
                logger.info("Task completed successfully", task_id=task_id)
                return
            except Exception as e:
                logger.warning(
                    "Task processing failed",
                    task_id=task_id,
                    attempt=attempts,
                    error=str(e),
                )
                if attempts < config.max_retries:
                    backoff = config.retry_backoff_seconds * (2 ** (attempts - 1))
                    await asyncio.sleep(backoff)
                else:
                    logger.error("Task exceeded max retries", task_id=task_id)
                    if self.dlq:
                        await self.dlq.send_to_dlq(task, reason=str(e))
                    else:
                        raise e