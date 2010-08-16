import braintree
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from braintree.transparent_redirect import TransparentRedirect

class TransparentRedirectGateway(object):
    def __init__(self, config):
        self.config = config

    def confirm(self, query_string):
        """
        Confirms a transparent redirect request. It expects the query string from the
        redirect request. The query string should _not_ include the leading "?" character. ::

            result = braintree.TransparentRedirect.confirm("foo=bar&id=12345")
        """
        parsed_query_string = TransparentRedirect.parse_and_validate_query_string(query_string)
        confirmation_gateway = {
            TransparentRedirect.Kind.CreateCustomer: "customer",
            TransparentRedirect.Kind.UpdateCustomer: "customer",
            TransparentRedirect.Kind.CreatePaymentMethod: "credit_card",
            TransparentRedirect.Kind.UpdatePaymentMethod: "credit_card",
            TransparentRedirect.Kind.CreateTransaction: "transaction"
        }[parsed_query_string["kind"][0]]

        gateway = braintree.braintree_gateway.BraintreeGateway(self.config)
        return getattr(gateway, confirmation_gateway)._post("/transparent_redirect_requests/" + parsed_query_string["id"][0] + "/confirm")

    def url(self):
        """
        Returns the url for POSTing Transparent Redirect HTML forms
        """
        return self.config.base_merchant_url() + "/transparent_redirect_requests"

