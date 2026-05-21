from uuid import uuid4


class TenantController:

    async def create_tenant(self, payload):
        return {
            "tenant_id": str(uuid4()),
            "name": payload.get("name")
        }

    async def get_tenant(self, tenant_id):
        return {
            "tenant_id": tenant_id,
            "status": "active"
        }