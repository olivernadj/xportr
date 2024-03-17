# pylint: disable=duplicate-code
import unittest
from xportr import (
    Metric, MetricType, MetricPool, Cardinal, Requirements
)


class TestModelCardinal(unittest.TestCase):
    def setUp(self) -> None:
        self._metric_pool_dict: [tuple, Metric] = {}  # empty dict for each setUp
        self._cardinals: dict[tuple, Cardinal] = {}
        self.metric_pool = MetricPool(self._metric_pool_dict)
        self.metric = self.metric_pool.get_or_create(
            name='metric1', documentation='Documentation 1',
            labels_w_default={'zlabel1': 'cardinal1', 'label2': 'cardinal2', 'c': ''},
            requirements=Requirements(metric_type=MetricType.GAUGE)
        )

    def test_same_labels(self) -> None:
        with self.subTest(name="default_is_same"):
            cardinal1 = self.metric.labels()
            cardinal2 = self.metric.labels(zlabel1='cardinal1')
            cardinal3 = self.metric.labels(zlabel1='cardinal1', label2='cardinal2')
            self.assertIs(cardinal1, cardinal2)
            self.assertIs(cardinal1, cardinal3)
        with self.subTest(name="default_overload"):
            cardinal1 = self.metric.labels(zlabel1='foo', label2='bar')
            cardinal2 = self.metric.labels(zlabel1='foo', label2='bar')
            self.assertIs(cardinal1, cardinal2)

    def test_different_labels_cardinal(self) -> None:
        cardinal1 = self.metric.labels(zlabel1='foo', label2='bar1', c='xyz')
        cardinal2 = self.metric.labels(zlabel1='foo', label2='bar2', c='xyz')
        self.assertIsNot(cardinal1, cardinal2)

    def test_extra_labels_cardinal(self) -> None:
        with self.assertRaises(KeyError):
            self.metric.labels(zlabel1='foo', label2='bar1', c='xyz', o_O='O_o')
