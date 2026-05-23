from typing import Dict, Any


class ToolInterface:
    async def execute(self, tool_name: str, params: Dict[str, Any]) -> Any:
        raise NotImplementedError