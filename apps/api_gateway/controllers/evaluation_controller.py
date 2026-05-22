from datetime import UTC, datetime
from uuid import uuid4

from apps.api_gateway.schemas.response_schema import (
    APIResponse,
)


class EvaluationController:
    """Controller for evaluation workflows."""

    async def run(
        self,
        payload: dict,
    ) -> APIResponse:
        evaluation_data = {
            "evaluation_id": str(uuid4()),
            "status": "queued",
            "submitted_at": datetime.now(UTC),
            "payload": payload,
        }

        return APIResponse(
            status="success",
            data=evaluation_data,
            error=None,
        )