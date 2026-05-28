import logging
import httpx

logger = logging.getLogger(__name__)


def echo_tool(payload: dict):
    return {
        "message": "Echo executed",
        "input": payload,
    }




class APIClient:
    def __init__(self, base_url: str, headers: dict = None):
        self.base_url = base_url
        self.headers = headers or {}

    async def get(self, path: str, params: dict = None):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}{path}",
                params=params,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

    async def post(self, path: str, data: dict = None):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}{path}",
                json=data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()