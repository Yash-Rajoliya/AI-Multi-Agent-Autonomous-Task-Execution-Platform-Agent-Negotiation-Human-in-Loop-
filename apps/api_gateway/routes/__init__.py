"""
Central API route registration package.

Aggregates public and internal API route groups
for the API Gateway application.

Route Groups:
- v1: Stable public APIs
- internal: Internal system APIs

Responsibilities:
- Router composition
- Namespace organization
- API version separation
- Internal/public route isolation
"""

from fastapi import APIRouter

api_router = APIRouter()

__all__ = ["api_router"]