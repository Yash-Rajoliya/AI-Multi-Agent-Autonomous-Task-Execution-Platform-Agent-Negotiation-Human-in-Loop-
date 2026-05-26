from typing import Dict
from core.tools.tool_registry import ToolRegistry


class PluginRegistry:
    def __init__(self):
        self.plugins: Dict[str, dict] = {}
        self.tool_registry = ToolRegistry()

    def register_plugin(self, name: str, manifest: dict):
        self.plugins[name] = manifest

    def register_tool(self, name: str, func, metadata=None):
        self.tool_registry.register(name, func, metadata)

    def get_tool(self, name: str):
        return self.tool_registry.get(name)

    def list_plugins(self):
        return list(self.plugins.keys())