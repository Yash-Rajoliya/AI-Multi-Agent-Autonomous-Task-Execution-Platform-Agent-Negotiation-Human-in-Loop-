"""
Version 1 public API routes.

Contains stable REST API endpoints exposed
to external consumers and platform clients.

Domains:
- Task management
- Agent orchestration
- Workflow execution
- Evaluation pipelines
- Tenant management
- Human approval workflows

API Principles:
- Backward compatibility
- Schema-driven validation
- Stateless request handling
- Service-oriented architecture
"""

from fastapi import APIRouter

v1_router = APIRouter(prefix="/v1")

__all__ = ["v1_router"]