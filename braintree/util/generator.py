import datetime
import types
from decimal import Decimal

class Generator(object):
    def __init__(self, dict):
        self.dict = dict

    def generate(self):
        return self.__generate_dict(self.dict)

    def __escape(self, value):
        return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("'", "&apos;").replace("\"", "&quot;");

    def __generate_boolean(self, value):
        return str(value).lower()

    def __generate_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%SZ")

    def __generate_dict(self, dictionary):
        xml = ""
        for key, val in dictionary.iteritems():
            xml += self.__generate_node(key, val)
        return xml

    def __generate_list(self, list):
        xml = ""
        for item in list:
            xml += self.__generate_node("item", item)
        return xml

    def __generate_node(self, key, value):
        open_tag = "<" + self.__escape(key) + ">"
        close_tag = "</" + self.__escape(key) + ">"

        if isinstance(value, unicode):
            return open_tag + self.__escape(value).encode('ascii', 'xmlcharrefreplace') + close_tag
        elif isinstance(value, str):
            return open_tag + self.__escape(value) + close_tag
        elif isinstance(value, Decimal):
            return open_tag + str(value) + close_tag
        elif isinstance(value, dict):
            return open_tag + self.__generate_dict(value) + close_tag
        elif isinstance(value, list):
            open_tag = "<" + key + " type=\"array\">"
            return open_tag + self.__generate_list(value) + close_tag
        elif isinstance(value, bool):
            open_tag = "<" + key + " type=\"boolean\">"
            return open_tag + self.__generate_boolean(value) + close_tag
        elif isinstance(value, (int, long)) and not isinstance(value, bool):
            open_tag = "<" + key + " type=\"integer\">"
            return open_tag + str(value) + close_tag
        elif isinstance(value, types.NoneType):
            return open_tag + close_tag
        elif isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
            open_tag = "<" + key + " type=\"datetime\">"
            return open_tag + self.__generate_datetime(value) + close_tag
        else:
            raise RuntimeError("Unexpected XML node type: " + str(type(value)))
