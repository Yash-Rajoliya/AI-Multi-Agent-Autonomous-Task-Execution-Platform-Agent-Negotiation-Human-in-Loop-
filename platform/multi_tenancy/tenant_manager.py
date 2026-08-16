from typing import Dict, Optional
from uuid import uuid4
from infrastructure.redis import RedisClient


class Tenant:
    def __init__(self, name: str):
        self.id = str(uuid4())
        self.name = name


class TenantManager:
    def __init__(self, redis: RedisClient):
        self.redis = redis

    async def create_tenant(self, name: str) -> Tenant:
        tenant = Tenant(name)
        await self.redis.set(f"tenant:{tenant.id}", tenant.name)
        return tenant

    async def get_tenant(self, tenant_id: str) -> Optional[Dict]:
        name = await self.redis.get(f"tenant:{tenant_id}")
        if not name:
            return None
        return {"id": tenant_id, "name": name}

    async def delete_tenant(self, tenant_id: str):
        await self.redis.set(f"tenant:{tenant_id}", "")