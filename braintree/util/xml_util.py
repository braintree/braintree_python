from xml.dom import minidom
import re

class XmlUtil:
    @staticmethod
    def xml_from_dict(data):
        pass

    @staticmethod
    def dict_from_xml(xml):
        doc = minidom.parseString("><".join(re.split(">\s+<", xml)).strip())
        xml = XmlUtil()
        xml.document = doc
        return {doc.documentElement.tagName: xml.parse_xml(doc.documentElement)}

    def parse_xml(self, root):
        child = root.firstChild

        if (child.nodeType == minidom.Node.TEXT_NODE):
            return child.nodeValue

        if self.__get_type(root) == "array":
            print("building list")
            return self.__build_list(child)
        else:
            print("building dict")
            return self.__build_dict(child)

    def __build_list(self, child):
        l=[]
        while child is not None:
            if (child.nodeType == minidom.Node.ELEMENT_NODE):
                l.append(self.parse_xml(child))
            child = child.nextSibling
        return l

    def __build_dict(self, child):
        d={}
        while child is not None:
            if (child.nodeType == minidom.Node.ELEMENT_NODE):
                if self.__get_type(child) == "array" or child.firstChild.nodeType == minidom.Node.TEXT_NODE:
                    d[child.tagName] = self.parse_xml(child)
                else:
                    if not self.__get_attribute(d, child.tagName):
                        d[child.tagName] = []

                    d[child.tagName].append(self.parse_xml(child))
            child = child.nextSibling
        return d

    def __get_attribute(self, dict, attribute):
        try:
            return dict[attribute]
        except:
            return None

    def __get_type(self, node):
        type = self.__get_attribute(node.attributes, "type")
        return type and type.value

