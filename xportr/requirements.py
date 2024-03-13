from enum import Enum, auto
from dataclasses import dataclass

DEFAULT_MAX_SAMPLES = 100


class MetricType(Enum):
    GAUGE = "gauge"
    COUNTER = "counter"
    SUMMARY = "summary"
    HISTOGRAM = "histogram"


class AggregationModes(Enum):
    MOST_RECENT = auto()  # Only the latest value will be preserved. No aggregation.
    ALL = auto()  # All Samples within a single Cardinal will be preserved. Enforces timestamp mode.
    # AVERAGE, MAX, MIN and SUM are aggregated on exporter level. Prometheus just scrap an
    # already aggregated values without knowing it. MetricPool.evaluate() evaluates and reset
    # aggregation. It should call right before dump the metrics.
    AVERAGE = auto()  # ^^
    MAX = auto()  # ^^
    MIN = auto()  # ^^
    SUM = auto()  # ^^


@dataclass
class Requirements:
    metric_type: MetricType
    aggregation: AggregationModes = AggregationModes.MOST_RECENT
    # Max Samples of a single Cardinal before the least recent will be cleaned up. Requires
    # AggregationModes.ALL
    max_samples: int = DEFAULT_MAX_SAMPLES
    # 0 meas never expire, otherwise after X seconds the Sample will be cleaned.
    time_to_live: int = 0
    timestamped: bool = False

    def __post_init__(self):
        if self.aggregation == AggregationModes.ALL:
            self.timestamped = True
        if self.aggregation not in [AggregationModes.ALL]:
            self.max_samples = 1
