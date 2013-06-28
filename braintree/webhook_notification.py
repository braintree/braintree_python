from braintree.resource import Resource
from braintree.configuration import Configuration
from braintree.subscription import Subscription
from braintree.merchant_account import MerchantAccount
from braintree.error_result import ErrorResult

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

    @staticmethod
    def parse(signature, payload):
        return Configuration.gateway().webhook_notification.parse(signature, payload)

    @staticmethod
    def verify(challenge):
        return Configuration.gateway().webhook_notification.verify(challenge)

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)
        if "subscription" in attributes['subject']:
            self.subscription = Subscription(gateway, attributes['subject']['subscription'])
        elif "merchant_account" in attributes['subject']:
            self.merchant_account = MerchantAccount(gateway, attributes['subject']['merchant_account'])
        elif "api_error_response" in attributes['subject']:
            self.errors = ErrorResult(gateway, attributes['subject']['api_error_response'])
