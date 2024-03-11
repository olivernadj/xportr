from enum import Enum, auto
from dataclasses import dataclass, field
from .utils import validate_metric_name, validate_label_names

DEFAULT_MAX_SAMPLES = 100


class MetricType(Enum):
    GAUGE = "gauge"
    COUNTER = "counter"
    SUMMARY = "summary"
    HISTOGRAM = "histogram"


class AggregationModes(Enum):
    MOST_RECENT = auto()  # Only the latest value will be preserved. No aggregation.
    ALL = auto()  # All Samples within a single Cardinal will be preserved. Requires timestamp mode.
    # AVERAGE, MAX, MIN and SUM are aggregated on exporter level. Prometheus just scrap an already aggregated
    # values without knowing it. MetricPool.evaluate() evaluates and reset aggregation. It should call right
    # before dump the metrics.
    AVERAGE = auto()  # ^^
    MAX = auto()  # ^^
    MIN = auto()  # ^^
    SUM = auto()  # ^^


@dataclass
class Requirements:
    metric_type: MetricType
    aggregation: AggregationModes = AggregationModes.MOST_RECENT
    # Max Samples of a single Cardinal before the least recent will be cleaned up. Requires AggregationModes.ALL
    max_samples: int = DEFAULT_MAX_SAMPLES
    time_to_live: int = 0  # 0 meas never expire, otherwise after X seconds the Sample will be cleaned.


@dataclass
class Sample:
    value: float
    timestamp: int = None


@dataclass
class Cardinal:
    requirements: Requirements
    samples: set[Sample] = field(default_factory=set)


@dataclass
class Metric:
    name: str
    documentation: str
    labels_w_default: dict[str, str]
    requirements: Requirements
    _cardinals: dict[tuple, Cardinal] = field(default_factory=dict)

    def __post_init__(self):
        validate_metric_name(self.name)
        validate_label_names(self.labels_w_default)

    def labels(self, **kwargs: [str, str]) -> Cardinal:
        merged_label_kwargs = {
            **self.labels_w_default,
            **kwargs
        }
        merged_sorted_label_kwargs = dict(sorted(merged_label_kwargs.items()))
        key = tuple(merged_sorted_label_kwargs.values())
        if key not in self._cardinals:
            metric = Cardinal(
                requirements=self.requirements,
            )
            self._cardinals[key] = metric
        return self._cardinals[key]

    def get_cardinals(self) -> dict[tuple, Cardinal]:
        return self._cardinals
