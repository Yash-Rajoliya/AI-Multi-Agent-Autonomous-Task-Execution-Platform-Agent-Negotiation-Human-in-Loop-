from typing import Dict


class ActionHandler:
    async def handle(self, action: Dict):
        return {"executed": action}