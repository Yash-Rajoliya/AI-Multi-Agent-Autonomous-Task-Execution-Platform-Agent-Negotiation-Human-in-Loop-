from typing import List, Dict
import uuid
import time


class EpisodicMemory:
    """
    Stores past interactions/events
    """

    def __init__(self):
        self.events: List[Dict] = []

    def add_event(self, content: str, metadata: dict = None):
        event = {
            "id": str(uuid.uuid4()),
            "timestamp": time.time(),
            "content": content,
            "metadata": metadata or {}
        }
        self.events.append(event)
        return event

    def search(self, query: str):
        # naive keyword match (can be upgraded)
        return [
            e for e in self.events
            if query.lower() in e["content"].lower()
        ]

    def get_recent(self, limit=5):
        return sorted(self.events, key=lambda x: x["timestamp"], reverse=True)[:limit]