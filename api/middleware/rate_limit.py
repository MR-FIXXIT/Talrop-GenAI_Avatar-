from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, limit_per_minute: int = 60):
        super().__init__(app)
        self.limit = limit_per_minute
        self.clients = {}

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        now = time.time()

        window = self.clients.get(ip, [])
        window = [t for t in window if now - t < 60]

        if len(window) >= self.limit:
            raise HTTPException(status_code=429, detail="Rate limit exceeded")

        window.append(now)
        self.clients[ip] = window

        return await call_next(request)
