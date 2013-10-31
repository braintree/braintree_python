import datetime
import urllib
from braintree.configuration import Configuration
from braintree.util.crypto import Crypto

class AuthorizationFingerprint(object):

    @staticmethod
    def generate(params={}):
        default_values = {
            "merchant_id": Configuration.merchant_id,
            "public_key": Configuration.public_key,
            "created_at": datetime.datetime.now()
        }
        data = dict(params.items() + default_values.items())
        tr_content = urllib.urlencode(data)
        tr_hash = Crypto.hmac_hash(Configuration.private_key, tr_content)
        return tr_hash + "|" + tr_content
