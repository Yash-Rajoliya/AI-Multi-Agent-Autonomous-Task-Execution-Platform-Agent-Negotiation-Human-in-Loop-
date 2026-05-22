from pydantic import BaseModel


class WorkflowCreateRequest(BaseModel):
    name: str
    steps: list[dict]