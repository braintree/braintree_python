from braintree.account_updater_daily_report import AccountUpdaterDailyReport
from braintree.configuration import Configuration
from braintree.connected_merchant_paypal_status_changed import ConnectedMerchantPayPalStatusChanged
from braintree.connected_merchant_status_transitioned import ConnectedMerchantStatusTransitioned
from braintree.disbursement import Disbursement
from braintree.dispute import Dispute
from braintree.error_result import ErrorResult
from braintree.granted_payment_instrument_update import GrantedPaymentInstrumentUpdate
from braintree.local_payment_completed import LocalPaymentCompleted
from braintree.local_payment_expired import LocalPaymentExpired
from braintree.local_payment_funded import LocalPaymentFunded
from braintree.local_payment_reversed import LocalPaymentReversed
from braintree.merchant_account import MerchantAccount
from braintree.oauth_access_revocation import OAuthAccessRevocation
from braintree.partner_merchant import PartnerMerchant
from braintree.payment_method_customer_data_updated_metadata import PaymentMethodCustomerDataUpdatedMetadata
from braintree.resource import Resource
from braintree.revoked_payment_method_metadata import RevokedPaymentMethodMetadata
from braintree.subscription import Subscription
from braintree.transaction import Transaction
from braintree.transaction_review import TransactionReview
from braintree.validation_error_collection import ValidationErrorCollection

class WebhookNotification(Resource):
    class Kind(object):
        AccountUpdaterDailyReport = "account_updater_daily_report"
        Check = "check"
        ConnectedMerchantPayPalStatusChanged = "connected_merchant_paypal_status_changed"
        ConnectedMerchantStatusTransitioned = "connected_merchant_status_transitioned"
        Disbursement = "disbursement"
        DisbursementException = "disbursement_exception"
        DisputeAccepted = "dispute_accepted"
        DisputeAutoAccepted = "dispute_auto_accepted"
        DisputeDisputed = "dispute_disputed"
        DisputeExpired = "dispute_expired"
        DisputeLost = "dispute_lost"
        DisputeOpened = "dispute_opened"
        DisputeUnderReview = "dispute_under_review"
        DisputeWon = "dispute_won"
        GrantedPaymentMethodRevoked = "granted_payment_method_revoked"
        GrantorUpdatedGrantedPaymentMethod = "grantor_updated_granted_payment_method"
        LocalPaymentCompleted = "local_payment_completed"
        LocalPaymentExpired = "local_payment_expired"
        LocalPaymentFunded = "local_payment_funded"
        LocalPaymentReversed = "local_payment_reversed"
        OAuthAccessRevoked = "oauth_access_revoked"
        PartnerMerchantConnected = "partner_merchant_connected"
        PartnerMerchantDeclined = "partner_merchant_declined"
        PartnerMerchantDisconnected = "partner_merchant_disconnected"
        PaymentMethodCustomerDataUpdated = "payment_method_customer_data_updated"
        PaymentMethodRevokedByCustomer = "payment_method_revoked_by_customer"
        RecipientUpdatedGrantedPaymentMethod = "recipient_updated_granted_payment_method"
        RefundFailed = "refund_failed"
        SubscriptionBillingSkipped = "subscription_billing_skipped"
        SubscriptionCanceled = "subscription_canceled"
        SubscriptionChargedSuccessfully = "subscription_charged_successfully"
        SubscriptionChargedUnsuccessfully = "subscription_charged_unsuccessfully"
        SubscriptionExpired = "subscription_expired"
        SubscriptionTrialEnded = "subscription_trial_ended"
        SubscriptionWentActive = "subscription_went_active"
        SubscriptionWentPastDue = "subscription_went_past_due"
        TransactionDisbursed = "transaction_disbursed"
        TransactionReviewed = "transaction_reviewed"
        TransactionSettled = "transaction_settled"
        TransactionSettlementDeclined = "transaction_settlement_declined"

    @staticmethod
    def parse(signature, payload):
        return Configuration.gateway().webhook_notification.parse(signature, payload)

    @staticmethod
    def verify(challenge):
        return Configuration.gateway().webhook_notification.verify(challenge)

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

        if "source_merchant_id" not in attributes:
            self.source_merchant_id = None

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
        elif "transaction_review" in node_wrapper:
            self.transaction_review = TransactionReview(node_wrapper['transaction_review'])
        elif "connected_merchant_status_transitioned" in node_wrapper:
            self.connected_merchant_status_transitioned = ConnectedMerchantStatusTransitioned(gateway, node_wrapper['connected_merchant_status_transitioned'])
        elif "connected_merchant_paypal_status_changed" in node_wrapper:
            self.connected_merchant_paypal_status_changed = ConnectedMerchantPayPalStatusChanged(gateway, node_wrapper['connected_merchant_paypal_status_changed'])
        elif "partner_merchant" in node_wrapper:
            self.partner_merchant = PartnerMerchant(gateway, node_wrapper['partner_merchant'])
        elif "oauth_application_revocation" in node_wrapper:
            self.oauth_access_revocation = OAuthAccessRevocation(node_wrapper["oauth_application_revocation"])
        elif "disbursement" in node_wrapper:
            self.disbursement = Disbursement(gateway, node_wrapper['disbursement'])
        elif "dispute" in node_wrapper:
            self.dispute = Dispute(node_wrapper['dispute'])
        elif "account_updater_daily_report" in node_wrapper:
            self.account_updater_daily_report = AccountUpdaterDailyReport(gateway, node_wrapper['account_updater_daily_report'])
        elif "granted_payment_instrument_update" in node_wrapper:
            self.granted_payment_instrument_update = GrantedPaymentInstrumentUpdate(gateway, node_wrapper["granted_payment_instrument_update"])
        elif attributes["kind"] in [WebhookNotification.Kind.GrantedPaymentMethodRevoked, WebhookNotification.Kind.PaymentMethodRevokedByCustomer]:
            self.revoked_payment_method_metadata = RevokedPaymentMethodMetadata(gateway, node_wrapper)
        elif "local_payment" in node_wrapper and attributes["kind"] == WebhookNotification.Kind.LocalPaymentCompleted:
            self.local_payment_completed = LocalPaymentCompleted(gateway, node_wrapper["local_payment"])
        elif "local_payment_expired" in node_wrapper and attributes["kind"] == WebhookNotification.Kind.LocalPaymentExpired:
            self.local_payment_expired = LocalPaymentExpired(gateway, node_wrapper["local_payment_expired"])
        elif "local_payment_funded" in node_wrapper and attributes["kind"] == WebhookNotification.Kind.LocalPaymentFunded:
            self.local_payment_funded = LocalPaymentFunded(gateway, node_wrapper["local_payment_funded"])
        elif "local_payment_reversed" in node_wrapper and attributes["kind"] == WebhookNotification.Kind.LocalPaymentReversed:
            self.local_payment_reversed = LocalPaymentReversed(gateway, node_wrapper["local_payment_reversed"])
        elif "payment_method_customer_data_updated_metadata" in node_wrapper and attributes["kind"] == WebhookNotification.Kind.PaymentMethodCustomerDataUpdated:
            self.payment_method_customer_data_updated_metadata = PaymentMethodCustomerDataUpdatedMetadata(gateway, node_wrapper["payment_method_customer_data_updated_metadata"])

        if "errors" in node_wrapper:
            self.errors = ValidationErrorCollection(node_wrapper['errors'])
            self.message = node_wrapper['message']
