from typing import Dict


class PlanningStrategy:
    async def create_plan(self, input_data: Dict) -> Dict:
        return {
            "steps": ["analyze", "research", "execute"]
        }