from braintree.add_on_gateway import AddOnGateway
from braintree.address_gateway import AddressGateway
from braintree.apple_pay_gateway import ApplePayGateway
from braintree.client_token_gateway import ClientTokenGateway
from braintree.configuration import Configuration
from braintree.credit_card_gateway import CreditCardGateway
from braintree.credit_card_verification_gateway import CreditCardVerificationGateway
from braintree.customer_gateway import CustomerGateway
from braintree.customer_session_gateway import CustomerSessionGateway
from braintree.discount_gateway import DiscountGateway
from braintree.dispute_gateway import DisputeGateway
from braintree.document_upload_gateway import DocumentUploadGateway
from braintree.exchange_rate_quote_gateway import ExchangeRateQuoteGateway
from braintree.merchant_account_gateway import MerchantAccountGateway
from braintree.merchant_gateway import MerchantGateway
from braintree.oauth_gateway import OAuthGateway
from braintree.payment_method_gateway import PaymentMethodGateway
from braintree.payment_method_nonce_gateway import PaymentMethodNonceGateway
from braintree.paypal_account_gateway import PayPalAccountGateway
from braintree.paypal_payment_resource_gateway import PayPalPaymentResourceGateway
from braintree.sepa_direct_debit_account_gateway import SepaDirectDebitAccountGateway
from braintree.plan_gateway import PlanGateway
from braintree.settlement_batch_summary_gateway import SettlementBatchSummaryGateway
from braintree.subscription_gateway import SubscriptionGateway
from braintree.testing_gateway import TestingGateway
from braintree.transaction_gateway import TransactionGateway
from braintree.transaction_line_item_gateway import TransactionLineItemGateway
from braintree.us_bank_account_gateway import UsBankAccountGateway
from braintree.us_bank_account_verification_gateway import UsBankAccountVerificationGateway
from braintree.webhook_notification_gateway import WebhookNotificationGateway
from braintree.webhook_testing_gateway import WebhookTestingGateway
import braintree.configuration

class BraintreeGateway(object):
    def __init__(self, config=None, **kwargs):
        if isinstance(config, braintree.configuration.Configuration):
            self.config = config
        else:
            self.config = Configuration(
                client_id=kwargs.get("client_id"),
                client_secret=kwargs.get("client_secret"),
                access_token=kwargs.get("access_token"),
                http_strategy=kwargs.get("http_strategy")
            )
        self.graphql_client = self.config.graphql_client()

        self.add_on = AddOnGateway(self)
        self.address = AddressGateway(self)
        self.apple_pay = ApplePayGateway(self)
        self.client_token = ClientTokenGateway(self)
        self.credit_card = CreditCardGateway(self)
        self.customer = CustomerGateway(self)
        self.customer_session = CustomerSessionGateway(self)
        self.discount = DiscountGateway(self)
        self.dispute = DisputeGateway(self)
        self.document_upload = DocumentUploadGateway(self)
        self.exchange_rate_quote = ExchangeRateQuoteGateway(self)
        self.merchant = MerchantGateway(self)
        self.merchant_account = MerchantAccountGateway(self) 
        self.oauth = OAuthGateway(self)
        self.payment_method = PaymentMethodGateway(self)
        self.payment_method_nonce = PaymentMethodNonceGateway(self)
        self.paypal_account = PayPalAccountGateway(self)
        self.paypal_payment_resource = PayPalPaymentResourceGateway(self)
        self.plan = PlanGateway(self)
        self.sepa_direct_debit_account = SepaDirectDebitAccountGateway(self)
        self.settlement_batch_summary = SettlementBatchSummaryGateway(self)
        self.subscription = SubscriptionGateway(self)
        self.testing = TestingGateway(self)
        self.transaction = TransactionGateway(self)
        self.transaction_line_item = TransactionLineItemGateway(self)
        self.us_bank_account = UsBankAccountGateway(self)
        self.us_bank_account_verification = UsBankAccountVerificationGateway(self)
        self.verification = CreditCardVerificationGateway(self)
        self.webhook_notification = WebhookNotificationGateway(self)
        self.webhook_testing = WebhookTestingGateway(self)
