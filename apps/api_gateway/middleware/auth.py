from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import jwt

from ..config import settings


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # Skip internal endpoints
        if request.url.path.startswith("/internal"):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(status_code=401, detail="Missing Authorization header")

        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise ValueError()

            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM]
            )

            request.state.user = payload

        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

        return await call_next(request)