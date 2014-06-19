try:
    import requests
    from braintree.exceptions.unexpected_error import UnexpectedError
    from braintree.exceptions.http.connection_error import ConnectionError
    from braintree.exceptions.http.invalid_response_error import InvalidResponseError
    from braintree.exceptions.http.timeout_error import TimeoutError
except ImportError:
    pass

class RequestsStrategy(object):
    def __init__(self, config, environment):
        self.config = config
        self.environment = environment

    def handle_exception(self, exception):
        if isinstance(exception, requests.exceptions.ConnectionError):
            raise ConnectionError(exception.message)
        elif isinstance(exception, requests.exceptions.HTTPError):
            raise InvalidResponseError(exception.message)
        elif isinstance(exception, requests.exceptions.Timeout):
            raise TimeoutError(exception.message)
        else:
            raise UnexpectedError(exception.message)

    def http_do(self, http_verb, path, headers, request_body):
        response = requests.request(
            http_verb,
            self.environment.base_url + path,
            headers=headers,
            data=request_body,
            verify=self.environment.ssl_certificate,
            timeout=self.config.timeout
        )

        return [response.status_code, response.text]
