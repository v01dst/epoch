import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from epoch import parse_input, format_ts
from datetime import timezone, timedelta


class TestParseInput(unittest.TestCase):
    def test_epoch(self):
        self.assertEqual(parse_input("1700000000"), 1700000000)

    def test_iso(self):
        ts = parse_input("2023-11-14T22:13:20Z")
        self.assertEqual(ts, 1700000000)

    def test_date(self):
        ts = parse_input("2023-11-14")
        self.assertIsNotNone(ts)

    def test_invalid(self):
        self.assertIsNone(parse_input("not-a-date"))


class TestFormatTs(unittest.TestCase):
    def test_iso(self):
        out = format_ts(1700000000, "iso", timezone.utc)
        self.assertIn("2023-11-14", out)

    def test_date(self):
        out = format_ts(1700000000, "date", timezone.utc)
        self.assertEqual(out, "2023-11-14")

    def test_relative(self):
        out = format_ts(1700000000, "relative", timezone.utc)
        self.assertTrue(out.endswith("ago") or out.endswith("from now"))


if __name__ == "__main__":
    unittest.main()
