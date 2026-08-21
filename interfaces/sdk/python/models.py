from pydantic import BaseModel


class Task(BaseModel):
    id: str
    status: str
    payload: dict


class WorkflowResponse(BaseModel):
    workflow_id: str
    status: str
    result: dict