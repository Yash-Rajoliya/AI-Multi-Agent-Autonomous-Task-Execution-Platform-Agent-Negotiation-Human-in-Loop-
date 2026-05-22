from collections.abc import Callable
from typing import Any

import jwt
from fastapi import Request
from jwt import ExpiredSignatureError, InvalidTokenError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from apps.api_gateway.config import settings


class AuthMiddleware(BaseHTTPMiddleware):
    """JWT authentication middleware."""

    EXCLUDED_PATHS = {
        "/docs",
        "/openapi.json",
        "/redoc",
        "/health",
    }

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[..., Any],
    ):
        path = request.url.path

        if (
            path.startswith("/internal")
            or path in self.EXCLUDED_PATHS
        ):
            return await call_next(request)

        auth_header = request.headers.get(
            "Authorization",
        )

        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": (
                        "Missing Authorization header"
                    ),
                },
            )

        try:
            scheme, token = auth_header.split(
                " ",
                maxsplit=1,
            )

        except ValueError:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": (
                        "Invalid authorization format"
                    ),
                },
            )

        if scheme.lower() != "bearer":
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid auth scheme",
                },
            )

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[
                    settings.JWT_ALGORITHM,
                ],
            )

            request.state.user = payload

        except ExpiredSignatureError:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Token expired",
                },
            )

        except InvalidTokenError:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid token",
                },
            )

        return await call_next(request)