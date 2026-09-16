import braintree
from braintree.sepa_direct_debit_account import SepaDirectDebitAccount
from braintree.error_result import ErrorResult
from braintree.exceptions.not_found_error import NotFoundError
from braintree.resource import Resource
from braintree.successful_result import SuccessfulResult
from braintree.util.validation import is_invalid_path_segment


class SepaDirectDebitAccountGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, sepa_direct_debit_account_token):
        try:
            if is_invalid_path_segment(sepa_direct_debit_account_token):
                raise NotFoundError()

            response = self.config.http().get(self.config.base_merchant_path() + "/payment_methods/sepa_debit_account/" + sepa_direct_debit_account_token)
            if "sepa_debit_account" in response:
                return SepaDirectDebitAccount(self.gateway, response["sepa_debit_account"])
        except NotFoundError:
            raise NotFoundError("sepa direct debit account with token " + repr(sepa_direct_debit_account_token) + " not found")

    def delete(self, sepa_direct_debit_account_token):
        if is_invalid_path_segment(sepa_direct_debit_account_token):
            raise NotFoundError("sepa direct debit account with token " + repr(sepa_direct_debit_account_token) + " not found")

        self.config.http().delete(self.config.base_merchant_path() + "/payment_methods/sepa_debit_account/" + sepa_direct_debit_account_token)
        return SuccessfulResult()
