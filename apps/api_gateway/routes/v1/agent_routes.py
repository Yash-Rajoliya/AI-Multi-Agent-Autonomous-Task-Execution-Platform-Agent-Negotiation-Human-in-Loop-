from fastapi import APIRouter, Request
from ...controllers.agent_controller import AgentController
from ...schemas.agent_schema import AgentCreateRequest
from ...middleware.rbac import RBAC

router = APIRouter()
controller = AgentController()


@router.post("/")
async def create_agent(request: Request, payload: AgentCreateRequest):
    RBAC.enforce(request, "admin")
    return await controller.create_agent(payload, request.state.user)


@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    return await controller.get_agent(agent_id)