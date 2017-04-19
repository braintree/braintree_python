import unittest
from braintree.util.datetime_parser import parse_datetime
from datetime import datetime


class TestDateParser(unittest.TestCase):
    def test_parses_with_zulu_and_symbols(self):
        result = parse_datetime('2017-04-19T18:51:21Z')
        self.assertEqual(result, datetime(2017, 4, 19, 18, 51, 21))

    def test_parses_with_zulu_and_no_symbols(self):
        result = parse_datetime('20170419T185121Z')
        self.assertEqual(result, datetime(2017, 4, 19, 18, 51, 21))

    def test_parses_with_zero_offset(self):
        result = parse_datetime('2017-04-19T18:51:21+00:00')
        self.assertEqual(result, datetime(2017, 4, 19, 18, 51, 21))

    def test_parses_with_negative_offset(self):
        result = parse_datetime('2017-04-19T18:51:21-01:30')
        self.assertEqual(result, datetime(2017, 4, 19, 20, 21, 21))

    def test_parses_with_positive_offset(self):
        result = parse_datetime('2017-04-19T18:51:21+07:00')
        self.assertEqual(result, datetime(2017, 4, 19, 11, 51, 21))

    def test_raises_with_bad_input(self):
        with self.assertRaises(ValueError):
            parse_datetime('20170420')
        with self.assertRaises(ValueError):
            parse_datetime('20170420Z')
