from infrastructure.redis import RedisClient


class QuotaExceededException(Exception):
    pass


class QuotaManager:
    def __init__(self, redis: RedisClient):
        self.redis = redis

    async def set_quota(self, tenant_id: str, limit: int):
        await self.redis.set(f"quota:{tenant_id}", str(limit))

    async def check_quota(self, tenant_id: str):
        limit = await self.redis.get(f"quota:{tenant_id}")
        usage = await self.redis.get(f"usage:{tenant_id}") or "0"

        if int(usage) >= int(limit):
            raise QuotaExceededException("Quota exceeded")

        await self.redis.set(f"usage:{tenant_id}", str(int(usage) + 1))