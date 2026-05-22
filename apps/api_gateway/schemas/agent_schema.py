from datetime import datetime

from pydantic import BaseModel, Field


class AgentCreateRequest(BaseModel):
    """Request schema for creating agents."""

    name: str = Field(..., min_length=2, max_length=100)

    capabilities: list[str] = Field(
        default_factory=list,
    )


class AgentResponse(BaseModel):
    """Response schema for agent operations."""

    agent_id: str
    name: str
    capabilities: list[str]
    status: str
    created_by: str
    created_at: datetime