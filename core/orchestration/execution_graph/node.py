from typing import Callable, Any


class Node:
    def __init__(self, node_id: str, func: Callable[..., Any]):
        self.id = node_id
        self.func = func
        self.status = "pending"
        self.result = None

    async def execute(self, context: dict):
        self.status = "running"
        try:
            self.result = await self.func(context)
            self.status = "completed"
        except Exception as e:
            self.status = "failed"
            raise e