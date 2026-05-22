"""
API Gateway middleware package.

Middleware components provide request and response
interception for platform-wide cross-cutting concerns.

Responsibilities:
- Authentication enforcement
- RBAC authorization
- Request context propagation
- Audit logging
- Rate limiting
- Correlation ID management
- Security validation
- Observability instrumentation

Middleware Stack:
- auth
- rbac
- rate_limiter
- audit_logger
- request_context

Design Goals:
- Low overhead
- Stateless execution
- Centralized security controls
- Consistent request tracing
"""

__all__: list[str] = [
    "auth",
    "rbac",
    "rate_limiter",
    "audit_logger",
    "request_context",
]