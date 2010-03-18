from datetime import datetime
import urllib
from braintree.configuration import Configuration
from braintree.util.crypto import Crypto

class TransparentRedirect:
    @staticmethod
    def tr_data(data, redirect_url):
        data = TransparentRedirect.flatten_dictionary(data)
        date_string = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        data["time"] = date_string
        data["redirect_url"] = redirect_url
        data["public_key"] = Configuration.public_key
        data["api_version"] = "1"

        tr_content = urllib.urlencode(data)
        tr_hash = Crypto.hmac_hash(Configuration.private_key, tr_content)
        return tr_hash + "|" + tr_content

    @staticmethod
    def flatten_dictionary(params, parent=None):
        data = {}
        for key, val in params.iteritems():
            full_key = parent + "[" + key + "]" if parent else key
            if type(val) == dict:
                data.update(TransparentRedirect.flatten_dictionary(val, full_key))
            else:
                data[full_key] = val
        return data
