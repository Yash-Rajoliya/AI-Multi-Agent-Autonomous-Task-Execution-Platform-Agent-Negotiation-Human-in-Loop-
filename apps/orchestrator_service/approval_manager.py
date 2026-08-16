import asyncio
import logging

logger = logging.getLogger(__name__)


class ApprovalManager:
    async def requires_approval(self, node) -> bool:
        # Example logic
        return node.type == "agent"

    async def wait_for_approval(self, node) -> bool:
        logger.info(f"Waiting approval for node {node.id}")

        # Simulated human approval
        await asyncio.sleep(0.5)

        return True