from typing import Dict

from core.agents.base.base_agent import BaseAgent
from .data_processor import DataProcessor
from .source_ranker import SourceRanker


class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__("researcher")
        self.processor = DataProcessor()
        self.ranker = SourceRanker()

    async def plan(self, input_data: Dict):
        return {"query": input_data.get("query")}

    async def act(self, plan: Dict):
        raw_data = ["Source A", "Source B"]
        processed = self.processor.process(raw_data)
        ranked = self.ranker.rank(processed)

        return {"data": ranked}

    async def reflect(self, result: Dict):
        return {"quality": "good"}