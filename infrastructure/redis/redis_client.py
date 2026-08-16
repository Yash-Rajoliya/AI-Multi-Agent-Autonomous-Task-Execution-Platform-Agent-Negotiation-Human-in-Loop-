import aioredis
from infrastructure.config import get_settings


class RedisClient:
    def __init__(self):
        self.settings = get_settings()
        self._client = None

    async def connect(self):
        self._client = await aioredis.from_url(
            self.settings.REDIS_URL,
            decode_responses=True,
        )

    async def get(self, key: str):
        return await self._client.get(key)

    async def set(self, key: str, value: str):
        await self._client.set(key, value)

    async def close(self):
        await self._client.close()