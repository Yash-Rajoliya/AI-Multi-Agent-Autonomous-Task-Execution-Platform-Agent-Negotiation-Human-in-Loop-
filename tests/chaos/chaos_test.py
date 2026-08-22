import asyncio
import random


class ChaosMonkey:
    def __init__(self, services: list):
        self.services = services

    async def inject_failure(self):
        service = random.choice(self.services)
        print(f"[CHAOS] Killing service: {service}")
        await asyncio.sleep(1)

    async def run(self, iterations: int = 5):
        for _ in range(iterations):
            await self.inject_failure()


async def test_chaos():
    monkey = ChaosMonkey(
        services=["api", "worker", "orchestrator", "redis"]
    )

    await monkey.run()