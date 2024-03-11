import unittest
from model import Metric, MetricType
from pool import MetricPool


class TestMetricPool(unittest.TestCase):
    def setUp(self) -> None:
        self._metric_pool: [tuple, Metric] = {}
        self.metric_pool = MetricPool(self._metric_pool)
        self.metric_pool.get_or_create(
            name='metric1', documentation='Documentation 1',
            labels_w_default={'label1': 'default1'},
            metric_type=MetricType.COUNTER
        )
        self.metric_pool.get_or_create(
            name='metric2', documentation='Documentation 2',
            labels_w_default={'label2': 'default2'},
            metric_type=MetricType.GAUGE
        )

    def test_validate_existing_pool(self) -> None:
        with self.subTest(name="value_error"):
            metric_pool = {
                ('metric1', 'label1'): Metric(
                    name='metric1', documentation='Documentation 1',
                    labels_w_default={'label2': 'default1'},
                    metric_type=MetricType.COUNTER),
            }
            with self.assertRaises(ValueError):
                MetricPool(metric_pool)
        with self.subTest(name="type_error"):
            metric_pool = {
                'metric1-label1': Metric(
                    name='metric1', documentation='Documentation 1',
                    labels_w_default={'label1': 'default1'},
                    metric_type=MetricType.COUNTER),
            }
            with self.assertRaises(TypeError):
                MetricPool(metric_pool)

    def test_get_or_create_existing_metric(self):
        existing_metric_key = ('metric1', 'label1')
        existing_metric = self._metric_pool[existing_metric_key]
        retrieved_metric = self.metric_pool.get_or_create('metric1', 'Documentation 1', {'label1': 'still-the-same'},
                                                          MetricType.COUNTER)
        self.assertIs(retrieved_metric, existing_metric)

    def test_get_or_create_new_metric(self):
        new_metric_name = 'new_metric'
        new_metric_labels = ('label3', 'default3')
        new_metric_key = (new_metric_name, new_metric_labels[0])
        new_metric = self.metric_pool.get_or_create(new_metric_name, 'New Metric Documentation', {'label3': 'default3'},
                                                    MetricType.SUMMARY)
        self.assertIsInstance(new_metric, Metric)
        self.assertEqual(new_metric.name, new_metric_name)
        self.assertIn(new_metric_key, self.metric_pool._metric_pool)

    def test_get_or_create_different_labels(self):
        metric_name = 'metric3'
        metric1 = self.metric_pool.get_or_create(metric_name, 'Metric 3 Documentation', {'label1': 'value1'},
                                                 MetricType.HISTOGRAM)
        metric2 = self.metric_pool.get_or_create(metric_name, 'Metric 3 Documentation', {'label2': 'value2'},
                                                 MetricType.HISTOGRAM)
        self.assertIsNot(metric1, metric2)  # Different metric instances
