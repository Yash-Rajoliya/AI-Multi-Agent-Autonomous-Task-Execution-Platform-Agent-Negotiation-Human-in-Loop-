from infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


async def retry_failed_tasks():
    logger.info("Retrying failed tasks from DLQ")
    # TODO: integrate with worker DLQ and requeue messages