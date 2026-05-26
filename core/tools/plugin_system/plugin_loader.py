import importlib
from .plugin_manifest import PluginManifest
from .plugin_registry import PluginRegistry


class PluginLoader:
    def __init__(self, registry: PluginRegistry):
        self.registry = registry

    def load_manifest(self, manifest_dict: dict):
        manifest = PluginManifest(**manifest_dict)

        self.registry.register_plugin(manifest.name, manifest.dict())

        for tool in manifest.tools:
            module_name, func_name = tool.entrypoint.split(":")
            module = importlib.import_module(module_name)
            func = getattr(module, func_name)

            self.registry.register_tool(
                tool.name,
                func,
                metadata={
                    "description": tool.description,
                    "input_schema": tool.input_schema
                }
            )