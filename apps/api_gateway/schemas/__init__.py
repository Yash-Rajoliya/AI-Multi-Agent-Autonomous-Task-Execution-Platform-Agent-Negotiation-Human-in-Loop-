"""
Pydantic schema definitions for API Gateway.

Provides typed request and response models used
across all gateway endpoints.

Responsibilities:
- Request validation
- Response serialization
- OpenAPI schema generation
- Data normalization
- Contract enforcement

Schema Categories:
- Task schemas
- Agent schemas
- Workflow schemas
- Approval schemas
- Shared response schemas

Design Goals:
- Strong typing
- Explicit contracts
- Backward compatibility
- API consistency
"""

__all__: list[str] = [
    "task_schema",
    "agent_schema",
    "workflow_schema",
    "approval_schema",
    "response_schema",]