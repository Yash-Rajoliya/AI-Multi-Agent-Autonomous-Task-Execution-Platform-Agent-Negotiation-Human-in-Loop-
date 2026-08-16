import asyncio
from typing import Dict

from infrastructure.observability.logging import get_logger
from infrastructure.observability.metrics import increment_counter

from apps.agent-runtime.agent_executor import AgentExecutor

from .queue_consumer import QueueConsumer
from .retry_manager import RetryManager
from .dead_letter_queue import DeadLetterQueue
from .worker_config import config

logger = get_logger(__name__)


class Worker:
    def __init__(self):
        self.consumer = QueueConsumer(config.queue_name)
        self.retry_manager = RetryManager()
        self.dlq = DeadLetterQueue()
        self.executor = AgentExecutor()

        self._processed_tasks = set()  # naive idempotency (replace with Redis in prod)

    async def start(self):
        logger.info("Worker started", concurrency=config.concurrency)

        tasks = [
            asyncio.create_task(self.consumer.consume(self._handle_message))
            for _ in range(config.concurrency)
        ]

        await asyncio.gather(*tasks)

    async def _handle_message(self, message: Dict):
        task_id = message.get("task_id")

        if config.enable_idempotency and task_id in self._processed_tasks:
            logger.warning("Duplicate task skipped", task_id=task_id)
            return

        async def process():
            logger.info("Processing task", task_id=task_id)

            await self.executor.execute(message)

            increment_counter("worker_tasks_success")

            if config.enable_idempotency:
                self._processed_tasks.add(task_id)

        try:
            await self.retry_manager.execute_with_retry(task_id, process)

        except Exception as e:
            increment_counter("worker_tasks_failed")

            await self.dlq.push(message, str(e))