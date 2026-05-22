from pydantic import BaseModel


class ApprovalResponse(BaseModel):
    approval_id: str
    status: str