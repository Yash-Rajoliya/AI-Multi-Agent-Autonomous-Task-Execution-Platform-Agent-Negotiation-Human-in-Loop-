from typing import Dict, Any

from .agent_protocol import AgentProtocol
from .cognition_loop import CognitionLoop


class BaseAgent(AgentProtocol):
    def __init__(self, name: str, memory=None, tools=None):
        self.name = name
        self.memory = memory
        self.tools = tools
        self.loop = CognitionLoop(self)

    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return await self.loop.run(input_data)

    async def plan(self, input_data: Dict[str, Any]):
        raise NotImplementedError

    async def act(self, plan: Dict[str, Any]):
        raise NotImplementedError

    async def reflect(self, result: Dict[str, Any]):
        raise NotImplementedError