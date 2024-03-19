import time
from abc import ABC
from typing import Any, TypeVar
from .requirements import Requirements
from .timestamped_deque import TimestampedDeque

T = TypeVar("T")


class Sampler(ABC):
    requirements: Requirements
    outbox: TimestampedDeque[tuple[int, Any]]

    def __init__(self, requirements: Requirements):
        self.requirements = requirements
        self.outbox = TimestampedDeque(
            elems_with_ts=(), elems_without_ts=(),
            maxlen=self.requirements.max_samples,
            ttl=self.requirements.time_to_live
        )

    def set(self, amount: T, timestamp: int = None):
        timestamp = timestamp if timestamp is not None else time.time_ns()
        self.outbox.append((timestamp, amount))

    def get(self) -> TimestampedDeque[tuple[int, Any]]:
        return self.outbox.get_all_non_expired()


class MostRecentSampler(Sampler):
    pass


class AllSampler(Sampler):
    pass


class AverageSampler(Sampler):
    pass


class MaxSampler(Sampler):
    pass


class MinSampler(Sampler):
    pass


class SumSampler(Sampler):
    pass
