import braintree
from braintree.us_bank_account import UsBankAccount
from braintree.exceptions.not_found_error import NotFoundError
from braintree.util.validation import is_invalid_path_segment

class UsBankAccountGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, us_bank_account_token):
        try:
            if is_invalid_path_segment(us_bank_account_token):
                raise NotFoundError()

            response = self.config.http().get(self.config.base_merchant_path() + "/payment_methods/us_bank_account/" + us_bank_account_token)
            if "us_bank_account" in response:
                return UsBankAccount(self.gateway, response["us_bank_account"])
        except NotFoundError:
            raise NotFoundError("US bank account with token " + repr(us_bank_account_token) + " not found")

