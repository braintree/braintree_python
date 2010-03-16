import httplib
import base64
import string
from braintree.configuration import Configuration
from braintree.util.xml_util import XmlUtil
from braintree.exceptions.authentication_error import AuthenticationError
from braintree.exceptions.authorization_error import AuthorizationError
from braintree.exceptions.down_for_maintenance_error import DownForMaintenanceError
from braintree.exceptions.not_found_error import NotFoundError
from braintree.exceptions.server_error import ServerError
from braintree.exceptions.unexpected_error import UnexpectedError

class Http(object):
    def post(self, path, params):
        return self.__http_do("POST", path, params)

    def __http_do(self, http_verb, path, params):
        if Configuration.is_ssl():
            connection_type = httplib.HTTPSConnection
        else:
            connection_type = httplib.HTTPConnection

        conn = connection_type(Configuration.server_and_port())
        conn.request(http_verb, Configuration.base_merchant_path() + path, XmlUtil.xml_from_dict(params), self.__headers())
        response = conn.getresponse()
        status = response.status

        if status in [200, 201, 422]:
            data = response.read()
            conn.close()
            return XmlUtil.dict_from_xml(data)
        else:
            conn.close()
            __raise_exception_from_status(status)

    def __authorization_header(self):
        return "Basic " + base64.encodestring(Configuration.public_key + ":" + Configuration.private_key).strip()

    def __headers(self):
        return {
            "Accept": "application/xml",
            "Authorization": self.__authorization_header(),
            "Content-type": "application/xml",
            "User-Agent": "Braintree Python 1.0.0",
            "X-ApiVersion": "1"
        }

    def __raise_exception_from_status(self, status):
        if status == 401:
            raise AuthenticationError()
        elif status == 403:
            raise AuthorizationError()
        elif status == 404:
            raise NotFoundError()
        elif status == 500:
            raise ServerError()
        elif status == 503:
            raise DownForMaintenanceError()
        else:
            raise UnexpectedError("Unexpected HTTP_RESPONSE " + str(status))

