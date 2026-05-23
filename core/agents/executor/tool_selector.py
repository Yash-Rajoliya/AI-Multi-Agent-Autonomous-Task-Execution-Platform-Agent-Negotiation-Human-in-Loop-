from typing import Dict


class ToolSelector:
    def select(self, plan: Dict):
        return {"tool": "default"}