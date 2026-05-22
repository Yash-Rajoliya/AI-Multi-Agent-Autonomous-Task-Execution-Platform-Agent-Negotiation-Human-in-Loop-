from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Standardized API error response."""

    code: str
    message: str


class APIResponse(BaseModel):
    """Standardized API response wrapper."""

    status: str
    data: Any | None = None
    error: ErrorResponse | None = None