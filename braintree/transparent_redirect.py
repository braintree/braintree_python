from datetime import datetime
import cgi
import urllib
import urlparse
import braintree
from braintree.configuration import Configuration
from braintree.util.crypto import Crypto
from braintree.util.http import Http
from braintree.exceptions.forged_query_string_error import ForgedQueryStringError

class TransparentRedirect:
    """
    A class used for Transparent Redirect operations
    """

    class Kind(object):
        CreateCustomer = "create_customer"
        UpdateCustomer = "update_customer"
        CreatePaymentMethod = "create_payment_method"
        UpdatePaymentMethod = "update_payment_method"
        CreateTransaction = "create_transaction"

    @staticmethod
    def confirm(query_string):
        """
        Confirms a transparent redirect request. It expects the query string from the
        redirect request. The query string should _not_ include the leading "?" character. ::

            result = braintree.TransparentRedirect.confirm("foo=bar&id=12345")
        """
        parsed_query_string = TransparentRedirect.parse_and_validate_query_string(query_string)
        confirmation_klass = {
            TransparentRedirect.Kind.CreateCustomer: braintree.customer.Customer,
            TransparentRedirect.Kind.UpdateCustomer: braintree.transaction.Customer,
            TransparentRedirect.Kind.CreatePaymentMethod: braintree.customer.CreditCard,
            TransparentRedirect.Kind.UpdatePaymentMethod: braintree.customer.CreditCard,
            TransparentRedirect.Kind.CreateTransaction: braintree.transaction.Transaction
        }[parsed_query_string["kind"][0]]
        return confirmation_klass._post("/transparent_redirect_requests/" + parsed_query_string["id"][0] + "/confirm")


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

        return query_params

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
    def url():
        """
        Returns the url for POSTing Transparent Redirect HTML forms
        """
        return Configuration.base_merchant_url() + "/transparent_redirect_requests"

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
