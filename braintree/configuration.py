import os
from braintree.environment import Environment

class Configuration(object):
    @staticmethod
    def configure(environment, merchant_id, public_key, private_key):
        Configuration.environment = environment
        Configuration.merchant_id = merchant_id
        Configuration.public_key = public_key
        Configuration.private_key = private_key
        Configuration.use_unsafe_ssl = False

    @staticmethod
    def base_merchant_path():
        return "/merchants/" + Configuration.merchant_id

    @staticmethod
    def base_merchant_url():
        return Configuration.environment.protocol + Configuration.environment.server_and_port + Configuration.base_merchant_path()
