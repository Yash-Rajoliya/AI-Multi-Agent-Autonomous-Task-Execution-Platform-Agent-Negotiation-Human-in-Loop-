from typing import Dict, Any
import time


class WorkingMemory:
    """
    Short-term memory (session scoped)
    """

    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}

    def set(self, key: str, value: Any):
        self._store[key] = value
        self._timestamps[key] = time.time()

    def get(self, key: str):
        return self._store.get(key)

    def delete(self, key: str):
        self._store.pop(key, None)
        self._timestamps.pop(key, None)

    def clear(self):
        self._store.clear()
        self._timestamps.clear()

    def dump(self):
        return self._store.copy()