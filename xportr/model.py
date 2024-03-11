from enum import Enum
from dataclasses import dataclass, field
from .utils import validate_metric_name, validate_label_names


class MetricType(Enum):
    GAUGE = "gauge"
    COUNTER = "counter"
    SUMMARY = "summary"
    HISTOGRAM = "histogram"


@dataclass
class Sample:
    value: float
    timestamp: int = None


@dataclass
class Entity:
    metric_type: MetricType
    samples: set[Sample] = field(default_factory=set)


@dataclass
class Metric:
    name: str
    documentation: str
    labels_w_default: dict[str, str]
    metric_type: MetricType
    _cardinals: dict[tuple, Entity] = field(default_factory=dict)

    def __post_init__(self):
        validate_metric_name(self.name)
        validate_label_names(self.labels_w_default)

    def labels(self, **kwargs: [str, str]) -> Entity:
        merged_sorted_label_kwargs = dict(sorted({
            **self.labels_w_default,
            **kwargs.items()
        }))
        key = tuple(sorted(merged_sorted_label_kwargs.values()))
        if key not in self._cardinals:
            metric = Entity(
                metric_type=self.metric_type,
            )
            self._cardinals[key] = metric
        return self._cardinals[key]

    def get_cardinals(self) -> dict[tuple, Entity]:
        return self._cardinals
