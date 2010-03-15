import httplib
import base64
import string
from braintree.configuration import Configuration
from braintree.util.xml_util import XmlUtil

class Http:
    def post(self, path, params):
        return self.__http_do("POST", path, params)

    def __http_do(self, http_verb, path, params):
        if Configuration.ssl():
            connection_type = httplib.HTTPSConnection
        else:
            connection_type = httplib.HTTPConnection

        conn = connection_type(Configuration.server_and_port())
        conn.request(http_verb, Configuration.base_merchant_path() + path, XmlUtil.xml_from_dict(params), self.__headers())
        response = conn.getresponse()
        if response.status in [200, 201]:
            data = response.read()
            return XmlUtil.dict_from_xml(data)

    def __authorization_header(self):
        return "Basic " + base64.encodestring(Configuration.public_key + ":" + Configuration.private_key).strip()

    def __headers(self):
        return {
            "Content-type": "application/xml",
            "Accept": "application/xml",
            "Authorization": self.__authorization_header(),
            "User-Agent": "Braintree Python 1.0.0",
            "X-ApiVersion": "1"
        }

