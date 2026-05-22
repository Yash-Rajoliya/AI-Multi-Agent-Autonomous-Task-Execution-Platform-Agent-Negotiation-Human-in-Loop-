import time
from collections import defaultdict, deque
from collections.abc import Callable
from typing import Any

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from apps.api_gateway.config import settings


class RateLimiterMiddleware(BaseHTTPMiddleware):
    """Simple in-memory sliding window rate limiter."""

    def __init__(self, app) -> None:
        super().__init__(app)

        self.storage: dict[str, deque] = defaultdict(
            deque,
        )

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any],
    ):
        client = request.client

        if client is None:
            return JSONResponse(
                status_code=400,
                content={
                    "detail": (
                        "Unable to determine client IP"
                    ),
                },
            )

        client_ip = client.host

        now = time.time()

        request_window = self.storage[client_ip]

        while request_window and (
            now - request_window[0]
        ) >= 60:
            request_window.popleft()

        if (
            len(request_window)
            >= settings.RATE_LIMIT_PER_MINUTE
        ):
            return JSONResponse(
                status_code=429,
                content={
                    "detail": (
                        "Rate limit exceeded"
                    ),
                },
                headers={
                    "Retry-After": "60",
                },
            )

        request_window.append(now)

        response = await call_next(request)

        response.headers[
            "X-RateLimit-Limit"
        ] = str(settings.RATE_LIMIT_PER_MINUTE)

        response.headers[
            "X-RateLimit-Remaining"
        ] = str(
            max(
                0,
                settings.RATE_LIMIT_PER_MINUTE
                - len(request_window),
            ),
        )

        return response