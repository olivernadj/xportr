import unittest
from xportr import (
    Requirements, MetricType, AggregationModes,
    Metric, MetricPool
)
from xportr.prometheus import (
    sample_line
)


class TestPrometheusFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self._metric_pool_dict: [tuple, Metric] = {}  # empty dict for each setUp
        self.metric_pool = MetricPool(self._metric_pool_dict)

    def test_sample_line(self):
        metric = self.metric_pool.get_or_create(
            name='metric1', documentation='Documentation 1',
            labels_w_default={'label1': 'default1'},
            requirements=Requirements(metric_type=MetricType.GAUGE, aggregation=AggregationModes.MOST_RECENT)
        )
        metric.labels().set(5)
        metric_labes_keys = metric.labels_w_default.keys()
        for labels, cardinal in metric.get_cardinals().items():
            cardinal_labels = dict(zip(metric_labes_keys, labels))
            for sample in cardinal.get():
                line_ts_txt = sample_line(
                    name=metric.name,
                    labels=cardinal_labels,
                    value=sample[1],
                    timestamp_ns=1710322834559256212,
                )
                self.assertEqual("metric1{label1=\"default1\"} 5.0 1710322834559256\n", line_ts_txt)
                line_txt = sample_line(
                    name=metric.name,
                    labels=cardinal_labels,
                    value=sample[1],
                )
                self.assertEqual("metric1{label1=\"default1\"} 5.0\n", line_txt)

