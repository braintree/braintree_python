import unittest
from braintree.util.xml_util import XmlUtil

class TestXmlUtil(unittest.TestCase):
    def test_dict_from_xml_simple(self):
        xml = """
        <container>val</container>
        """
        expected = {"container": "val"}
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

    def test_xml_from_dict_simple(self):
        dict = {"a": "b"}
        self.assertEqual(dict, self.__xml_and_back(dict))

    def __xml_and_back(self, dict):
        XmlUtil.dict_from_xml(XmlUtil.xml_from_dict(dict))
