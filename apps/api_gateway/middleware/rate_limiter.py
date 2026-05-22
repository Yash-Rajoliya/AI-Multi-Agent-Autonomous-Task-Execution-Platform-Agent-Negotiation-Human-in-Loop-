from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import time
from collections import defaultdict

from ..config import settings


class RateLimiterMiddleware(BaseHTTPMiddleware):

    def __init__(self, app):
        super().__init__(app)
        self.storage = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()

        window = self.storage[ip]
        window[:] = [t for t in window if now - t < 60]

        if len(window) >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        window.append(now)

        return await call_next(request)