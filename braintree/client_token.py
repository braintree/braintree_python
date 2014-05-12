import datetime
import json
import urllib
from braintree.configuration import Configuration
from braintree.signature_service import SignatureService
from braintree.util.crypto import Crypto
from braintree import exceptions

class ClientToken(object):

    @staticmethod
    def generate(params=None, gateway=None):

        if gateway is None:
            gateway = Configuration.gateway().client_token

        if params and "options" in params and not "customer_id" in params:
            for option in ["verify_card", "make_default", "fail_on_duplicate_payment_method"]:
                if option in params["options"]:
                    raise exceptions.InvalidSignatureError("cannot specify %s without a customer_id" % option)

        return gateway.generate(params)

    @staticmethod
    def generate_signature():
        return [
            "customer_id", "proxy_merchant_id",
            {"options": ["make_default", "verify_card", "fail_on_duplicate_payment_method"]}
        ]
