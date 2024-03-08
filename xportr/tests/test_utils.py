import unittest
import string
from ..xportr.utils import (
    float_to_go_string,
)


class GeneratorTest(unittest.TestCase):
    def test_float_to_go_string(self) -> None:
        self.assertEqual(float_to_go_string(float("Inf")), "+Inf")
