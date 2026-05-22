 from datetime import UTC, datetime
from uuid import uuid4

from apps.api_gateway.schemas.agent_schema import (
    AgentCreateRequest,
    AgentResponse,
)


class AgentService:
    """Service layer for agent operations."""

    async def create(
        self,
        payload: AgentCreateRequest,
        user: dict,
    ) -> AgentResponse:
        return AgentResponse(
            agent_id=str(uuid4()),
            name=payload.name,
            capabilities=payload.capabilities,
            status="active",
            created_by=user["sub"],
            created_at=datetime.now(UTC),
        )

    async def get(
        self,
        agent_id: str,
    ) -> AgentResponse:
        return AgentResponse(
            agent_id=agent_id,
            name="planner-agent",
            capabilities=["planning", "reasoning"],
            status="active",
            created_by="system",
            created_at=datetime.now(UTC),
        )


class AgentController:
    """Controller for agent APIs."""

    def __init__(self) -> None:
        self.service = AgentService()

    async def create_agent(
        self,
        payload: AgentCreateRequest,
        user: dict,
    ) -> AgentResponse:
        return await self.service.create(payload, user)

    async def get_agent(
        self,
        agent_id: str,
    ) -> AgentResponse:
        return await self.service.get(agent_id)