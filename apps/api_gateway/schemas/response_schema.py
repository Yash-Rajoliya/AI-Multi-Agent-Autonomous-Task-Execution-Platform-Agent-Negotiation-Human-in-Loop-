from pydantic import BaseModel
from typing import Any, Optional


class APIResponse(BaseModel):
    status: str
    data: Optional[Any]
    error: Optional[dict]