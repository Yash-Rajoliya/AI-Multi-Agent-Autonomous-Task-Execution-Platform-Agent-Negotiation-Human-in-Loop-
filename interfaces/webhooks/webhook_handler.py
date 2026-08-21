from typing import Callable, Dict
from .event_parser import EventParser


class WebhookHandler:
    def __init__(self):
        self.handlers: Dict[str, Callable] = {}

    def register(self, event_type: str, handler: Callable):
        self.handlers[event_type] = handler

    async def handle(self, payload: dict):
        event = EventParser.parse(payload)
        event_type = event["type"]

        if event_type not in self.handlers:
            raise ValueError(f"No handler for event: {event_type}")

        return await self.handlers[event_type](event["data"])