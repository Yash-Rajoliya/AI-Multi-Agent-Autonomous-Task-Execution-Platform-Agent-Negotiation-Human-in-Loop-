import asyncio
import signal

from infrastructure.observability.logging import setup_logging, get_logger
from .worker import Worker

logger = get_logger(__name__)


async def main():
    setup_logging()

    worker = Worker()

    stop_event = asyncio.Event()

    def shutdown():
        logger.info("Shutdown signal received")
        stop_event.set()

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)
    loop.add_signal_handler(signal.SIGTERM, shutdown)

    worker_task = asyncio.create_task(worker.start())

    await stop_event.wait()

    worker_task.cancel()
    logger.info("Worker stopped")


if __name__ == "__main__":
    asyncio.run(main())