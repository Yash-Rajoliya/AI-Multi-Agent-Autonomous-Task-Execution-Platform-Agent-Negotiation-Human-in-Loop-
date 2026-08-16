import asyncio
import logging
from typing import Dict, Any

from agent_executor import AgentExecutor
from capability_loader import CapabilityLoader
from sandbox import Sandbox
from runtime_config import get_config

logger = logging.getLogger(__name__)


class AgentRuntime:
    def __init__(self):
        self.config = get_config()
        self.loader = CapabilityLoader()
        self.sandbox = Sandbox(timeout=self.config.TOOL_TIMEOUT)

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
            "core.tools.api_tools.api_client.echo_tool"
        )

    async def run_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        async with self._semaphore:
            try:
                return await self.executor.execute(task)
            except Exception as e:
                logger.exception("Task execution failed")
                return {
                    "status": "error",
                    "error": str(e),
                }

    async def run_batch(self, tasks):
        return await asyncio.gather(*[self.run_task(t) for t in tasks])