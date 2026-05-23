from typing import Dict

from core.agents.base.base_agent import BaseAgent
from .evaluation_engine import EvaluationEngine


class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__("critic")
        self.engine = EvaluationEngine()

    async def plan(self, input_data: Dict):
        return input_data

    async def act(self, plan: Dict):
        return self.engine.evaluate(plan)

    async def reflect(self, result: Dict):
        return {"approved": result["score"] > 0.5}