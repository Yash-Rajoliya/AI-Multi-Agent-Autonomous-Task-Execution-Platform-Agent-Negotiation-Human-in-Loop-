from infrastructure.messaging import MessageBus


class TaskConsumer:
    def __init__(self, bus: MessageBus):
        self.bus = bus

    async def listen(self):
        async for topic, msg in self.bus.consume():
            if topic == "tasks":
                print("Processing task:", msg)