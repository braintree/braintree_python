import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration

class IdealPayment(Resource):
    @staticmethod
    def sale(nonce, transactionRequest):
        request = transactionRequest.copy()
        request["payment_method_nonce"] = nonce
        if not "options" in request:
            request["options"] = {}
        request["options"]["submit_for_settlement"] = True
        return Configuration.gateway().transaction.sale(request)
