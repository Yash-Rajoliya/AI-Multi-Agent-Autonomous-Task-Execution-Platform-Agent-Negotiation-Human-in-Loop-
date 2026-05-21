from fastapi import APIRouter, Request
from ...controllers.approval_controller import ApprovalController
from ...middleware.rbac import RBAC

router = APIRouter()
controller = ApprovalController()


@router.post("/{approval_id}/approve")
async def approve(request: Request, approval_id: str):
    RBAC.enforce(request, "reviewer")
    return await controller.approve(approval_id, request.state.user)


@router.post("/{approval_id}/reject")
async def reject(request: Request, approval_id: str):
    RBAC.enforce(request, "reviewer")
    return await controller.reject(approval_id, request.state.user)