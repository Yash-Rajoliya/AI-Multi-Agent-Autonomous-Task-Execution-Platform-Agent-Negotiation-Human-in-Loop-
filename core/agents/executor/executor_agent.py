from typing import Dict

from core.agents.base.base_agent import BaseAgent
from .action_handler import ActionHandler
from .tool_selector import ToolSelector


class ExecutorAgent(BaseAgent):
    def __init__(self):
        super().__init__("executor")
        self.handler = ActionHandler()
        self.selector = ToolSelector()

    async def plan(self, input_data: Dict):
        return {"action": input_data.get("task")}

    async def act(self, plan: Dict):
        tool = self.selector.select(plan)
        return await self.handler.handle(tool)

    async def reflect(self, result: Dict):
        return {"status": "executed"}