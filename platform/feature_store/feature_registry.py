from typing import Dict, Callable


class FeatureRegistry:
    def __init__(self):
        self._features: Dict[str, Callable] = {}

    def register(self, name: str, fn: Callable):
        self._features[name] = fn

    def get(self, name: str):
        return self._features.get(name)

    def list_features(self):
        return list(self._features.keys())