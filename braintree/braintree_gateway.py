from braintree.address_gateway import AddressGateway
from braintree.credit_card_gateway import CreditCardGateway
from braintree.customer_gateway import CustomerGateway
from braintree.subscription_gateway import SubscriptionGateway
from braintree.transaction_gateway import TransactionGateway
from braintree.transparent_redirect_gateway import TransparentRedirectGateway

class BraintreeGateway(object):
    def __init__(self, config):
        self.config = config
        self.address = AddressGateway(config)
        self.credit_card = CreditCardGateway(config)
        self.customer = CustomerGateway(config)
        self.subscription = SubscriptionGateway(config)
        self.transaction = TransactionGateway(config)
        self.transparent_redirect = TransparentRedirectGateway(config)

