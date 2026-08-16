import asyncio
import concurrent.futures
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class SandboxExecutionError(Exception):
    pass


class SandboxTimeoutError(SandboxExecutionError):
    pass


class Sandbox:
    def __init__(self, timeout: int = 10, max_workers: int = 4):
        self.timeout = timeout
        self.executor = concurrent.futures.ProcessPoolExecutor(
            max_workers=max_workers
        )

    async def run(self, func: Callable, *args, **kwargs) -> Any:
        loop = asyncio.get_running_loop()
        try:
            if asyncio.iscoroutinefunction(func):
                return await asyncio.wait_for(
                    func(*args, **kwargs),
                    timeout=self.timeout,
                )
            
            # Offload synchronous/blocking capabilities to a isolated process executor
            return await asyncio.wait_for(
                loop.run_in_executor(self.executor, func, *args, **kwargs),
                timeout=self.timeout,
            )
        except asyncio.TimeoutError:
            logger.error(f"Sandbox execution timed out after {self.timeout}s")
            raise SandboxTimeoutError(f"Execution timed out after {self.timeout}s")
        except Exception as e:
            logger.exception("Sandbox execution error")
            raise SandboxExecutionError(f"Execution failed: {str(e)}")

    def shutdown(self):
        self.executor.shutdown(wait=False, cancel_futures=True)