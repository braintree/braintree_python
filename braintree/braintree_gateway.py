from braintree.add_on_gateway import AddOnGateway
from braintree.address_gateway import AddressGateway
from braintree.credit_card_gateway import CreditCardGateway
from braintree.customer_gateway import CustomerGateway
from braintree.discount_gateway import DiscountGateway
from braintree.plan_gateway import PlanGateway
from braintree.settlement_batch_summary_gateway import SettlementBatchSummaryGateway
from braintree.subscription_gateway import SubscriptionGateway
from braintree.transaction_gateway import TransactionGateway
from braintree.transparent_redirect_gateway import TransparentRedirectGateway

class BraintreeGateway(object):
    def __init__(self, config):
        self.config = config
        self.add_on = AddOnGateway(self)
        self.address = AddressGateway(self)
        self.credit_card = CreditCardGateway(self)
        self.customer = CustomerGateway(self)
        self.discount = DiscountGateway(self)
        self.plan = PlanGateway(self)
        self.settlement_batch_summary = SettlementBatchSummaryGateway(self)
        self.subscription = SubscriptionGateway(self)
        self.transaction = TransactionGateway(self)
        self.transparent_redirect = TransparentRedirectGateway(self)

