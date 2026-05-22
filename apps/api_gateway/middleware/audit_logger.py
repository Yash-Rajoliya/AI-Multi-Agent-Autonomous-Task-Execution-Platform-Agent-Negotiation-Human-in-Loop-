from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
import time
import logging

logger = logging.getLogger("audit")


class AuditLoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        start = time.time()

        response = await call_next(request)

        duration = time.time() - start

        logger.info({
            "path": request.url.path,
            "method": request.method,
            "status": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "user": getattr(request.state, "user", None)
        })

        return response