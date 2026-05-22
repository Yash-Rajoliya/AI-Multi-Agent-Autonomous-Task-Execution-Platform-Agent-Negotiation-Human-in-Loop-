from datetime import UTC, datetime

from apps.api_gateway.schemas.approval_schema import (
    ApprovalActionResponse,
)


class ApprovalService:
    """Service layer for approval workflows."""

    async def approve(
        self,
        approval_id: str,
        user: dict,
    ) -> ApprovalActionResponse:
        return ApprovalActionResponse(
            approval_id=approval_id,
            status="approved",
            reviewed_by=user["sub"],
            reviewed_at=datetime.now(UTC),
        )

    async def reject(
        self,
        approval_id: str,
        user: dict,
    ) -> ApprovalActionResponse:
        return ApprovalActionResponse(
            approval_id=approval_id,
            status="rejected",
            reviewed_by=user["sub"],
            reviewed_at=datetime.now(UTC),
        )


class ApprovalController:
    """Controller for approval operations."""

    def __init__(self) -> None:
        self.service = ApprovalService()

    async def approve(
        self,
        approval_id: str,
        user: dict,
    ) -> ApprovalActionResponse:
        return await self.service.approve(
            approval_id,
            user,
        )

    async def reject(
        self,
        approval_id: str,
        user: dict,
    ) -> ApprovalActionResponse:
        return await self.service.reject(
            approval_id,
            user,
        )