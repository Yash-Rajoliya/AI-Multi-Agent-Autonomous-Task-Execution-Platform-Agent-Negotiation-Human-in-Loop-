import asyncio
import signal

from infrastructure.observability.logging import setup_logging, get_logger

from .scheduler import Scheduler
from .jobs.cleanup_jobs import cleanup_memory, cleanup_logs
from .jobs.retry_jobs import retry_failed_tasks
from .jobs.monitoring_jobs import system_health_check, metrics_snapshot

logger = get_logger(__name__)


async def main():
    setup_logging()

    scheduler = Scheduler()

    # Register jobs
    scheduler.register_job("cleanup_memory", 60, cleanup_memory)
    scheduler.register_job("cleanup_logs", 300, cleanup_logs)
    scheduler.register_job("retry_failed_tasks", 120, retry_failed_tasks)
    scheduler.register_job("system_health_check", 30, system_health_check)
    scheduler.register_job("metrics_snapshot", 45, metrics_snapshot)

    stop_event = asyncio.Event()

    def shutdown():
        logger.info("Shutdown signal received")
        stop_event.set()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    scheduler_task = asyncio.create_task(scheduler.start())

    await stop_event.wait()

    scheduler_task.cancel()
    logger.info("Scheduler stopped")


if __name__ == "__main__":
    asyncio.run(main())