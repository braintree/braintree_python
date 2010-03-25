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

    def __init__(self, environment=None):
        if environment == None:
            environment = Configuration.environment
        self.environment = environment

    def post(self, path, params):
        return self.__http_do("POST", path, params)

    def delete(self, path):
        return self.__http_do("DELETE", path)

    def get(self, path):
        return self.__http_do("GET", path)

    def put(self, path, params={}):
        return self.__http_do("PUT", path, params)

    def __http_do(self, http_verb, path, params=None):
        if self.environment.is_ssl:
            self.__verify_ssl()
            conn = httplib.HTTPSConnection(self.environment.server, self.environment.port)
        else:
            conn = httplib.HTTPConnection(self.environment.server, self.environment.port)

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

    def __verify_ssl(self):
        if not Configuration.use_unsafe_ssl:
            try:
                from M2Crypto import SSL
            except ImportError, e:
                print "Cannot load M2Crypto.  Please refer to Braintree documentation."
                print """
If you are in an environment where you absolutely cannot load M2Crypto
(such as Google App Engine), you can turn off SSL Verification by setting:

    Configuration.use_unsafe_ssl = True

This is highly discouraged, however, since it leaves you susceptible to
man-in-the-middle attacks."""
                raise e

            ctx = SSL.Context()
            ctx.set_verify(SSL.verify_peer | SSL.verify_fail_if_no_peer_cert, depth=9)
            ctx.load_verify_locations(self.environment.ssl_certificate)
            s = SSL.Connection(ctx)
            s.connect((self.environment.server, self.environment.port))
