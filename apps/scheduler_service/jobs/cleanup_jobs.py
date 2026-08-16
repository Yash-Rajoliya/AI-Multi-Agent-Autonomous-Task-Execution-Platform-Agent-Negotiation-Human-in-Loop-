from infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


async def cleanup_memory():
    logger.info("Running memory cleanup job")
    # TODO: integrate with memory-service to purge stale entries


async def cleanup_logs():
    logger.info("Running log cleanup job")
    # TODO: purge old logs from storage