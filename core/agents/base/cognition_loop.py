from typing import Dict, Any

from infrastructure.observability.logging import get_logger

logger = get_logger(__name__)


class CognitionLoop:
    def __init__(self, agent):
        self.agent = agent

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Cognition loop started", agent=self.agent.name)

        plan = await self.agent.plan(input_data)
        result = await self.agent.act(plan)
        reflection = await self.agent.reflect(result)

        return {
            "plan": plan,
            "result": result,
            "reflection": reflection,
        }