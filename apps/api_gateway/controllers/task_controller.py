from uuid import uuid4

from infrastructure.messaging.message_bus import MessageBus


class TaskController:
    """Controller for task management."""

    def __init__(self) -> None:
        self.bus = MessageBus()

    async def create_task(
        self,
        request: dict,
        trace_id: str | None = None,
    ) -> dict:
        event = {
            "event_id": str(uuid4()),
            "event_type": "task.created",
            "source": "api-gateway",
            "trace_id": trace_id or "generated",
            "payload": request,
        }

        self.bus.publish(
            topic="tasks.created.v1",
            key=event["event_id"],
            value=event,
        )

        return {
            "status": "accepted",
            "event_id": event["event_id"],
        }