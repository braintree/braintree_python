import httplib
import base64
import socket
import ssl
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
    @staticmethod
    def is_error_status(status):
        return status not in [200, 201, 422]

    @staticmethod
    def raise_exception_from_status(status):
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

    def __init__(self, server_and_port=None, is_ssl=None, cert_file=None):
        self.server_and_port = server_and_port or Configuration.environment.server_and_port
        if is_ssl == None:
            is_ssl = Configuration.environment.is_ssl
        self.is_ssl = is_ssl
        if cert_file == None:
            cert_file = Configuration.environment.cert_file
        self.cert_file = cert_file

    def post(self, path, params):
        return self.__http_do("POST", path, params)

    def delete(self, path):
        return self.__http_do("DELETE", path)

    def get(self, path):
        return self.__http_do("GET", path)

    def put(self, path, params={}):
        return self.__http_do("PUT", path, params)

    def __http_do(self, http_verb, path, params=None):
        if self.is_ssl:
            conn = httplib.HTTPSConnection(self.server_and_port)
            sock = socket.create_connection((conn.host, conn.port), conn.timeout)
            conn.sock = ssl.wrap_socket(sock, ca_certs=self.cert_file, cert_reqs=ssl.CERT_REQUIRED)
        else:
            conn = httplib.HTTPConnection(self.server_and_port)

        conn.request(
            http_verb,
            Configuration.base_merchant_path() + path,
            params and XmlUtil.xml_from_dict(params),
            self.__headers()
        )
        response = conn.getresponse()
        status = response.status

        if Http.is_error_status(status):
            conn.close()
            Http.raise_exception_from_status(status)
        else:
            data = response.read()
            conn.close()
            if len(data.strip()) == 0:
                return {}
            else:
                print data
                return XmlUtil.dict_from_xml(data)

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
