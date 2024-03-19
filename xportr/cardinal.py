import time
from abc import ABC
from typing import Any, TypeVar
from .requirements import Requirements
from .timestamped_deque import TimestampedDeque
from .sampler import Sampler

T = TypeVar("T")


class Cardinal(ABC):
    requirements: Requirements
    sampler: Sampler

    def __init__(self, requirements: Requirements, sampler: Sampler):
        self.requirements = requirements
        self.sampler = sampler

    def set(self, amount: T, timestamp: int = None):
        raise NotImplementedError

    def inc(self, amount: T = None, timestamp: int = None):
        raise NotImplementedError

    def get(self) -> TimestampedDeque[tuple[int, Any]]:
        raise NotImplementedError


class GaugeCardinal(Cardinal):
    def set(self, amount: T, timestamp: int = None):
        self.sampler.set(amount=amount, timestamp=timestamp)

    def get(self) -> TimestampedDeque[tuple[int, Any]]:
        return self.sampler.get()


class CounterCardinal(Cardinal):
    def inc(self, amount: T = None, timestamp: int = None):
        amount = amount if amount is not None else 1
        if amount < 0:
            raise ValueError('Counters can only be incremented by non-negative amounts.')
        timestamp = timestamp if timestamp is not None else time.time_ns()
        samples = self.sampler.get()
        if samples:
            amount += samples[-1][1]  # [-1]:last element, [1]:amount
        self.sampler.set(amount=amount, timestamp=timestamp)

    def get(self) -> TimestampedDeque[tuple[int, Any]]:
        return self.sampler.get()


class SummaryCardinal(Cardinal):
    pass


class HistogramCardinal(Cardinal):
    pass
