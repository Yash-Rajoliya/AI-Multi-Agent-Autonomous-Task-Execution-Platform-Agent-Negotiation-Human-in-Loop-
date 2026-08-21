from typing import Dict


class EventParser:
    @staticmethod
    def parse(payload: Dict):
        if "event_type" not in payload:
            raise ValueError("Invalid webhook payload")

        return {
            "type": payload["event_type"],
            "data": payload.get("data", {})
        }