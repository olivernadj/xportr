# pylint: disable=duplicate-code
import unittest

from xportr import (
    Requirements, MetricType, AggregationModes
)


class TestRequirements(unittest.TestCase):
    def test_requirements(self) -> None:
        for metric_type in MetricType:
            for aggregation_mode in AggregationModes:
                for timestamped in [True, False]:
                    with self.subTest(
                            metric_type=metric_type,
                            aggregation_mode=aggregation_mode,
                            timestamped=timestamped):
                        req = Requirements(
                            metric_type=metric_type,
                            aggregation=aggregation_mode,
                            timestamped=timestamped,
                        )
                        self.assertEqual(req.metric_type, metric_type)
                        self.assertEqual(req.aggregation, aggregation_mode)
                        if req.aggregation == AggregationModes.ALL:
                            self.assertTrue(req.timestamped)
                        if req.aggregation not in [AggregationModes.ALL]:
                            self.assertEqual(1, req.max_samples)
