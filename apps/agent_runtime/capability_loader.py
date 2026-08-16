import importlib
import logging
from typing import Dict, Callable

logger = logging.getLogger(__name__)


class CapabilityLoader:
    def __init__(self):
        self._registry: Dict[str, Callable] = {}

    def register(self, name: str, path: str):
        module_path, func_name = path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)

        self._registry[name] = func
        logger.info(f"Loaded capability: {name}")

    def get(self, name: str) -> Callable:
        if name not in self._registry:
            raise ValueError(f"Capability not found: {name}")
        return self._registry[name]

    def list_capabilities(self):
        return list(self._registry.keys())