"""
Internal system routes.

Provides operational and infrastructure-facing APIs
used by internal services and platform components.

Examples:
- Health checks
- Metrics endpoints
- System diagnostics
- Internal orchestration controls
- Readiness/liveness probes

Security Notes:
- Not intended for public exposure
- Protected through internal network policies
"""

from fastapi import APIRouter

internal_router = APIRouter(prefix="/internal")

__all__ = ["internal_router"]