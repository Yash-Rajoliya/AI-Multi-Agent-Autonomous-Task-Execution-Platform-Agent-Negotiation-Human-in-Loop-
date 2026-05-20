from infrastructure.messaging import MessageBus


class TaskPublisher:
    def __init__(self, bus: MessageBus):
        self.bus = bus

    async def publish_task(self, payload: dict):
        await self.bus.publish("tasks", payload)