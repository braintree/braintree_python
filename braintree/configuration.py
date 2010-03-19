import os
from braintree.environment import Environment

class Configuration(object):
    @staticmethod
    def base_merchant_path():
        return "/merchants/" + Configuration.merchant_id

    @staticmethod
    def base_merchant_url():
        return Configuration.protocol() + Configuration.environment.server_and_port + Configuration.base_merchant_path()

    @staticmethod
    def protocol():
        if Configuration.environment.is_ssl:
            return "https://"
        else:
            return "http://"
