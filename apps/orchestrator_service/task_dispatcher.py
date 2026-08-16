import asyncio
import logging
from typing import Any

logger = logging.getLogger(__name__)


class TaskDispatcher:
    async def dispatch(self, node) -> Any:
        logger.info(f"Dispatching node: {node.id}")

        # Simulate routing logic
        if node.type == "agent":
            return await self._run_agent(node)
        elif node.type == "tool":
            return await self._run_tool(node)
        else:
            raise ValueError(f"Unknown node type: {node.type}")

    async def _run_agent(self, node):
        await asyncio.sleep(0.2)
        return {"status": "success", "output": f"Agent executed {node.id}"}

    async def _run_tool(self, node):
        await asyncio.sleep(0.1)
        return {"status": "success", "output": f"Tool executed {node.id}"}