import unittest
from ..src.utils import float_to_go_string, validate_metric_name, validate_label_name, validate_label_names


class GeneratorTest(unittest.TestCase):
    def test_float_to_go_string(self) -> None:
        self.assertEqual(float_to_go_string(float("Inf")), "+Inf")

    def test_validate_metric_name(self) -> None:
        with self.subTest(name="valid_names"):
            valid_names = ['metric_name', 'metric_123', 'MetricName', 'metric:name']
            for name in valid_names:
                with self.subTest(name=name):
                    self.assertIsNone(validate_metric_name(name))

        with self.subTest(name="invalid_names"):
            invalid_names = ['1metric', '$metric', 'metric name', 'metric-name']
            for name in invalid_names:
                with self.subTest(name=name):
                    with self.assertRaises(ValueError):
                        validate_metric_name(name)

    def test_validate_label_name(self) -> None:
        with self.subTest(name="valid_labels"):
            valid_labels = ['label', 'label_123', 'LabelName']
            for label in valid_labels:
                with self.subTest(label=label):
                    self.assertIsNone(validate_label_name(label))

        with self.subTest(name="invalid_labels"):
            invalid_labels = ['1label', '$label', 'label name', 'label-name', 'label:name']
            for label in invalid_labels:
                with self.subTest(label=label):
                    with self.assertRaises(ValueError):
                        validate_label_name(label)

        with self.subTest(name="reserved_labels"):
            reserved_labels = ['__reserved', '__another_reserved']
            for label in reserved_labels:
                with self.subTest(label=label):
                    with self.assertRaises(ValueError):
                        validate_label_name(label)

    def test_validate_label_names(self) -> None:
        with self.subTest(name="valid_labels"):
            valid_labels = {'label1': 'value1', 'label2': 'value2'}
            self.assertIsNone(validate_label_names(valid_labels))

        with self.subTest(name="invalid_labels"):
            invalid_labels = {'1label': 'value1', '$label': 'value2', 'label-name': 'value3'}
            with self.assertRaises(ValueError):
                validate_label_names(invalid_labels)
