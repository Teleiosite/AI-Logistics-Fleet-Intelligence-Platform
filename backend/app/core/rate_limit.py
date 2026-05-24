from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from threading import Lock

from fastapi import HTTPException, Request, status


@dataclass(frozen=True)
class RateLimitRule:
    requests: int
    window_seconds: int


class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._events: dict[str, deque[datetime]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, rule: RateLimitRule) -> None:
        now = datetime.now(timezone.utc)
        threshold = now - timedelta(seconds=rule.window_seconds)

        with self._lock:
            events = self._events[key]
            while events and events[0] < threshold:
                events.popleft()

            if len(events) >= rule.requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Try again in {rule.window_seconds} seconds.",
                )

            events.append(now)


rate_limiter = InMemoryRateLimiter()


def get_client_key(request: Request, suffix: str) -> str:
    client_host = request.client.host if request.client else "unknown"
    return f"{suffix}:{client_host}"
