import logging
from typing import Any, Dict

from capability_loader import CapabilityLoader
from sandbox import Sandbox, SandboxExecutionError

logger = logging.getLogger(__name__)


class AgentExecutor:
    def __init__(self, loader: CapabilityLoader, sandbox: Sandbox):
        self.loader = loader
        self.sandbox = sandbox

    async def execute(self, task: Dict[str, Any]) -> Dict[str, Any]:
        capability_name = task.get("capability")
        payload = task.get("input", {})

        if not capability_name:
            raise ValueError("Task missing required 'capability' field.")

        logger.info(f"Executing task with capability: {capability_name}")

        func = self.loader.get(capability_name)

        try:
            result = await self.sandbox.run(func, payload)
            return {
                "status": "success",
                "capability": capability_name,
                "output": result,
            }
        except SandboxExecutionError as e:
            logger.error(f"Execution failed in sandbox for {capability_name}: {str(e)}")
            return {
                "status": "error",
                "capability": capability_name,
                "error": str(e),
            }