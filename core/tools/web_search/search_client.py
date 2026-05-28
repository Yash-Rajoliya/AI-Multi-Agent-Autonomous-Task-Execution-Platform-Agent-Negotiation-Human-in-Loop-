import httpx
import os


class SearchClient:
    def __init__(self):
        self.api_key = os.getenv("SEARCH_API_KEY")
        self.endpoint = "https://api.tavily.com/search"

    async def search(self, query: str):
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(
                self.endpoint,
                json={
                    "api_key": self.api_key,
                    "query": query
                }
            )
            response.raise_for_status()
            return response.json()