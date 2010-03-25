import types
from decimal import Decimal

class Generator(object):
    def __init__(self, dict):
        self.dict = dict

    def generate(self):
        return self.__generate_dict(self.dict)

    def __generate_boolean(self, value):
        return str(value).lower()

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
        open_tag = "<" + key + ">"
        close_tag = "</" + key + ">"

        if type(value) == str or type(value) == unicode:
            return open_tag + value + close_tag
        elif type(value) == Decimal:
            return open_tag + str(value) + close_tag
        elif type(value) == int:
            open_tag = "<" + key + " type=\"integer\">"
            return open_tag + str(value) + close_tag
        elif type(value) == dict:
            return open_tag + self.__generate_dict(value) + close_tag
        elif type(value) == list:
            open_tag = "<" + key + " type=\"array\">"
            return open_tag + self.__generate_list(value) + close_tag
        elif type(value) == bool:
            open_tag = "<" + key + " type=\"boolean\">"
            return open_tag + self.__generate_boolean(value) + close_tag
        elif type(value) == types.NoneType:
            return open_tag + close_tag
        else:
            raise RuntimeError("Unexpected XML node type: " + str(type(value)))
