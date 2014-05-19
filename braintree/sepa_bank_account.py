import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration

class SEPABankAccount(Resource):
    class MandateType(object):
        """
        Constants representing the type of the mandate.  Available type:
        * Braintree.SEPABankAccount.MandateType.Business
        * Braintree.SEPABankAccount.MandateType.Consumer
        """
        Business = "business"
        Consumer = "consumer"

