import copy
import importlib
import os
import unittest

# Choose implementation: BOOKING_MODULE=booking_v1 python test_booking.py
can_book = importlib.import_module(os.environ.get("BOOKING_MODULE", "booking")).can_book

NOW = 540
EXISTING = [(600, 660)]


class TestAcceptanceCriteria(unittest.TestCase):
    def test_touching_end_is_available(self):          # AC4
        self.assertTrue(can_book(660, 720, NOW, False, EXISTING))

    def test_touching_start_is_available(self):        # AC4
        self.assertTrue(can_book(540 + 1, 600, NOW, False, EXISTING))

    def test_overlap_is_unavailable(self):             # AC4
        self.assertFalse(can_book(630, 690, NOW, False, EXISTING))

    def test_booking_inside_existing(self):            # AC4
        self.assertFalse(can_book(610, 650, NOW, False, EXISTING))

    def test_booking_contains_existing(self):          # AC4
        self.assertFalse(can_book(590, 670, NOW, False, EXISTING))

    def test_blocked_rejects_all(self):                # AC3
        self.assertFalse(can_book(660, 720, NOW, True, EXISTING))

    def test_exactly_120_allowed(self):                # AC2
        self.assertTrue(can_book(720, 840, NOW, False, EXISTING))

    def test_121_rejected(self):                       # AC2
        self.assertFalse(can_book(720, 841, NOW, False, EXISTING))

    def test_starts_now_rejected(self):                # AC1
        self.assertFalse(can_book(540, 570, NOW, False, EXISTING))

    def test_starts_one_minute_after_now(self):        # AC1
        self.assertTrue(can_book(541, 570, NOW, False, []))

    def test_starts_before_now_rejected(self):         # AC1
        self.assertFalse(can_book(500, 530, NOW, False, []))

    def test_reversed_times(self):                     # AC1
        self.assertFalse(can_book(700, 650, NOW, False, []))

    def test_zero_length(self):                        # AC1
        self.assertFalse(can_book(700, 700, NOW, False, []))

    def test_day_bounds(self):                         # AC1
        self.assertFalse(can_book(-1, 30, NOW, False, []))
        self.assertFalse(can_book(1400, 1441, NOW, False, []))
        self.assertTrue(can_book(1380, 1440, NOW, False, []))
        self.assertTrue(can_book(1, 60, 0, False, []))

    def test_multiple_bookings(self):                  # AC4
        ex = [(600, 660), (700, 760), (800, 860)]
        self.assertTrue(can_book(660, 700, NOW, False, ex))
        self.assertFalse(can_book(740, 810, NOW, False, ex))
        self.assertTrue(can_book(860, 900, NOW, False, ex))

    def test_empty_existing(self):                     # AC4
        self.assertTrue(can_book(700, 760, NOW, False, []))

    def test_inputs_unchanged(self):                   # AC5
        ex = [(600, 660), (700, 760)]
        before = copy.deepcopy(ex)
        can_book(630, 690, NOW, False, ex)
        can_book(660, 700, NOW, False, ex)
        self.assertEqual(ex, before)

    def test_returns_bool(self):
        self.assertIs(can_book(660, 720, NOW, False, EXISTING), True)
        self.assertIs(can_book(630, 690, NOW, False, EXISTING), False)

    def test_non_integer_times_rejected(self):         # AC1
        self.assertFalse(can_book(600.5, 660, NOW, False, []))
        self.assertFalse(can_book(True, 660, NOW, False, []))
        self.assertFalse(can_book("600", 660, NOW, False, []))


if __name__ == "__main__":
    unittest.main(verbosity=2)
