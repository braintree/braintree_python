import unittest
from datetime import date, datetime, timedelta, timezone

from braintree.util.xml_util import XmlUtil


class TestGeneratorTimezones(unittest.TestCase):
    def test_positive_offset_preserves_instant_across_date_boundary(self):
        value = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone(timedelta(hours=5, minutes=30)))
        xml = XmlUtil.xml_from_dict({"created_at": value})
        self.assertEqual('<created_at type="datetime">2026-01-01T21:34:05Z</created_at>', xml)
        self.assertEqual({"created_at": datetime(2026, 1, 1, 21, 34, 5)}, XmlUtil.dict_from_xml(xml))

    def test_negative_offset_preserves_instant(self):
        value = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone(timedelta(hours=-7)))
        xml = XmlUtil.xml_from_dict({"created_at": value})
        self.assertEqual('<created_at type="datetime">2026-01-02T10:04:05Z</created_at>', xml)
        self.assertEqual({"created_at": datetime(2026, 1, 2, 10, 4, 5)}, XmlUtil.dict_from_xml(xml))

    def test_utc_keeps_existing_output(self):
        value = datetime(2026, 1, 2, 3, 4, 5, tzinfo=timezone.utc)
        self.assertEqual('<value type="datetime">2026-01-02T03:04:05Z</value>', XmlUtil.xml_from_dict({"value": value}))

    def test_naive_datetime_keeps_existing_output(self):
        value = datetime(2026, 1, 2, 3, 4, 5)
        self.assertEqual('<value type="datetime">2026-01-02T03:04:05Z</value>', XmlUtil.xml_from_dict({"value": value}))

    def test_date_keeps_existing_output(self):
        self.assertEqual('<value type="datetime">2026-01-02T00:00:00Z</value>', XmlUtil.xml_from_dict({"value": date(2026, 1, 2)}))
