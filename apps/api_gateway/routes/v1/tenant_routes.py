from fastapi import APIRouter, Request
from ...controllers.tenant_controller import TenantController
from ...middleware.rbac import RBAC

router = APIRouter()
controller = TenantController()


@router.post("/")
async def create_tenant(request: Request, payload: dict):
    RBAC.enforce(request, "super_admin")
    return await controller.create_tenant(payload)


@router.get("/{tenant_id}")
async def get_tenant(tenant_id: str):
    return await controller.get_tenant(tenant_id)