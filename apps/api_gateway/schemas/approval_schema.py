from datetime import datetime

from pydantic import BaseModel


class ApprovalActionResponse(BaseModel):
    """Approval workflow response schema."""

    approval_id: str
    status: str
    reviewed_by: str
    reviewed_at: datetime