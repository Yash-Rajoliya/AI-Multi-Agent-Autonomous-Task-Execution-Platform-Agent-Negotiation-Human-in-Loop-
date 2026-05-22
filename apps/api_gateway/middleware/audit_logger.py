import logging
import time
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("audit")


class AuditLoggerMiddleware(BaseHTTPMiddleware):
    """Middleware for structured API audit logging."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any],
    ) -> Response:
        start_time = time.perf_counter()

        try:
            response = await call_next(request)

        except Exception as exc:
            duration_ms = round(
                (time.perf_counter() - start_time) * 1000,
                2,
            )

            logger.exception(
                "Request failed",
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "duration_ms": duration_ms,
                    "request_id": getattr(
                        request.state,
                        "request_id",
                        None,
                    ),
                    "error": str(exc),
                },
            )

            raise

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2,
        )

        logger.info(
            "Request completed",
            extra={
                "path": request.url.path,
                "method": request.method,
                "status_code": response.status_code,
                "duration_ms": duration_ms,
                "request_id": getattr(
                    request.state,
                    "request_id",
                    None,
                ),
                "user": getattr(
                    request.state,
                    "user",
                    None,
                ),
            },
        )

        return response