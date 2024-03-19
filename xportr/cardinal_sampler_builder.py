from typing import Any, TypeVar
from .requirements import MetricType, AggregationModes, Requirements
from .cardinal import (
    Cardinal, GaugeCardinal, CounterCardinal, SummaryCardinal, HistogramCardinal
)
from .sampler import (
    MostRecentSampler, AllSampler, AverageSampler, MaxSampler, MinSampler, SumSampler
)

T = TypeVar("T")

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
