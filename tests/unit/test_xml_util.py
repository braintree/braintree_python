from tests.test_helper import *

class TestXmlUtil(unittest.TestCase):
    def test_dict_from_xml_simple(self):
        xml = """
        <container>val</container>
        """
        expected = {"container": "val"}
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_dict_from_xml_typecasts_ints(self):
        xml = """
        <container type="integer">1</container>
        """
        expected = {"container": 1}
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_dict_from_xml_typecasts_nils(self):
        xml = """
        <root>
          <a_nil_value nil="true"></a_nil_value>
          <an_empty_string></an_empty_string>
        </root>
        """
        expected = {"root": {"a_nil_value": None, "an_empty_string": ""}}
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_dict_from_xml_typecasts_booleans(self):
        xml = """
        <root>
          <casted-true type="boolean">true</casted-true>
          <casted-one type="boolean">1</casted-one>
          <casted-false type="boolean">false</casted-false>
          <casted-anything type="boolean">anything</casted-anything>
          <uncasted-true>true</uncasted-true>
        </root>
        """
        expected = {
            "root": {
                "casted_true": True,
                "casted_one": True,
                "casted_false": False,
                "casted_anything": False,
                "uncasted_true": "true"
            }
        }
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_dict_from_xml_typecasts_datetimes(self):
        xml = """
        <root>
          <created-at type="datetime">2009-10-28T10:19:49Z</created-at>
        </root>
        """
        expected = {"root": {"created_at": datetime(2009, 10, 28, 10, 19, 49)}}
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_dict_from_xml_with_dashes(self):
        xml = """
        <my-item>val</my-item>
        """
        expected = {"my_item": "val"}
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_dict_from_xml_nested(self):
        xml = """
        <container>
            <elem>val</elem>
        </container>
        """
        expected = {"container": {"elem": "val"}}
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_dict_from_xml_array(self):
        xml = """
        <container>
            <elements type="array">
                <elem>val1</elem>
                <elem>val2</elem>
                <elem>val3</elem>
            </elements>
        </container>
        """
        expected = {"container": {"elements": ["val1", "val2", "val3"]}}
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_dict_from_xml_with_empty_array(self):
        xml = """
        <container>
            <elements type="array" />
        </container>
        """
        expected = {"container": {"elements": []}}
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_dict_from_xml_array_of_hashes(self):
        xml = """
        <container>
            <elements type="array">
                <elem><val>val1</val></elem>
                <elem><val>val2</val></elem>
                <elem><val>val3</val></elem>
            </elements>
        </container>
        """
        expected = {"container": {"elements": [{"val": "val1"}, {"val": "val2"}, {"val": "val3"}]}}
        self.assertEqual(expected, XmlUtil.dict_from_xml(xml))

    def test_xml_from_dict_escapes_keys_and_values(self):
        test_dict = {"k<ey": "va&lue"}
        self.assertEqual("<k&lt;ey>va&amp;lue</k&lt;ey>", XmlUtil.xml_from_dict(test_dict))

    def test_xml_from_dict_escapes_keys_list(self):
        test_dict = {"k<ey": []}
        self.assertEqual("<k&lt;ey type=\"array\"></k&lt;ey>", XmlUtil.xml_from_dict(test_dict))

    def test_xml_from_dict_escapes_keys_bool(self):
        test_dict = {"k<ey": True}
        self.assertEqual("<k&lt;ey type=\"boolean\">true</k&lt;ey>", XmlUtil.xml_from_dict(test_dict))

    def test_xml_from_dict_escapes_keys_int(self):
        test_dict = {"k<ey": 10}
        self.assertEqual("<k&lt;ey type=\"integer\">10</k&lt;ey>", XmlUtil.xml_from_dict(test_dict))

    def test_xml_from_dict_escapes_keys_datetime(self):
        test_dict = {"k<ey": datetime(2023, 1, 2, 3, 4, 5)}
        self.assertEqual("<k&lt;ey type=\"datetime\">2023-01-02T03:04:05Z</k&lt;ey>", XmlUtil.xml_from_dict(test_dict))

    def test_xml_from_dict_with_xml_injection(self):
        test_dict = {"<merchant-account-id>12345</merchant-account-id>": []}
        self.assertEqual("<&lt;merchant-account-id&gt;12345&lt;/merchant-account-id&gt; type=\"array\"></&lt;merchant-account-id&gt;12345&lt;/merchant-account-id&gt;>", XmlUtil.xml_from_dict(test_dict))

    def test_xml_from_dict_simple(self):
        test_dict = {"a": "b"}
        self.assertEqual(test_dict, self.__xml_and_back(test_dict))

    def test_xml_from_dict_with_integer(self):
        test_dict = {"a": 1}
        self.assertEqual('<a type="integer">1</a>', XmlUtil.xml_from_dict(test_dict))

    def test_xml_from_dict_with_long(self):
        test_dict = {"a": 12341234123412341234}
        self.assertEqual('<a type="integer">12341234123412341234</a>', XmlUtil.xml_from_dict(test_dict))

    def test_xml_from_dict_with_boolean(self):
        test_dict = {"a": True}
        self.assertEqual(test_dict, self.__xml_and_back(test_dict))

    def test_xml_from_dict_simple_xml_and_back_twice(self):
        test_dict = {"a": "b"}
        self.assertEqual(test_dict, self.__xml_and_back(self.__xml_and_back(test_dict)))

    def test_xml_from_dict_nested(self):
        test_dict = {"container": {"item": "val"}}
        self.assertEqual(test_dict, self.__xml_and_back(test_dict))

    def test_xml_from_dict_with_array(self):
        test_dict = {"container": {"elements": ["val1", "val2", "val3"]}}
        self.assertEqual(test_dict, self.__xml_and_back(test_dict))

    def test_xml_from_dict_with_array_of_hashes(self):
        test_dict = {"container": {"elements": [{"val": "val1"}, {"val": "val2"}, {"val": "val3"}]}}
        self.assertEqual(test_dict, self.__xml_and_back(test_dict))

    def test_xml_from_dict_retains_underscores(self):
        test_dict = {"container": {"my_element": "val"}}
        self.assertEqual(test_dict, self.__xml_and_back(test_dict))

    def test_xml_from_dict_escapes_special_chars(self):
        test_dict = {"container": {"element": "<&>'\""}}
        self.assertEqual(test_dict, self.__xml_and_back(test_dict))

    def test_xml_from_dict_with_datetime(self):
        test_dict = {"a": datetime(2010, 1, 2, 3, 4, 5)}
        self.assertEqual(test_dict, self.__xml_and_back(test_dict))

    def test_xml_from_dict_with_unicode_characters(self):
        test_dict = {"a": u"\u1f61hat?"}
        self.assertEqual('<a>&#8033;hat?</a>', XmlUtil.xml_from_dict(test_dict))

    def test_xml_from_dict_with_dates_formats_as_datetime(self):
        test_dict = {"a": date(2010, 1, 2)}
        self.assertEqual('<a type="datetime">2010-01-02T00:00:00Z</a>', XmlUtil.xml_from_dict(test_dict))

    @staticmethod
    def __xml_and_back(test_dict):
        return XmlUtil.dict_from_xml(XmlUtil.xml_from_dict(test_dict))
