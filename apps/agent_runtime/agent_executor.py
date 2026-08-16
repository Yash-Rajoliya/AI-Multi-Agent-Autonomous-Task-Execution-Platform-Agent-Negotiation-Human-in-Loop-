import logging
from typing import Dict, Any

from sandbox import Sandbox
from capability_loader import CapabilityLoader

logger = logging.getLogger(__name__)


class AgentExecutor:
    def __init__(self, loader: CapabilityLoader, sandbox: Sandbox):
        self.loader = loader
        self.sandbox = sandbox

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        capability_name = task.get("capability")
        payload = task.get("input", {})

        logger.info(f"Executing task with capability: {capability_name}")

        func = self.loader.get(capability_name)

        result = await self.sandbox.run(func, payload)

        return {
            "status": "success",
            "capability": capability_name,
            "output": result,
        }