# pylint: disable=duplicate-code
import time
import unittest
import random
from xportr import (
    Requirements, MetricType, AggregationModes, cardinal_sampler_builder,
    Metric, MetricPool
)


class TestCardinalSamplerBuilder(unittest.TestCase):
    def setUp(self):
        pass

    def test_build_all_possible_samplers(self):
        unique_cardinal_samplers = []
        for metric_type in MetricType:
            for aggregation_mode in AggregationModes:
                req = Requirements(
                    metric_type=metric_type,
                    aggregation=aggregation_mode
                )
                cardinal_sampler = cardinal_sampler_builder(requirements=req)
                build = (
                    cardinal_sampler.__class__.__name__,
                    cardinal_sampler.sampler.__class__.__name__)
                if build in unique_cardinal_samplers:
                    self.fail("Duplicated cardinal_sampler")
                unique_cardinal_samplers.append(build)


class TestCardinalSampler(unittest.TestCase):
    def setUp(self) -> None:
        self._metric_pool_dict: [tuple, Metric] = {}  # empty dict for each setUp
        self.metric_pool = MetricPool(self._metric_pool_dict)

    def test_gauge_most_recent(self):
        metric = self.metric_pool.get_or_create(
            name='metric1', documentation='Documentation 1',
            labels_w_default={'label1': 'default1'},
            requirements=Requirements(
                metric_type=MetricType.GAUGE,
                aggregation=AggregationModes.MOST_RECENT)
        )
        cardinal_sampler = metric.labels()
        with self.subTest(name="default_timestamp"):
            for _ in range(5):
                v = random.uniform(-50, 50)
                cardinal_sampler.set(v)
                self.assertEqual(v, cardinal_sampler.get()[0][1])
        with self.subTest(name="explicit_timestamp"):
            for _ in range(5):
                v = random.uniform(-50, 50)
                ts = time.time_ns()
                cardinal_sampler.set(v, ts)
                self.assertEqual((ts, v), cardinal_sampler.get()[0])

    def test_gauge_all(self):
        metric = self.metric_pool.get_or_create(
            name='metric1', documentation='Documentation 1',
            labels_w_default={'label1': 'default_timestamp'},
            requirements=Requirements(
                metric_type=MetricType.GAUGE,
                aggregation=AggregationModes.ALL)
        )
        cardinal_sampler = metric.labels()
        with self.subTest(name="default_timestamp"):
            for i in range(5):
                v = random.uniform(-50, 50)
                cardinal_sampler.set(v)
                self.assertEqual(v, cardinal_sampler.get()[i][1])
        cardinal_sampler = metric.labels(label1='explicit_timestamp')
        with self.subTest(name="explicit_timestamp"):
            for i in range(5):
                v = random.uniform(-50, 50)
                ts = time.time_ns()
                cardinal_sampler.set(v, ts)
                self.assertEqual((ts, v), cardinal_sampler.get()[i])
        with self.subTest(name="maxlen"):
            cardinal_sampler = self.metric_pool.get_or_create(
                name='maxlen', documentation='Documentation maxlen',
                labels_w_default={'label1': 'default'},
                requirements=Requirements(
                    metric_type=MetricType.GAUGE,
                    aggregation=AggregationModes.ALL,
                    max_samples=16)
            ).labels(label1='maxlen')
            for i in range(32):
                v = random.uniform(-50, 50)
                cardinal_sampler.set(v)
                self.assertEqual((i+1) if i < 16 else 16, len(cardinal_sampler.get()))

    def test_counter_most_recent(self):
        metric = self.metric_pool.get_or_create(
            name='counter1', documentation='Documentation of counter 1',
            labels_w_default={'label1': 'default1'},
            requirements=Requirements(
                metric_type=MetricType.COUNTER,
                aggregation=AggregationModes.MOST_RECENT)
        )
        cardinal_sampler = metric.labels()
        with self.subTest(name="default_timestamp"):
            total = 0
            for _ in range(5):
                v = random.uniform(0, 50)
                total += v
                cardinal_sampler.inc(v)
                self.assertEqual(total, cardinal_sampler.get()[0][1])
        cardinal_sampler = metric.labels(label1='explicit_timestamp')
        with self.subTest(name="explicit_timestamp"):
            total = 0
            for _ in range(5):
                v = random.uniform(0, 50)
                total += v
                ts = time.time_ns()
                cardinal_sampler.inc(v, ts)
                self.assertEqual((ts, total), cardinal_sampler.get()[0])
        with self.subTest(name="expect_raises"):
            cardinal_sampler = metric.labels(label1='expect_raises')
            with self.assertRaises(ValueError):
                cardinal_sampler.inc(-1)

    def test_counter_all(self):
        metric = self.metric_pool.get_or_create(
            name='metric1', documentation='Documentation 1',
            labels_w_default={'label1': 'default_timestamp'},
            requirements=Requirements(
                metric_type=MetricType.COUNTER,
                aggregation=AggregationModes.ALL)
        )
        cardinal_sampler = metric.labels()
        with self.subTest(name="default_timestamp"):
            total = 0
            for i in range(5):
                v = random.uniform(0, 50)
                total += v
                cardinal_sampler.inc(v)
                self.assertEqual(total, cardinal_sampler.get()[i][1])
        cardinal_sampler = metric.labels(label1='explicit_timestamp')
        with self.subTest(name="explicit_timestamp"):
            total = 0
            for i in range(5):
                v = random.uniform(0, 50)
                total += v
                ts = time.time_ns()
                cardinal_sampler.inc(v, ts)
                self.assertEqual((ts, total), cardinal_sampler.get()[i])
        with self.subTest(name="maxlen"):
            cardinal_sampler = self.metric_pool.get_or_create(
                name='maxlen', documentation='Documentation maxlen',
                labels_w_default={'label1': 'default'},
                requirements=Requirements(
                    metric_type=MetricType.COUNTER,
                    aggregation=AggregationModes.ALL,
                    max_samples=16)
            ).labels(label1='maxlen')
            for i in range(32):
                cardinal_sampler.inc()
                self.assertEqual((i+1) if i < 16 else 16, len(cardinal_sampler.get()))
        with self.subTest(name="expect_raises"):
            with self.assertRaises(ValueError):
                cardinal_sampler.inc(-1)
