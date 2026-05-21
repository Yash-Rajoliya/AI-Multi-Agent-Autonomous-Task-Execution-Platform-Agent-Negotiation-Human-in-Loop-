from infrastructure.messaging.message_bus import KafkaBus
from infrastructure.messaging.event_schema import BaseEvent, EventMetadata


class TaskController:
    def __init__(self, bus: KafkaBus):
        self.bus = bus

    async def create_task(self, request):
        event = BaseEvent(
            metadata=EventMetadata(
                event_type="task.created",
                source="api-gateway",
                trace_id=request.headers.get("x-trace-id", "generated"),
            ),
            payload=request.dict(),
        )

        await self.bus.publish("tasks.created.v1", event)

        return {"status": "accepted"}