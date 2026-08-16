import asyncio
import logging
from typing import Any, Dict, List

from agent_executor import AgentExecutor
from capability_loader import CapabilityLoader
from runtime_config import get_config
from sandbox import Sandbox

logger = logging.getLogger(__name__)


class AgentRuntime:
    def __init__(self):
        self.config = get_config()
        self.loader = CapabilityLoader()
        self.sandbox = Sandbox(
            timeout=self.config.TOOL_TIMEOUT,
            max_workers=self.config.SANDBOX_MAX_WORKERS,
        )

        self.executor = AgentExecutor(
            loader=self.loader,
            sandbox=self.sandbox,
        )

        self._semaphore = asyncio.Semaphore(self.config.MAX_CONCURRENT_AGENTS)

    async def initialize(self):
        logger.info("Initializing Agent Runtime...")

        # Register built-in capabilities
        self.loader.register(
            "echo",
            "core.tools.api_tools.api_client.echo_tool",
        )

    async def run_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        async with self._semaphore:
            try:
                return await asyncio.wait_for(
                    self.executor.execute(task),
                    timeout=self.config.EXECUTION_TIMEOUT,
                )
            except asyncio.TimeoutError:
                logger.error("Overall task runtime execution timed out")
                return {
                    "status": "error",
                    "error": "Task exceeded max runtime execution timeout",
                }
            except Exception as e:
                logger.exception("Task execution failed unexpectedly")
                return {
                    "status": "error",
                    "error": str(e),
                }

    async def run_batch(self, tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return await asyncio.gather(
            *[self.run_task(t) for t in tasks], return_exceptions=False
        )

    async def shutdown(self):
        logger.info("Shutting down Agent Runtime sandbox resources...")
        self.sandbox.shutdown()