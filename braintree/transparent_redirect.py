from datetime import datetime
import cgi
import urllib
import urlparse
from braintree.configuration import Configuration
from braintree.util.crypto import Crypto
from braintree.util.http import Http
from braintree.exceptions.forged_query_string_error import ForgedQueryStringError

class TransparentRedirect:
    @staticmethod
    def parse_and_validate_query_string(query_string):
        query_params = cgi.parse_qs(query_string)
        http_status = int(query_params["http_status"][0])
        message = query_params.get("bt_message")
        if message != None:
            message = message[0]

        if Http.is_error_status(http_status):
            Http.raise_exception_from_status(http_status, message)

        if not TransparentRedirect.is_valid_tr_query_string(query_string):
            raise ForgedQueryStringError

        return query_params["id"][0]

    @staticmethod
    def tr_data(data, redirect_url):
        data = TransparentRedirect.__flatten_dictionary(data)
        date_string = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        data["time"] = date_string
        data["redirect_url"] = redirect_url
        data["public_key"] = Configuration.public_key
        data["api_version"] = Configuration.api_version()

        tr_content = urllib.urlencode(data)
        tr_hash = Crypto.hmac_hash(Configuration.private_key, tr_content)
        return tr_hash + "|" + tr_content

    @staticmethod
    def is_valid_tr_query_string(query_string):
        content, hash = query_string.split("&hash=")
        return hash == Crypto.hmac_hash(Configuration.private_key, content)

    @staticmethod
    def __flatten_dictionary(params, parent=None):
        data = {}
        for key, val in params.iteritems():
            full_key = parent + "[" + key + "]" if parent else key
            if isinstance(val, dict):
                data.update(TransparentRedirect.__flatten_dictionary(val, full_key))
            else:
                data[full_key] = val
        return data
