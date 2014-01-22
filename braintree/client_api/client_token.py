import datetime
import json
import urllib
from braintree.configuration import Configuration
from braintree.signature_service import SignatureService
from braintree.util.crypto import Crypto
from braintree import exceptions

class ClientToken(object):

    @staticmethod
    def generate(params={}):
        data = {
            "public_key": Configuration.public_key,
            "created_at": datetime.datetime.now()
        }

        if "customer_id" in params:
            data["customer_id"] = params["customer_id"]

        for option in ["verify_card", "make_default", "fail_on_duplicate_payment_method"]:
            if option in params:
                if not "customer_id" in data:
                    raise exceptions.InvalidSignatureError("cannot specify %s without a customer_id" % option)
                data["credit_card[options][%s]" % option] = params[option]

        authorization_fingerprint = SignatureService(Configuration.private_key, Crypto.sha256_hmac_hash).sign(data)

        return json.dumps({
            "authorization_fingerprint": authorization_fingerprint,
            "client_api_url": Configuration.instantiate().base_merchant_url() + "/client_api",
            "auth_url": Configuration.instantiate().environment.auth_url
        })
