import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration
from braintree.iban_bank_account import IbanBankAccount

# NEXT_MAJOR_VERSION Remove this class as legacy Ideal has been removed/disabled in the Braintree Gateway
# DEPRECATED If you're looking to accept iDEAL as a payment method contact accounts@braintreepayments.com for a solution.
class IdealPayment(Resource):

    @staticmethod
    def find(ideal_payment_id):
        return Configuration.gateway().ideal_payment.find(ideal_payment_id)

    @staticmethod
    def sale(ideal_payment_id, transactionRequest):
        request = transactionRequest.copy()
        request["payment_method_nonce"] = ideal_payment_id
        if not "options" in request:
            request["options"] = {}
        request["options"]["submit_for_settlement"] = True
        return Configuration.gateway().transaction.sale(request)

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if attributes.get('iban_bank_account') is not None:
            self.iban_bank_account = IbanBankAccount(gateway, self.iban_bank_account)
        else:
            self.iban_bank_account = None
