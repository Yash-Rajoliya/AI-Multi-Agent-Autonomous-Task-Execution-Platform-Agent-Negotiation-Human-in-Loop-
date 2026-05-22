import uuid
from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestContextMiddleware(
    BaseHTTPMiddleware,
):
    """Inject request context metadata."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any],
    ) -> Response:
        request_id = request.headers.get(
            "X-Request-ID",
        )

        if not request_id:
            request_id = str(uuid.uuid4())

        trace_id = request.headers.get(
            "X-Trace-ID",
            request_id,
        )

        request.state.request_id = request_id
        request.state.trace_id = trace_id

        response = await call_next(request)

        response.headers[
            "X-Request-ID"
        ] = request_id

        response.headers[
            "X-Trace-ID"
        ] = trace_id

        return response