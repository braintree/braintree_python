import httplib
import base64
from braintree.configuration import Configuration
from braintree.util.xml_util import XmlUtil
from braintree.exceptions.authentication_error import AuthenticationError
from braintree.exceptions.authorization_error import AuthorizationError
from braintree.exceptions.down_for_maintenance_error import DownForMaintenanceError
from braintree.exceptions.not_found_error import NotFoundError
from braintree.exceptions.server_error import ServerError
from braintree.exceptions.unexpected_error import UnexpectedError
from braintree.exceptions.upgrade_required_error import UpgradeRequiredError
from braintree import version

class Http(object):
    @staticmethod
    def is_error_status(status):
        return status not in [200, 201, 422]

    @staticmethod
    def raise_exception_from_status(status, message=None):
        if status == 401:
            raise AuthenticationError()
        elif status == 403:
            raise AuthorizationError(message)
        elif status == 404:
            raise NotFoundError()
        elif status == 426:
            raise UpgradeRequiredError()
        elif status == 500:
            raise ServerError()
        elif status == 503:
            raise DownForMaintenanceError()
        else:
            raise UnexpectedError("Unexpected HTTP_RESPONSE " + str(status))

    def __init__(self, config):
        self.config = config
        self.environment = self.config.environment

    def post(self, path, params={}):
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
            self.config.base_merchant_path() + path,
            XmlUtil.xml_from_dict(params) if params else '',
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
        return "Basic " + base64.encodestring(self.config.public_key + ":" + self.config.private_key).strip()

    def __headers(self):
        return {
            "Accept": "application/xml",
            "Authorization": self.__authorization_header(),
            "Content-type": "application/xml",
            "User-Agent": "Braintree Python " + version.Version,
            "X-ApiVersion": Configuration.api_version()
        }

    def __verify_ssl(self):
        if Configuration.use_unsafe_ssl: return

        try:
            import pycurl
        except ImportError, e:
            print "Cannot load PycURL.  Please refer to Braintree documentation."
            print """
If you are in an environment where you absolutely cannot load PycURL
(such as Google App Engine), you can turn off SSL Verification by setting:

    Configuration.use_unsafe_ssl = True

This is highly discouraged, however, since it leaves you susceptible to
man-in-the-middle attacks."""
            raise e

        curl = pycurl.Curl()
        # see http://curl.haxx.se/libcurl/c/curl_easy_setopt.html for info on these options
        curl.setopt(pycurl.CAINFO, self.environment.ssl_certificate)
        curl.setopt(pycurl.ENCODING, 'gzip')
        curl.setopt(pycurl.SSL_VERIFYPEER, 1)
        curl.setopt(pycurl.SSL_VERIFYHOST, 2)
        curl.setopt(pycurl.NOBODY, 1)
        curl.setopt(pycurl.NOSIGNAL, 1)
        curl.setopt(pycurl.URL, self.environment.protocol + self.environment.server_and_port)
        curl.perform()
