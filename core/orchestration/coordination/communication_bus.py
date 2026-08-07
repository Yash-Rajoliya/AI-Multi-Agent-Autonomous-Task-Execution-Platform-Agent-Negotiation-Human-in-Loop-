import asyncio


class CommunicationBus:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def publish(self, message):
        await self.queue.put(message)

    async def subscribe(self):
        while True:
            msg = await self.queue.get()
            yield msg