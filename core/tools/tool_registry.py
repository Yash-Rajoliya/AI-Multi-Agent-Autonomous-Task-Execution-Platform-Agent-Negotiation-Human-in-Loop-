from typing import Dict, Callable, Any


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._metadata: Dict[str, dict] = {}

    def register(self, name: str, func: Callable, metadata: dict = None):
        if name in self._tools:
            raise ValueError(f"Tool '{name}' already registered")

        self._tools[name] = func
        self._metadata[name] = metadata or {}

    def get(self, name: str):
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found")
        return self._tools[name]

    def list_tools(self):
        return [
            {
                "name": name,
                "metadata": self._metadata.get(name, {})
            }
            for name in self._tools
        ]

    async def execute(self, name: str, *args, **kwargs):
        tool = self.get(name)

        if callable(tool):
            result = tool(*args, **kwargs)
            if hasattr(result, "__await__"):
                return await result
            return result

        raise TypeError("Invalid tool type")