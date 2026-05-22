from datetime import datetime

from pydantic import BaseModel, Field


class WorkflowStep(BaseModel):
    """Workflow step definition."""

    step_name: str
    agent_type: str
    config: dict = Field(default_factory=dict)


class WorkflowCreateRequest(BaseModel):
    """Workflow creation request schema."""

    name: str = Field(
        ...,
        min_length=3,
        max_length=200,
    )

    steps: list[WorkflowStep]


class WorkflowResponse(BaseModel):
    """Workflow response schema."""

    workflow_id: str
    name: str
    steps: list[WorkflowStep]
    status: str
    created_by: str
    created_at: datetime