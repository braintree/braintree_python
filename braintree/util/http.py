import sys
import requests
if sys.version_info[0] == 2:
    from base64 import encodestring as encodebytes
else:
    from base64 import encodebytes
import braintree
from braintree import version
from braintree.util.xml_util import XmlUtil
from braintree.exceptions.authentication_error import AuthenticationError
from braintree.exceptions.authorization_error import AuthorizationError
from braintree.exceptions.down_for_maintenance_error import DownForMaintenanceError
from braintree.exceptions.not_found_error import NotFoundError
from braintree.exceptions.server_error import ServerError
from braintree.exceptions.too_many_requests_error import TooManyRequestsError
from braintree.exceptions.unexpected_error import UnexpectedError
from braintree.exceptions.upgrade_required_error import UpgradeRequiredError
from braintree.exceptions.unexpected_error import UnexpectedError
from braintree.exceptions.http.connection_error import ConnectionError
from braintree.exceptions.http.invalid_response_error import InvalidResponseError
from braintree.exceptions.http.timeout_error import TimeoutError

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
        elif status == 429:
            raise TooManyRequestsError()
        elif status == 500:
            raise ServerError()
        elif status == 503:
            raise DownForMaintenanceError()
        else:
            raise UnexpectedError("Unexpected HTTP_RESPONSE " + str(status))

    def __init__(self, config, environment=None):
        self.config = config
        self.environment = environment or self.config.environment

    def post(self, path, params={}):
        return self.__http_do("POST", path, params)

    def delete(self, path):
        return self.__http_do("DELETE", path)

    def get(self, path):
        return self.__http_do("GET", path)

    def put(self, path, params={}):
        return self.__http_do("PUT", path, params)

    def __http_do(self, http_verb, path, params=None):
        http_strategy = self.config.http_strategy()
        request_body = XmlUtil.xml_from_dict(params) if params else ''

        full_path = path if path.startswith(self.config.base_url()) else (self.config.base_url() + path)

        try:
            status, response_body = http_strategy.http_do(http_verb, full_path, self.__headers(), request_body)
        except Exception as e:
            if self.config.wrap_http_exceptions:
                http_strategy.handle_exception(e)
            else:
                raise

        if Http.is_error_status(status):
            Http.raise_exception_from_status(status)
        else:
            if len(response_body.strip()) == 0:
                return {}
            else:
                return XmlUtil.dict_from_xml(response_body)

    def http_do(self, http_verb, path, headers, request_body):
        response = self.__request_function(http_verb)(
            path if path.startswith(self.config.base_url()) else self.config.base_url() + path,
            headers=headers,
            data=request_body,
            verify=self.environment.ssl_certificate,
            timeout=self.config.timeout
        )

        return [response.status_code, response.text]

    def handle_exception(self, exception):
        if isinstance(exception, requests.exceptions.ConnectionError):
            raise ConnectionError(exception)
        elif isinstance(exception, requests.exceptions.HTTPError):
            raise InvalidResponseError(exception)
        elif isinstance(exception, requests.exceptions.Timeout):
            raise TimeoutError(exception)
        else:
            raise UnexpectedError(exception)

    def __request_function(self, method):
        if method == "GET":
            return requests.get
        elif method == "POST":
            return requests.post
        elif method == "PUT":
            return requests.put
        elif method == "DELETE":
            return requests.delete

    def __authorization_header(self):
        if self.config.has_client_credentials():
            return b"Basic " + encodebytes(
                        self.config.client_id.encode('ascii') +
                        b":" +
                        self.config.client_secret.encode('ascii')
                    ).replace(b"\n", b"").strip()
        elif self.config.has_access_token():
            return b"Bearer " + self.config.access_token.encode('ascii')
        else:
            return b"Basic " + encodebytes(
                        self.config.public_key.encode('ascii') +
                        b":" +
                        self.config.private_key.encode('ascii')
                    ).replace(b"\n", b"").strip()

    def __headers(self):
        return {
            "Accept": "application/xml",
            "Authorization": self.__authorization_header(),
            "Content-type": "application/xml",
            "User-Agent": "Braintree Python " + version.Version,
            "X-ApiVersion": braintree.configuration.Configuration.api_version()
        }

