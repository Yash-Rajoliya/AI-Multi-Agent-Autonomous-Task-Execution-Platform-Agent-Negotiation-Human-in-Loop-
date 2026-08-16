import json

from infrastructure.redis.redis_client import get_redis_client
from infrastructure.observability.logging import get_logger
from .worker_config import config

logger = get_logger(__name__)


class DeadLetterQueue:
    def __init__(self):
        self.redis = get_redis_client()
        self.queue_name = config.dead_letter_queue

    async def push(self, payload: dict, reason: str):
        message = {
            "payload": payload,
            "reason": reason,
        }

        await self.redis.rpush(self.queue_name, json.dumps(message))

        logger.error(
            "Message sent to DLQ",
            queue=self.queue_name,
            reason=reason,
        )