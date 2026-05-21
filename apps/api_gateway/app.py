from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .lifecycle import register_lifecycle
from .routes.v1 import task_routes, agent_routes, workflow_routes
from .routes.internal import system_routes

from .middleware.request_context import RequestContextMiddleware
from .middleware.audit_logger import AuditLoggerMiddleware
from .middleware.rate_limiter import RateLimiterMiddleware
from .middleware.auth import AuthMiddleware

from .config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url=None,
    )

    # Middleware stack (ordered intentionally)
    app.add_middleware(RequestContextMiddleware)
    app.add_middleware(AuditLoggerMiddleware)
    app.add_middleware(RateLimiterMiddleware)
    app.add_middleware(AuthMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(task_routes.router, prefix="/api/v1/tasks", tags=["Tasks"])
    app.include_router(agent_routes.router, prefix="/api/v1/agents", tags=["Agents"])
    app.include_router(workflow_routes.router, prefix="/api/v1/workflows", tags=["Workflows"])
    app.include_router(system_routes.router, prefix="/internal", tags=["Internal"])

    register_lifecycle(app)

    return app