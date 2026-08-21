import httpx
from .models import Task, WorkflowResponse


class AIClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    async def create_task(self, payload: dict) -> Task:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{self.base_url}/v1/tasks",
                json=payload,
                headers=self.headers
            )
            return Task(**res.json())

    async def run_workflow(self, payload: dict) -> WorkflowResponse:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"{self.base_url}/v1/workflows/run",
                json=payload,
                headers=self.headers
            )
            return WorkflowResponse(**res.json())