from __future__ import annotations

from collections import defaultdict, deque
from datetime import datetime, timedelta


class RateLimiter:
    def __init__(self, attempts: int, window_seconds: int) -> None:
        self.attempts = attempts
        self.window = timedelta(seconds=window_seconds)
        self._events: dict[str, deque[datetime]] = defaultdict(deque)

    def check(self, key: str) -> None:
        now = datetime.utcnow()
        bucket = self._events[key]
        while bucket and now - bucket[0] > self.window:
            bucket.popleft()
        if len(bucket) >= self.attempts:
            raise ValueError("Rate limit exceeded")
        bucket.append(now)
