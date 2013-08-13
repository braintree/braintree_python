from braintree.resource import Resource
from braintree.configuration import Configuration
from braintree.subscription import Subscription
from braintree.merchant_account import MerchantAccount
from braintree.transaction import Transaction
from braintree.error_result import ErrorResult
from braintree.validation_error_collection import ValidationErrorCollection

class WebhookNotification(Resource):
    class Kind(object):
        SubscriptionCanceled = "subscription_canceled"
        SubscriptionChargedSuccessfully = "subscription_charged_successfully"
        SubscriptionChargedUnsuccessfully = "subscription_charged_unsuccessfully"
        SubscriptionExpired = "subscription_expired"
        SubscriptionTrialEnded = "subscription_trial_ended"
        SubscriptionWentActive = "subscription_went_active"
        SubscriptionWentPastDue = "subscription_went_past_due"
        SubMerchantAccountApproved = "sub_merchant_account_approved"
        SubMerchantAccountDeclined = "sub_merchant_account_declined"
        TransactionDisbursed = "transaction_disbursed"

    @staticmethod
    def parse(signature, payload):
        return Configuration.gateway().webhook_notification.parse(signature, payload)

    @staticmethod
    def verify(challenge):
        return Configuration.gateway().webhook_notification.verify(challenge)

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

        if "api_error_response" in attributes["subject"]:
            node_wrapper = attributes["subject"]["api_error_response"]
        else:
            node_wrapper = attributes["subject"]

        if "subscription" in node_wrapper:
            self.subscription = Subscription(gateway, node_wrapper['subscription'])
        elif "merchant_account" in node_wrapper:
            self.merchant_account = MerchantAccount(gateway, node_wrapper['merchant_account'])
        elif "transaction" in node_wrapper:
            self.transaction = Transaction(gateway, node_wrapper['transaction'])

        if "errors" in node_wrapper:
            self.errors = ValidationErrorCollection(node_wrapper['errors'])
            self.message = node_wrapper['message']
