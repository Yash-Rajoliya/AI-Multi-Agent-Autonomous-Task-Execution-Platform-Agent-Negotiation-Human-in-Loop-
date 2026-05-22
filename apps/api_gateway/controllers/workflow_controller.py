from datetime import UTC, datetime
from uuid import uuid4

from apps.api_gateway.schemas.workflow_schema import (
    WorkflowCreateRequest,
    WorkflowResponse,
)


class WorkflowService:
    """Service layer for workflow management."""

    async def create(
        self,
        payload: WorkflowCreateRequest,
        user: dict,
    ) -> WorkflowResponse:
        return WorkflowResponse(
            workflow_id=str(uuid4()),
            name=payload.name,
            steps=payload.steps,
            status="created",
            created_by=user["sub"],
            created_at=datetime.now(UTC),
        )

    async def get(
        self,
        workflow_id: str,
    ) -> WorkflowResponse:
        return WorkflowResponse(
            workflow_id=workflow_id,
            name="research-workflow",
            steps=[],
            status="running",
            created_by="system",
            created_at=datetime.now(UTC),
        )


class WorkflowController:
    """Controller for workflow APIs."""

    def __init__(self) -> None:
        self.service = WorkflowService()

    async def create_workflow(
        self,
        payload: WorkflowCreateRequest,
        user: dict,
    ) -> WorkflowResponse:
        return await self.service.create(
            payload,
            user,
        )

    async def get_workflow(
        self,
        workflow_id: str,
    ) -> WorkflowResponse:
        return await self.service.get(workflow_id)