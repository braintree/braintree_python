import httplib
import socket
from braintree.exceptions.unexpected_error import UnexpectedError
from braintree.exceptions.http.connection_error import ConnectionError
from braintree.exceptions.http.invalid_response_error import InvalidResponseError
from braintree.exceptions.http.timeout_error import TimeoutError

class HttplibStrategy(object):
    def __init__(self, config, environment):
        self.config = config
        self.environment = environment
        self.exception_to_wrap = httplib.HTTPException

    def handle_exception(self, exception):
        if isinstance(exception, httplib.ImproperConnectionState):
            raise ConnectionError(exception.message)
        elif isinstance(exception, httplib.IncompleteRead):
            raise ConnectionError(exception.message)
        elif isinstance(exception, httplib.BadStatusLine):
            raise InvalidResponseError(exception.message)
        elif isinstance(exception, socket.timeout):
            raise TimeoutError(exception.message)
        else:
            raise UnexpectedError(exception.message)

    def http_do(self, http_verb, path, headers, request_body):
        if self.environment.is_ssl:
            conn = httplib.HTTPSConnection(self.environment.server, self.environment.port, timeout=self.config.timeout)
        else:
            conn = httplib.HTTPConnection(self.environment.server, self.environment.port, timeout=self.config.timeout)

        conn.request(http_verb, path, request_body, headers)
        response = conn.getresponse()
        status = response.status
        response_body = response.read()
        conn.close()
        return [status, response_body]
