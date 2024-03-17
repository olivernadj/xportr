# from enum import Enum, auto
# from typing import Any
from typing import Callable
from dataclasses import dataclass, field
from .utils import validate_metric_name, validate_label_names
from .cardinal_sampler_builder import cardinal_sampler_builder, Cardinal
from .requirements import Requirements

# @dataclass
# class Sample:
#     value: float
#     timestamp: int = None
#
#
# @dataclass
# class Cardinal:
#     requirements: Requirements
#     sampler: Any
#
#     # samples: set[Sample] = field(default_factory=set)
#
#     def __post_init__(self):
#         CardinalSamplerBuilder.build_metric(self.requirements)


@dataclass
class Metric:
    name: str
    documentation: str
    labels_w_default: dict[str, str]
    requirements: Requirements
    builder: Callable = None
    _cardinals: dict[tuple, Cardinal] = field(default_factory=dict)

    def __post_init__(self):
        validate_metric_name(self.name)
        validate_label_names(self.labels_w_default)
        if self.builder is None:
            self.builder = cardinal_sampler_builder

    def labels(self, **kwargs: [str, str]) -> Cardinal:
        extra_labels = [key for key in kwargs if key not in self.labels_w_default]
        if extra_labels:
            raise KeyError(f"Extra labels: {extra_labels}")
        merged_label_kwargs = {
            **self.labels_w_default,
            **kwargs
        }
        merged_sorted_label_kwargs = dict(sorted(merged_label_kwargs.items()))
        key = tuple(merged_sorted_label_kwargs.values())
        if key not in self._cardinals:
            cardinal = self.builder(
                requirements=self.requirements,
            )
            self._cardinals[key] = cardinal
        return self._cardinals[key]

    def get_cardinals(self) -> dict[tuple, Cardinal]:
        return self._cardinals
