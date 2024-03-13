import time
from typing import Iterable
from collections import deque


class TimestampedDeque(deque):
    """Deques support thread-safe, memory efficient appends and pops from either side of the
    deque"""
    _ttl: int = 0

    def __init__(self, elems_with_ts: Iterable, elems_without_ts: Iterable, maxlen: int, ttl: int):
        self._ttl = ttl * 1000000000  # seconds to nanoseconds
        deque.__init__(self, iterable=elems_with_ts, maxlen=maxlen)
        if elems_without_ts:
            self.ts_extend(iterable=elems_without_ts)

    def ts_extend(self, iterable: Iterable, entrance_timestamp: int = None):
        entrance_timestamp = time.time_ns() if entrance_timestamp is None else entrance_timestamp
        for elem in iterable:
            self.append((entrance_timestamp, elem))

    def ts_append(self, elem, entrance_timestamp: int = None):
        entrance_timestamp = time.time_ns() if entrance_timestamp is None else entrance_timestamp
        self.append((entrance_timestamp, elem))

    def get_all_non_expired(self) -> 'TimestampedDeque':
        must_entered_after = 0 if self._ttl == 0 else time.time_ns() - self._ttl
        return TimestampedDeque(
            elems_with_ts=[e for e in self if e[0] > must_entered_after],
            elems_without_ts=(), maxlen=self.maxlen, ttl=self._ttl)
