from pydantic import BaseModel


class AgentCreateRequest(BaseModel):
    name: str
    capabilities: list[str]