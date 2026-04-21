from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass
from threading import Lock

from flask import Request

from uzix.errors import RateLimitError, UnauthorizedError


@dataclass(frozen=True)
class RateLimitState:
    limit: int
    remaining: int
    retry_after: int


class InMemoryRateLimiter:
    def __init__(self, *, limit: int, window_seconds: int, clock=None):
        self.limit = limit
        self.window_seconds = window_seconds
        self.clock = clock or time.monotonic
        self._buckets: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str) -> RateLimitState:
        now = self.clock()
        with self._lock:
            bucket = self._buckets[key]
            cutoff = now - self.window_seconds
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()

            if len(bucket) >= self.limit:
                retry_after = max(1, int(self.window_seconds - (now - bucket[0])))
                return RateLimitState(limit=self.limit, remaining=0, retry_after=retry_after)

            bucket.append(now)
            remaining = max(0, self.limit - len(bucket))
            return RateLimitState(limit=self.limit, remaining=remaining, retry_after=0)


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.headers.get("X-Real-IP"):
        return request.headers["X-Real-IP"].strip()
    return request.remote_addr or "unknown"


def get_api_key(request: Request, header_name: str) -> str | None:
    header_value = request.headers.get(header_name)
    if header_value:
        return header_value.strip()

    authorization = request.headers.get("Authorization", "")
    if authorization.lower().startswith("bearer "):
        return authorization[7:].strip()

    return None


def require_api_key(request: Request, *, allowed_keys: tuple[str, ...], header_name: str) -> str | None:
    if not allowed_keys:
        return None

    api_key = get_api_key(request, header_name)
    if api_key and api_key in allowed_keys:
        return api_key

    raise UnauthorizedError(f"Missing or invalid API key. Provide it via {header_name} or Authorization: Bearer <key>.")


def enforce_rate_limit(rate_limiter: InMemoryRateLimiter, key: str) -> RateLimitState:
    state = rate_limiter.check(key)
    if state.retry_after > 0:
        raise RateLimitError(retry_after=state.retry_after)
    return state
