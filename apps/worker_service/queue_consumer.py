from infrastructure.messaging.message_bus import KafkaBus
from infrastructure.messaging.event_schema import BaseEvent
from .worker import Worker


class QueueConsumer:
    def __init__(self, bus: KafkaBus):
        self.bus = bus
        self.worker = Worker()

    async def handle_workflow(self, event: BaseEvent):
        workflow = event.payload["workflow"]

        result = await self.worker.execute(workflow)

        await self.bus.publish(
            "tasks.completed.v1",
            BaseEvent(
                metadata=event.metadata,
                payload={"result": result},
            ),
        )