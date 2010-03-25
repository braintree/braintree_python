import os
import inspect

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

    @staticmethod
    def braintree_root():
        return os.path.dirname(inspect.getfile(Environment))

Environment.Development = Environment("localhost", os.getenv("GATEWAY_PORT") or "3000", False, None)
Environment.Sandbox = Environment("sandbox.braintreegateway.com", "443", True, Environment.braintree_root() + "/ssl/valicert_ca.crt")
Environment.Production = Environment("www.braintreegateway.com", "443", True, Environment.braintree_root() + "/ssl/securetrust_ca.crt")
