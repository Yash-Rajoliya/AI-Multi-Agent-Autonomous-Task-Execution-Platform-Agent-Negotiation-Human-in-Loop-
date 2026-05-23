from typing import Dict


class PlanValidator:
    def validate(self, plan: Dict) -> bool:
        return "steps" in plan and len(plan["steps"]) > 0