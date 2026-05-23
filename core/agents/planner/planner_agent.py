from typing import Dict

from core.agents.base.base_agent import BaseAgent
from .planning_strategy import PlanningStrategy
from .plan_validator import PlanValidator


class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("planner")
        self.strategy = PlanningStrategy()
        self.validator = PlanValidator()

    async def plan(self, input_data: Dict):
        plan = await self.strategy.create_plan(input_data)

        if not self.validator.validate(plan):
            raise ValueError("Invalid plan")

        return plan

    async def act(self, plan: Dict):
        return plan

    async def reflect(self, result: Dict):
        return {"status": "validated"}