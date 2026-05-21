from fastapi import APIRouter, Request
from ...controllers.workflow_controller import WorkflowController
from ...schemas.workflow_schema import WorkflowCreateRequest
from ...middleware.rbac import RBAC

router = APIRouter()
controller = WorkflowController()


@router.post("/")
async def create_workflow(request: Request, payload: WorkflowCreateRequest):
    RBAC.enforce(request, "user")
    return await controller.create_workflow(payload, request.state.user)


@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    return await controller.get_workflow(workflow_id)