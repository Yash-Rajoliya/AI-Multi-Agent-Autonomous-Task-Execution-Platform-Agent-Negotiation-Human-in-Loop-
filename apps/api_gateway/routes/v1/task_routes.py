from fastapi import APIRouter, Depends, Request

from ...controllers.task_controller import TaskController
from ...schemas.task_schema import TaskCreateRequest
from ...middleware.rbac import RBAC

router = APIRouter()
controller = TaskController()


@router.post("/")
async def create_task(request: Request, payload: TaskCreateRequest):
    RBAC.enforce(request, "user")
    return await controller.create_task(payload, request.state.user)


@router.get("/{task_id}")
async def get_task(task_id: str):
    return await controller.get_task(task_id)