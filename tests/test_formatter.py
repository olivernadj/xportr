# pylint: disable=duplicate-code
import unittest
from xportr import (
    Requirements, MetricType, AggregationModes,
    Metric, MetricPool
)
from xportr.prometheus import (
    format_sample_line, generate_metric_with_cardinals, generate_all_metrics
)


class TestPrometheusFormatter(unittest.TestCase):
    def setUp(self) -> None:
        self._metric_pool_dict: [tuple, Metric] = {}  # empty dict for each setUp
        self.metric_pool = MetricPool(self._metric_pool_dict)

    def test_sample_line(self) -> None:
        metric = self.metric_pool.get_or_create(
            name='metric1', documentation='Documentation 1',
            labels_w_default={'label1': 'default1'},
            requirements=Requirements(
                metric_type=MetricType.GAUGE,
                aggregation=AggregationModes.MOST_RECENT)
        )
        metric.labels().set(5)
        metric_labels_keys = metric.labels_w_default.keys()
        for labels, cardinal in metric.get_cardinals().items():
            cardinal_labels = dict(zip(metric_labels_keys, labels))
            for sample in cardinal.get():
                line_ts_txt = format_sample_line(
                    name=metric.name,
                    labels=cardinal_labels,
                    value=sample[1],
                    timestamp_ns=1710322834559256212,
                )
                self.assertEqual(
                    "metric1{label1=\"default1\"} 5.0 1710322834559\n",
                    line_ts_txt)
                line_txt = format_sample_line(
                    name=metric.name,
                    labels=cardinal_labels,
                    value=sample[1],
                )
                self.assertEqual(
                    "metric1{label1=\"default1\"} 5.0\n",
                    line_txt)

    def test_metric_with_cardinals(self) -> None:
        metric = self.metric_pool.get_or_create(
            name='metric1', documentation='Documentation 1',
            labels_w_default={'label1': 'default1'},
            requirements=Requirements(
                metric_type=MetricType.GAUGE,
                aggregation=AggregationModes.MOST_RECENT)
        )
        with self.subTest(name="empty_metric"):
            self.assertEqual("", generate_metric_with_cardinals(metric))
        with self.subTest(name="cardinal_with_sample"):
            metric.labels().set(5)
            metric_with_cardinals_txt = generate_metric_with_cardinals(metric)
            self.assertEqual(
                "# HELP metric1 Documentation 1\n"
                "# TYPE metric1 gauge\n"
                "metric1{label1=\"default1\"} 5.0\n",
                metric_with_cardinals_txt)

    def test_all_metrics(self) -> None:
        self.metric_pool.get_or_create(
            name='metric1', documentation='Documentation 1',
            labels_w_default={'label1': 'default1'},
            requirements=Requirements(
                metric_type=MetricType.GAUGE,
                aggregation=AggregationModes.MOST_RECENT)
        ).labels().set(5)
        cardinal = self.metric_pool.get_or_create(
            name='metric2', documentation='Documentation 2',
            labels_w_default={'label2': 'default2'},
            requirements=Requirements(
                metric_type=MetricType.GAUGE,
                aggregation=AggregationModes.ALL)
        ).labels()
        cardinal.set(7, 1710322834558256212)
        cardinal.set(6.5, 1710322834559256212)
        with self.subTest(name="multiple_metrics"):
            metric_with_cardinals_txt = generate_all_metrics(self.metric_pool.get_metrics())
            self.assertEqual(
                "# HELP metric1 Documentation 1\n"
                "# TYPE metric1 gauge\n"
                "metric1{label1=\"default1\"} 5.0\n"
                "# HELP metric2 Documentation 2\n"
                "# TYPE metric2 gauge\n"
                "metric2{label2=\"default2\"} 7.0 1710322834558\n"
                "metric2{label2=\"default2\"} 6.5 1710322834559\n",
                metric_with_cardinals_txt)
