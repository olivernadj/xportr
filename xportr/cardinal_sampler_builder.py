import time
from abc import ABC
from typing import Any, TypeVar
from .requirements import MetricType, AggregationModes, Requirements
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

    def set(self, value: T, timestamp: int):
        raise NotImplementedError

    def get(self) -> TimestampedDeque[tuple[int, Any]]:
        raise NotImplementedError


class MostRecentSampler(Sampler):
    def set(self, value: T, timestamp: int):
        timestamp = timestamp if timestamp is not None else time.time_ns()
        self.outbox.append((timestamp, value))

    def get(self) -> TimestampedDeque[tuple[int, Any]]:
        return self.outbox.get_all_non_expired()


class AllSampler(Sampler):
    def set(self, value: T, timestamp: int = None):
        timestamp = timestamp if timestamp is not None else time.time_ns()
        self.outbox.append((timestamp, value))

    def get(self) -> TimestampedDeque[tuple[int, Any]]:
        return self.outbox.get_all_non_expired()


class AverageSampler(Sampler):
    pass


class MaxSampler(Sampler):
    pass


class MinSampler(Sampler):
    pass


class SumSampler(Sampler):
    pass


class Cardinal(ABC):
    requirements: Requirements
    sampler: Sampler

    def __init__(self, requirements: Requirements, sampler: Sampler):
        self.requirements = requirements
        self.sampler = sampler

    def set(self, value: T, timestamp: int = None):
        raise NotImplementedError

    def get(self) -> TimestampedDeque[tuple[int, Any]]:
        raise NotImplementedError


class GaugeCardinal(Cardinal):

    def set(self, value: T, timestamp: int = None):
        self.sampler.set(value=value, timestamp=timestamp)

    def get(self) -> TimestampedDeque[tuple[int, Any]]:
        return self.sampler.get()


class CounterCardinal(Cardinal):
    pass


class SummaryCardinal(Cardinal):
    pass


class HistogramCardinal(Cardinal):
    pass


CARDINALS: dict[MetricType, Any] = {
    MetricType.GAUGE: GaugeCardinal,
    MetricType.COUNTER: CounterCardinal,
    MetricType.SUMMARY: SummaryCardinal,
    MetricType.HISTOGRAM: HistogramCardinal,
}

AGGREGATIONS: dict[AggregationModes, Any] = {
    AggregationModes.MOST_RECENT: MostRecentSampler,
    AggregationModes.ALL: AllSampler,
    AggregationModes.AVERAGE: AverageSampler,
    AggregationModes.MAX: MaxSampler,
    AggregationModes.MIN: MinSampler,
    AggregationModes.SUM: SumSampler,
}


def cardinal_sampler_builder(requirements: Requirements) -> Cardinal:
    sampler_class = AGGREGATIONS[requirements.aggregation]
    sampler = sampler_class(requirements=requirements)
    cardinal_class = CARDINALS[requirements.metric_type]
    cardinal = cardinal_class(requirements=requirements, sampler=sampler)
    return cardinal
