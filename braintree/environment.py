import os
import inspect
from braintree.exceptions.configuration_error import ConfigurationError

class Environment(object):
    """
    A class representing which environment the client library is using.
    Pass in one of the following values as the first argument to
    :class:`braintree.Configuration.configure() <braintree.configuration.Configuration>` ::

        braintree.Environment.Sandbox
        braintree.Environment.Production
    """

    def __init__(self, name, server, port, auth_url, is_ssl, ssl_certificate):
        self.__name__ = name
        self.__server = server
        self.__port = port
        self.is_ssl = is_ssl
        self.ssl_certificate = ssl_certificate
        self.__auth_url = auth_url

    @property
    def base_url(self):
        return "%s%s:%s" % (self.protocol, self.server, self.port)

    @property
    def port(self):
        return int(self.__port)

    @property
    def auth_url(self):
        return self.__auth_url

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
    def parse_environment(environment):
        if isinstance(environment, Environment) or environment is None:
            return environment
        try:
            return Environment.All[environment]
        except KeyError as e:
            raise ConfigurationError("Unable to process supplied environment")

    @staticmethod
    def braintree_root():
        return os.path.dirname(inspect.getfile(Environment))

    def __str__(self):
        return self.__name__

Environment.Development = Environment("development", "localhost", os.getenv("GATEWAY_PORT") or "3000", "http://auth.venmo.dev:9292", False, None)
Environment.QA = Environment("qa", "gateway.qa.braintreepayments.com", "443", "http://auth.qa.venmo.com", True, Environment.braintree_root() + "/ssl/api_braintreegateway_com.ca.crt")
Environment.Sandbox = Environment("sandbox", "api.sandbox.braintreegateway.com", "443", "https://auth.sandbox.venmo.com", True, Environment.braintree_root() + "/ssl/api_braintreegateway_com.ca.crt")
Environment.Production = Environment("production", "api.braintreegateway.com", "443", "https://auth.venmo.com", True, Environment.braintree_root() + "/ssl/api_braintreegateway_com.ca.crt")
Environment.All = {
    "development": Environment.Development,
    "integration": Environment.Development,
    "qa": Environment.QA,
    "sandbox": Environment.Sandbox,
    "production": Environment.Production
}
