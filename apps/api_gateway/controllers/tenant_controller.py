from datetime import UTC, datetime
from uuid import uuid4

from apps.api_gateway.schemas.response_schema import (
    APIResponse,
)


class TenantController:
    """Controller for tenant management."""

    async def create_tenant(
        self,
        payload: dict,
    ) -> APIResponse:
        tenant_data = {
            "tenant_id": str(uuid4()),
            "name": payload.get("name"),
            "status": "active",
            "created_at": datetime.now(UTC),
        }

        return APIResponse(
            status="success",
            data=tenant_data,
            error=None,
        )

    async def get_tenant(
        self,
        tenant_id: str,
    ) -> APIResponse:
        tenant_data = {
            "tenant_id": tenant_id,
            "status": "active",
        }

        return APIResponse(
            status="success",
            data=tenant_data,
            error=None,
        )