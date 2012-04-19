try:
    import requests
except ImportError:
    pass

class RequestsStrategy(object):
    def __init__(self, config, environment):
        self.config = config
        self.environment = environment

    def http_do(self, http_verb, path, headers, request_body):
        response = self.__request_function(http_verb)(
            self.environment.base_url + path,
            headers=headers,
            data=request_body,
            verify=self.environment.ssl_certificate
        )

        return [response.status_code, response.text]

    def __request_function(self, method):
        if method == "GET":
            return requests.get
        elif method == "POST":
            return requests.post
        elif method == "PUT":
            return requests.put
        elif method == "DELETE":
            return requests.delete
