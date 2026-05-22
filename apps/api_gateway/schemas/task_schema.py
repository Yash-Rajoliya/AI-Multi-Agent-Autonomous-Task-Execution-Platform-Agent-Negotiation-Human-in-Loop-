from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreateRequest(BaseModel):
    """Task creation request schema."""

    task_name: str = Field(
        ...,
        min_length=3,
        max_length=200,
    )

    workflow_id: str

    payload: dict = Field(default_factory=dict)


class TaskResponse(BaseModel):
    """Task response schema."""

    task_id: str
    status: str
    created_at: datetime