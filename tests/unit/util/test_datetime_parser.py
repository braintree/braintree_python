import unittest
from braintree.util.datetime_parser import parse_datetime as parse
from datetime import datetime


class TestDateParser(unittest.TestCase):
    def test_parses_with_zulu_and_symbols(self):
        self.assertEqual(parse('2017-04-19T18:51:21Z'), datetime(2017, 4, 19, 18, 51, 21))
        self.assertEqual(parse('2017-04-19T18:51:21.45Z'), datetime(2017, 4, 19, 18, 51, 21, 450000))

    def test_parses_with_zulu_and_no_symbols(self):
        self.assertEqual(parse('20170419T185121Z'), datetime(2017, 4, 19, 18, 51, 21))
        self.assertEqual(parse('20170419T185121.123Z'), datetime(2017, 4, 19, 18, 51, 21, 123000))

    def test_parses_with_zero_offset(self):
        self.assertEqual(parse('2017-04-19T18:51:21+00:00'), datetime(2017, 4, 19, 18, 51, 21))
        self.assertEqual(parse('2017-04-19T18:51:21.420+00:00'), datetime(2017, 4, 19, 18, 51, 21, 420000))

    def test_parses_with_negative_offset(self):
        self.assertEqual(parse('2017-04-19T18:51:21-01:30'), datetime(2017, 4, 19, 20, 21, 21))
        self.assertEqual(parse('2017-04-19T18:51:21.987-01:30'), datetime(2017, 4, 19, 20, 21, 21, 987000))

    def test_parses_with_positive_offset(self):
        self.assertEqual(parse('2017-04-19T18:51:21+07:00'), datetime(2017, 4, 19, 11, 51, 21))
        self.assertEqual(parse('2017-04-19T18:51:21.765+07:00'), datetime(2017, 4, 19, 11, 51, 21, 765000))

    def test_raises_with_bad_input(self):
        with self.assertRaises(ValueError):
            parse('20170420')
        with self.assertRaises(ValueError):
            parse('20170420Z')
