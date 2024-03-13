from .model import Metric, Requirements


METRIC_POOL: dict[tuple, Metric] = {}


def validate_metric_pool(metric_pool: dict[tuple, Metric]):
    for key, metric in metric_pool.items():
        if not isinstance(key, tuple) or not isinstance(metric, Metric):
            raise TypeError("metric_pool must be dict[str, Metric] type")
        if key is not ('name',) + (tuple(sorted(metric.labels_w_default.keys()))):
            raise ValueError("key must be generated by: \""
                             "('name',) + (tuple(sorted(labels.keys())))\"")


class MetricPool:
    _metric_pool: dict[tuple, Metric] = {}

    def __init__(self, metric_pool: dict[tuple, Metric] = None):
        if metric_pool is None:
            metric_pool = METRIC_POOL
        validate_metric_pool(metric_pool)
        self._metric_pool = metric_pool

    def get_or_create(self,
                      name: str,
                      documentation: str,
                      labels_w_default: dict[str, str],
                      requirements: Requirements) -> Metric:
        """Returns an existing Metric instance from the pool or creates a new if name and label
        keys are not matching.

        The documentation and metric_type parameters are ignored if the instance already exists.
        """
        key = (name,) + (tuple(sorted(labels_w_default.keys())))
        if key not in self._metric_pool:
            metric = Metric(
                name=name,
                documentation=documentation,
                labels_w_default=labels_w_default,
                requirements=requirements,
            )
            self._metric_pool[key] = metric
        return self._metric_pool[key]

    def get_metrics(self) -> dict[tuple, Metric]:
        return self._metric_pool
