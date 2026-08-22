import asyncio
import time
import httpx


async def send_request():
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://localhost:8000/v1/tasks",
            json={"task": "load_test", "agent_type": "executor"}
        )


async def run_load_test(concurrency: int = 50, duration: int = 10):
    start = time.time()
    tasks = []

    while time.time() - start < duration:
        tasks.append(asyncio.create_task(send_request()))
        if len(tasks) >= concurrency:
            await asyncio.gather(*tasks)
            tasks = []

    print("Load test completed")


if __name__ == "__main__":
    asyncio.run(run_load_test())