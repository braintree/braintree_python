import httplib

class HttplibStrategy(object):
    def __init__(self, config, environment):
        self.config = config
        self.environment = environment

    def http_do(self, http_verb, path, headers, request_body):
        if self.environment.is_ssl:
            conn = httplib.HTTPSConnection(self.environment.server, self.environment.port)
        else:
            conn = httplib.HTTPConnection(self.environment.server, self.environment.port)

        conn.request(http_verb, path, request_body, headers)
        response = conn.getresponse()
        status = response.status
        response_body = response.read()
        conn.close()
        return [status, response_body]
