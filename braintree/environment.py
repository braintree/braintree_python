import os

class Environment(object):
    def __init__(self, server, port, is_ssl):
        self.server = server
        self.port = port
        self.is_ssl = is_ssl

    @property
    def server_and_port(self):
        return self.server + ":" + self.port

Environment.DEVELOPMENT = Environment("localhost", os.getenv("GATEWAY_PORT") or '3000', False)
Environment.SANDBOX = Environment("sandbox.braintreegateway.com", '443', True)
Environment.PRODUCTION = Environment("www.braintreegateway.com", '443', True)
