import asyncio
from infrastructure.messaging.message_bus import KafkaBus
from orchestration_engine import OrchestrationEngine


async def main():
    bus = KafkaBus(bootstrap_servers="localhost:9092")
    await bus.start()

    engine = OrchestrationEngine(bus)

    await bus.subscribe(
        topic="tasks.created.v1",
        group_id="orchestrator-group",
        handler=engine.handle_task_created,
    )

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())