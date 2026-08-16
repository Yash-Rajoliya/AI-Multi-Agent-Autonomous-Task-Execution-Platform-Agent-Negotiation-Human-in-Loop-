import asyncio
import logging
from typing import Callable, Any

logger = logging.getLogger(__name__)


class SandboxExecutionError(Exception):
    pass


class Sandbox:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    async def run(self, func: Callable, *args, **kwargs) -> Any:
        try:
            return await asyncio.wait_for(
                self._safe_execute(func, *args, **kwargs),
                timeout=self.timeout,
            )
        except asyncio.TimeoutError:
            raise SandboxExecutionError("Execution timed out")
        except Exception as e:
            logger.exception("Sandbox error")
            raise SandboxExecutionError(str(e))

    async def _safe_execute(self, func, *args, **kwargs):
        # Can extend with process isolation / container exec
        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)