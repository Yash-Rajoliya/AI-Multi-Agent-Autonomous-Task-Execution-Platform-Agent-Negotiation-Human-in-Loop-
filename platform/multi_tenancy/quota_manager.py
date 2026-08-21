from infrastructure.redis import RedisClient


class QuotaExceededException(Exception):
    pass


class QuotaManager:
    def __init__(self, redis: RedisClient, default_limit: int = 1000):
        self.redis = redis
        self.default_limit = default_limit

    async def set_quota(self, tenant_id: str, limit: int):
        await self.redis.set(f"quota:{tenant_id}", str(limit))

    async def check_quota(self, tenant_id: str):
        limit_val = await self.redis.get(f"quota:{tenant_id}")
        limit = int(limit_val) if limit_val is not None else self.default_limit

        usage_val = await self.redis.get(f"usage:{tenant_id}") or "0"
        usage = int(usage_val)

        if usage >= limit:
            raise QuotaExceededException(f"Quota exceeded for tenant {tenant_id}: {usage}/{limit}")

        await self.redis.set(f"usage:{tenant_id}", str(usage + 1))