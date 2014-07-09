import os
import sys
import braintree

class Configuration(object):
    """
    A class representing the configuration of your Braintree account.
    You must call configure before any other Braintree operations. ::

        braintree.Configuration.configure(
            braintree.Environment.Sandbox,
            "your_merchant_id",
            "your_public_key",
            "your_private_key"
        )
    """
    @staticmethod
    def configure(environment, merchant_id, public_key, private_key, **kwargs):
        Configuration.environment = environment
        Configuration.merchant_id = merchant_id
        Configuration.public_key = public_key
        Configuration.private_key = private_key
        Configuration.default_http_strategy = kwargs.get("http_strategy", None)
        Configuration.timeout = kwargs.get("timeout", 60)
        Configuration.wrap_http_exceptions = kwargs.get("wrap_http_exceptions", False)

    @staticmethod
    def for_partner(environment, partner_id, public_key, private_key, **kwargs):
        return Configuration(
            environment=environment,
            merchant_id=partner_id,
            public_key=public_key,
            private_key=private_key,
            http_strategy=kwargs.get("http_strategy", None),
            timeout=kwargs.get("timeout", 60),
            wrap_http_exceptions=kwargs.get("wrap_http_exceptions", False)
        )

    @staticmethod
    def gateway():
        return braintree.braintree_gateway.BraintreeGateway(Configuration.instantiate())

    @staticmethod
    def instantiate():
        return Configuration(
            environment=Configuration.environment,
            merchant_id=Configuration.merchant_id,
            public_key=Configuration.public_key,
            private_key=Configuration.private_key,
            http_strategy=Configuration.default_http_strategy,
            timeout=Configuration.timeout,
            wrap_http_exceptions=Configuration.wrap_http_exceptions
        )

    @staticmethod
    def api_version():
        return "4"

    def __init__(self, environment, merchant_id, public_key, private_key, **kwargs):
        self.environment = environment
        self.merchant_id = merchant_id
        self.public_key = public_key
        self.private_key = private_key
        self.timeout = kwargs.get("timeout", 60)
        self.wrap_http_exceptions = kwargs.get("wrap_http_exceptions", False)

        http_strategy = kwargs.get("http_strategy", None)

        if http_strategy:
            self._http_strategy = http_strategy(self, self.environment)
        else:
            self._http_strategy = self.http()

    def base_merchant_path(self):
        return "/merchants/" + self.merchant_id

    def base_merchant_url(self):
        return self.environment.protocol + self.environment.server_and_port + self.base_merchant_path()

    def http(self):
        return braintree.util.http.Http(self)

    def http_strategy(self):
        return self._http_strategy
