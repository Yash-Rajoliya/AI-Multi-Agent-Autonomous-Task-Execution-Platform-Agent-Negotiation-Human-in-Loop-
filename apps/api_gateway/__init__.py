# apps/api-gateway/__init__.py

"""
API Gateway application package.

Acts as the primary entry point for external clients and platform consumers.

Responsibilities:
- REST API exposure
- Authentication and authorization
- Request validation
- Tenant isolation
- Rate limiting
- Audit logging
- API lifecycle management
- Service orchestration routing
"""

__version__ = "1.0.0"

__all__ = [
    "app",
    "config",
    "dependencies",
    "lifecycle",
    "controllers",
    "middleware",
    "routes",
    "schemas",
    "utils",
]