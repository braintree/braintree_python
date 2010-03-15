import httplib
from braintree.configuration import Configuration
from braintree.util.xml_util import XmlUtil

class Http:
    def post(self, path, params):
        response = self.__http_do("GET", path, params)
        return XmlUtil.dict_from_xml(response)

    def __http_do(self, http_verb, path, params):
        if Configuration.ssl:
            connection_type = httplib.HTTPSConnection
        else:
            connection_type = httplib.HTTPConnection

        conn = connection_type(Configuration.server_and_port())
        body = XmlUtil.xml_from_dict(params)
        print(body)
        conn.request(http_verb, Configuration.base_merchant_path() + path, body, self.__headers())

    def __headers(self):
        return {
            "Content-type": "application/xml",
            "Accept": "application/xml"
        }

