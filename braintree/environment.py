import os

class Environment(object):
    def __init__(self, server, port, is_ssl, ssl_certificate):
        self.__server = server
        self.__port = port
        self.is_ssl = is_ssl
        self.ssl_certificate = ssl_certificate

    @property
    def port(self):
        return int(self.__port)

    @property
    def protocol(self):
        return self.__port == "443" and "https://" or "http://"

    @property
    def server(self):
        return self.__server

    @property
    def server_and_port(self):
        return self.__server + ":" + self.__port

Environment.DEVELOPMENT = Environment("localhost", os.getenv("GATEWAY_PORT") or "3000", False, None)
Environment.SANDBOX = Environment("sandbox.braintreegateway.com", "443", True, "braintree/ssl/valicert_ca.crt")
Environment.PRODUCTION = Environment("www.braintreegateway.com", "443", True, "braintree/ssl/securetrust_ca.crt")
