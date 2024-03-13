# pylint: disable=duplicate-code
import unittest
import time
from xportr import (
    TimestampedDeque
)


class TestTimestampedDeque(unittest.TestCase):
    def setUp(self):
        self.tsd = TimestampedDeque(
            elems_with_ts=[(time.time_ns(), 'lorem')],
            elems_without_ts=['ipsum', 'dolor'],
            maxlen=10, ttl=2)

    def test_expiration(self) -> None:
        with self.subTest(name="new_list_from_non_expired"):
            alive_dq = self.tsd.get_all_non_expired()
            self.assertEqual(len(alive_dq), len(self.tsd))
            self.assertIsNot(self.tsd, alive_dq)
        with self.subTest(name="wait_for_expiration"):
            time.sleep(2)
            self.tsd.ts_append('amet')
            self.tsd = self.tsd.get_all_non_expired()
            self.assertEqual(len(self.tsd), 1)
            self.assertIs(self.tsd[0][1], 'amet')

    def test_maxlen(self) -> None:
        self.tsd = TimestampedDeque(
            elems_with_ts=[(time.time_ns(), 'lorem')],
            elems_without_ts=['ipsum', 'dolor'],
            maxlen=15, ttl=2)
        with self.subTest(name="length"):
            self.tsd.ts_extend(
                [chr(i) for i in range(ord('a'), ord('a')+20)]
            )
            self.assertEqual(len(self.tsd), 15)
        with self.subTest(name="most_recent_elems"):
            self.tsd.ts_extend(['most', 'recent'])
            self.assertIs(self.tsd.pop()[1], 'recent')

    def test_manipulation(self) -> None:
        with self.subTest(name="ts_extend"):
            original_len = len(self.tsd)
            self.tsd.ts_extend(['sit'])
            self.assertGreater(len(self.tsd), original_len)
        with self.subTest(name="ts_append"):
            original_len = len(self.tsd)
            self.tsd.ts_append('amet')
            self.assertGreater(len(self.tsd), original_len)
