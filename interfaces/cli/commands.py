import httpx
from .cli_config import CLIConfig
from .display import Display


class Commands:
    def __init__(self):
        self.base_url = CLIConfig.API_URL

    async def create_task(self, payload: dict):
        async with httpx.AsyncClient(timeout=CLIConfig.TIMEOUT) as client:
            res = await client.post(f"{self.base_url}/v1/tasks", json=payload)
            Display.print_json(res.json())

    async def list_agents(self):
        async with httpx.AsyncClient(timeout=CLIConfig.TIMEOUT) as client:
            res = await client.get(f"{self.base_url}/v1/agents")
            Display.print_json(res.json())

    async def run_workflow(self, payload: dict):
        async with httpx.AsyncClient(timeout=CLIConfig.TIMEOUT) as client:
            res = await client.post(f"{self.base_url}/v1/workflows/run", json=payload)
            Display.print_json(res.json())