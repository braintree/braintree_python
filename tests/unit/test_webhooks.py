from tests.test_helper import *
from datetime import date
from braintree.dispute import Dispute
from braintree.credit_card import CreditCard
from braintree.paypal_account import PayPalAccount
from braintree.venmo_account import VenmoAccount

class TestWebhooks(unittest.TestCase):
    def test_granted_payment_method_revoked(self):
        webhook_testing_gateway = WebhookTestingGateway(BraintreeGateway(Configuration.instantiate()))

        sample_notification = webhook_testing_gateway.sample_notification(WebhookNotification.Kind.GrantedPaymentMethodRevoked, 'granted_payment_method_revoked_id')

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        metadata = notification.revoked_payment_method_metadata

        self.assertEqual(WebhookNotification.Kind.GrantedPaymentMethodRevoked, notification.kind)
        self.assertEqual("venmo_customer_id", metadata.customer_id)
        self.assertEqual("granted_payment_method_revoked_id", metadata.token)
        self.assertEqual(type(metadata.revoked_payment_method), VenmoAccount)

    def test_sample_notification_builds_a_parsable_notification(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.SubscriptionWentPastDue, notification.kind)
        self.assertEqual("my_id", notification.subscription.id)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)
        self.assertIsNone(notification.source_merchant_id)

    def test_sample_notification_with_source_merchant_id(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            'my_id',
            'my_source_merchant_id'
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual('my_source_merchant_id', notification.source_merchant_id)

    def test_completely_invalid_signature(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )
        with self.assertRaises(InvalidSignatureError):
            WebhookNotification.parse("bad_stuff", sample_notification['bt_payload'])

    def test_parse_raises_when_public_key_is_wrong(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        config = Configuration(
            environment=Environment.Development,
            merchant_id="integration_merchant_id",
            public_key="wrong_public_key",
            private_key="wrong_private_key"
        )
        gateway = BraintreeGateway(config)

        try:
            gateway.webhook_notification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])
        except InvalidSignatureError as e:
            self.assertEqual("no matching public key", str(e))
        else:
            self.assertFalse("raises exception")

    def test_invalid_signature_when_payload_modified(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        try:
            WebhookNotification.parse(sample_notification['bt_signature'], b"badstuff" + sample_notification['bt_payload'])
        except InvalidSignatureError as e:
            self.assertEqual("signature does not match payload - one has been modified", str(e))
        else:
            self.assertFalse("raises exception")

    def test_parse_raise_exception_if_signature_is_blank(self):
        try:
            WebhookNotification.parse(None, "payload")
        except InvalidSignatureError as e:
            self.assertEqual("signature cannot be blank", str(e))
        else:
            self.assertFalse("raises exception")

    def test_parse_raise_exception_if_payload_is_blank(self):
        try:
            WebhookNotification.parse("signature", None)
        except InvalidSignatureError as e:
            self.assertEqual("payload cannot be blank", str(e))
        else:
            self.assertFalse("raises exception")

    def test_invalid_signature_when_bontains_invalid_characters(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        try:
            WebhookNotification.parse(sample_notification['bt_signature'], "~* invalid! *~")
        except InvalidSignatureError as e:
            self.assertEqual("payload contains illegal characters", str(e))
        else:
            self.assertFalse("raises exception")

    def test_parse_allows_all_valid_characters(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        try:
            WebhookNotification.parse(sample_notification['bt_signature'], "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+=/\n")
        except InvalidSignatureError as e:
            self.assertNotEqual("payload contains illegal characters", str(e))

    def test_parse_retries_payload_with_a_newline(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'].rstrip())

        self.assertEqual(WebhookNotification.Kind.SubscriptionWentPastDue, notification.kind)
        self.assertEqual("my_id", notification.subscription.id)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)

    def test_verify_returns_a_correct_challenge_response(self):
        response = WebhookNotification.verify("20f9f8ed05f77439fe955c977e4c8a53")
        self.assertEqual("integration_public_key|d9b899556c966b3f06945ec21311865d35df3ce4", response)

    def test_verify_raises_when_challenge_is_invalid(self):
        try:
            WebhookNotification.verify("bad challenge")
        except InvalidChallengeError as e:
            self.assertEqual("challenge contains non-hex characters", str(e))
        else:
            self.assertFalse("raises exception")

    def test_builds_notification_for_approved_sub_merchant_account(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubMerchantAccountApproved,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.SubMerchantAccountApproved, notification.kind)
        self.assertEqual("my_id", notification.merchant_account.id)
        self.assertEqual(MerchantAccount.Status.Active, notification.merchant_account.status)
        self.assertEqual("master_ma_for_my_id", notification.merchant_account.master_merchant_account.id)
        self.assertEqual(MerchantAccount.Status.Active, notification.merchant_account.master_merchant_account.status)

    def test_builds_notification_for_declined_sub_merchant_account(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubMerchantAccountDeclined,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.SubMerchantAccountDeclined, notification.kind)
        self.assertEqual("my_id", notification.merchant_account.id)
        self.assertEqual(MerchantAccount.Status.Suspended, notification.merchant_account.status)
        self.assertEqual("master_ma_for_my_id", notification.merchant_account.master_merchant_account.id)
        self.assertEqual(MerchantAccount.Status.Suspended, notification.merchant_account.master_merchant_account.status)
        self.assertEqual("Credit score is too low", notification.message)
        self.assertEqual(ErrorCodes.MerchantAccount.DeclinedOFAC, notification.errors.for_object("merchant_account").on("base")[0].code)

    def test_builds_notification_for_disbursed_transactions(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.TransactionDisbursed,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.TransactionDisbursed, notification.kind)
        self.assertEqual("my_id", notification.transaction.id)
        self.assertEqual(100, notification.transaction.amount)
        self.assertEqual(datetime(2013, 7, 9, 18, 23, 29), notification.transaction.disbursement_details.disbursement_date)

    def test_builds_notification_for_reviewed_transactions(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.TransactionReviewed,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.TransactionReviewed, notification.kind)
        self.assertEqual("my_id", notification.transaction_review.transaction_id)
        self.assertEqual("a smart decision", notification.transaction_review.decision)
        self.assertEqual("hey@girl.com", notification.transaction_review.reviewer_email)
        self.assertEqual("I reviewed this", notification.transaction_review.reviewer_note)
        self.assertEqual(datetime(2021, 4, 20, 6, 9, 0), notification.transaction_review.reviewed_time)

    def test_builds_notification_for_settled_transactions(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.TransactionSettled,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.TransactionSettled, notification.kind)
        self.assertEqual("my_id", notification.transaction.id)
        self.assertEqual("settled", notification.transaction.status)
        self.assertEqual(100, notification.transaction.amount)
        self.assertEqual(notification.transaction.us_bank_account.routing_number, "123456789")
        self.assertEqual(notification.transaction.us_bank_account.last_4, "1234")
        self.assertEqual(notification.transaction.us_bank_account.account_type, "checking")
        self.assertEqual(notification.transaction.us_bank_account.account_holder_name, "Dan Schulman")

    def test_builds_notification_for_settlement_declined_transactions(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.TransactionSettlementDeclined,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.TransactionSettlementDeclined, notification.kind)
        self.assertEqual("my_id", notification.transaction.id)
        self.assertEqual("settlement_declined", notification.transaction.status)
        self.assertEqual(100, notification.transaction.amount)
        self.assertEqual(notification.transaction.us_bank_account.routing_number, "123456789")
        self.assertEqual(notification.transaction.us_bank_account.last_4, "1234")
        self.assertEqual(notification.transaction.us_bank_account.account_type, "checking")
        self.assertEqual(notification.transaction.us_bank_account.account_holder_name, "Dan Schulman")

    def test_builds_notification_for_disbursements(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.Disbursement,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.Disbursement, notification.kind)
        self.assertEqual("my_id", notification.disbursement.id)
        self.assertEqual(100, notification.disbursement.amount)
        self.assertEqual(None, notification.disbursement.exception_message)
        self.assertEqual(None, notification.disbursement.follow_up_action)
        self.assertEqual(date(2014, 2, 9), notification.disbursement.disbursement_date)

    def test_builds_notification_for_disbursement_exceptions(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisbursementException,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisbursementException, notification.kind)
        self.assertEqual("my_id", notification.disbursement.id)
        self.assertEqual(100, notification.disbursement.amount)
        self.assertEqual("bank_rejected", notification.disbursement.exception_message)
        self.assertEqual("update_funding_information", notification.disbursement.follow_up_action)
        self.assertEqual(date(2014, 2, 9), notification.disbursement.disbursement_date)

    def test_builds_notification_for_old_dispute_under_review(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeUnderReview,
            "legacy_dispute_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeUnderReview, notification.kind)
        self.assertEqual("legacy_dispute_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.UnderReview, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_old_dispute_opened(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeOpened,
            "legacy_dispute_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeOpened, notification.kind)
        self.assertEqual("legacy_dispute_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Open, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)
        self.assertEqual(notification.dispute.date_opened, date(2014, 3, 28))

    def test_builds_notification_for_old_dispute_lost(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeLost,
            "legacy_dispute_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeLost, notification.kind)
        self.assertEqual("legacy_dispute_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Lost, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)
        self.assertEqual(notification.dispute.date_opened, date(2014, 3, 28))

    def test_builds_notification_for_old_dispute_won(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeWon,
            "legacy_dispute_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeWon, notification.kind)
        self.assertEqual("legacy_dispute_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Won, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)
        self.assertEqual(notification.dispute.date_opened, date(2014, 3, 28))
        self.assertEqual(notification.dispute.date_won, date(2014, 9, 1))

    def test_builds_notification_for_old_dispute_accepted(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeAccepted,
            "legacy_dispute_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeAccepted, notification.kind)
        self.assertEqual("legacy_dispute_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Accepted, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_old_dispute_auto_accepted(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeAutoAccepted,
            "legacy_dispute_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeAutoAccepted, notification.kind)
        self.assertEqual("legacy_dispute_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.AutoAccepted, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_old_dispute_disputed(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeDisputed,
            "legacy_dispute_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeDisputed, notification.kind)
        self.assertEqual("legacy_dispute_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Disputed, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_old_dispute_expired(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeExpired,
            "legacy_dispute_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeExpired, notification.kind)
        self.assertEqual("legacy_dispute_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Expired, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_new_dispute_under_review(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeUnderReview,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeUnderReview, notification.kind)
        self.assertEqual("my_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.UnderReview, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_new_dispute_opened(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeOpened,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeOpened, notification.kind)
        self.assertEqual("my_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Open, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)
        self.assertEqual(notification.dispute.date_opened, date(2014, 3, 28))

    def test_builds_notification_for_new_dispute_lost(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeLost,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeLost, notification.kind)
        self.assertEqual("my_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Lost, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)
        self.assertEqual(notification.dispute.date_opened, date(2014, 3, 28))

    def test_builds_notification_for_new_dispute_won(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeWon,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeWon, notification.kind)
        self.assertEqual("my_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Won, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)
        self.assertEqual(notification.dispute.date_opened, date(2014, 3, 28))
        self.assertEqual(notification.dispute.date_won, date(2014, 9, 1))

    def test_builds_notification_for_new_dispute_accepted(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeAccepted,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeAccepted, notification.kind)
        self.assertEqual("my_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Accepted, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_new_dispute_auto_accepted(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeAutoAccepted,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeAutoAccepted, notification.kind)
        self.assertEqual("my_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.AutoAccepted, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_new_dispute_disputed(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeDisputed,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeDisputed, notification.kind)
        self.assertEqual("my_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Disputed, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_new_dispute_expired(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.DisputeExpired,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.DisputeExpired, notification.kind)
        self.assertEqual("my_id", notification.dispute.id)
        self.assertEqual(Dispute.Status.Expired, notification.dispute.status)
        self.assertEqual(Dispute.Kind.Chargeback, notification.dispute.kind)

    def test_builds_notification_for_partner_merchant_connected(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.PartnerMerchantConnected,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.PartnerMerchantConnected, notification.kind)
        self.assertEqual("abc123", notification.partner_merchant.partner_merchant_id)
        self.assertEqual("public_key", notification.partner_merchant.public_key)
        self.assertEqual("private_key", notification.partner_merchant.private_key)
        self.assertEqual("public_id", notification.partner_merchant.merchant_public_id)
        self.assertEqual("cse_key", notification.partner_merchant.client_side_encryption_key)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)

    def test_builds_notification_for_partner_merchant_disconnected(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.PartnerMerchantDisconnected,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.PartnerMerchantDisconnected, notification.kind)
        self.assertEqual("abc123", notification.partner_merchant.partner_merchant_id)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)

    def test_builds_notification_for_partner_merchant_declined(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.PartnerMerchantDeclined,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.PartnerMerchantDeclined, notification.kind)
        self.assertEqual("abc123", notification.partner_merchant.partner_merchant_id)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)

    def test_builds_notification_for_oauth_access_revoked(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.OAuthAccessRevoked,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])

        self.assertEqual(WebhookNotification.Kind.OAuthAccessRevoked, notification.kind)
        self.assertEqual("my_id", notification.oauth_access_revocation.merchant_id)
        self.assertEqual("oauth_application_client_id", notification.oauth_access_revocation.oauth_application_client_id)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)

    def test_builds_notification_for_connected_merchant_status_transitioned(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.ConnectedMerchantStatusTransitioned,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.ConnectedMerchantStatusTransitioned, notification.kind)
        self.assertEqual("new_status", notification.connected_merchant_status_transitioned.status)
        self.assertEqual("my_id", notification.connected_merchant_status_transitioned.merchant_public_id)
        self.assertEqual("my_id", notification.connected_merchant_status_transitioned.merchant_id)
        self.assertEqual("oauth_application_client_id", notification.connected_merchant_status_transitioned.oauth_application_client_id)

    def test_builds_notification_for_connected_merchant_paypal_status_changed(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.ConnectedMerchantPayPalStatusChanged,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.ConnectedMerchantPayPalStatusChanged, notification.kind)
        self.assertEqual("link", notification.connected_merchant_paypal_status_changed.action)
        self.assertEqual("my_id", notification.connected_merchant_paypal_status_changed.merchant_public_id)
        self.assertEqual("my_id", notification.connected_merchant_paypal_status_changed.merchant_id)
        self.assertEqual("oauth_application_client_id", notification.connected_merchant_paypal_status_changed.oauth_application_client_id)

    def test_builds_notification_for_refund_failed(self):
        sample_notification = WebhookTesting.sample_notification(
                WebhookNotification.Kind.RefundFailed,
                "my_id"
         )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.RefundFailed, notification.kind)
        self.assertEqual("my_id", notification.transaction.id)

    def test_builds_notification_for_subscription_billing_skipped(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionBillingSkipped,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.SubscriptionBillingSkipped, notification.kind)
        self.assertEqual("my_id", notification.subscription.id)
        self.assertTrue(len(notification.subscription.transactions) == 0)
        self.assertTrue(len(notification.subscription.discounts) == 0)
        self.assertTrue(len(notification.subscription.add_ons) == 0)

    def test_builds_notification_for_subscription_charged_successfully(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionChargedSuccessfully,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.SubscriptionChargedSuccessfully, notification.kind)
        self.assertEqual("my_id", notification.subscription.id)
        self.assertTrue(len(notification.subscription.transactions) == 1)

        transaction = notification.subscription.transactions.pop()

        self.assertEqual("submitted_for_settlement", transaction.status)
        self.assertEqual(Decimal("49.99"), transaction.amount)

    def test_builds_notification_for_subscription_charged_unsuccessfully(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionChargedUnsuccessfully,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.SubscriptionChargedUnsuccessfully, notification.kind)
        self.assertEqual("my_id", notification.subscription.id)
        self.assertTrue(len(notification.subscription.transactions) == 1)

        transaction = notification.subscription.transactions.pop()

        self.assertEqual("failed", transaction.status)
        self.assertEqual(Decimal("49.99"), transaction.amount)

    def test_builds_notification_for_check(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.Check,
            ""
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.Check, notification.kind)

    def test_builds_notification_for_account_updater_daily_report_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.AccountUpdaterDailyReport,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])

        self.assertEqual(WebhookNotification.Kind.AccountUpdaterDailyReport, notification.kind)
        self.assertEqual("link-to-csv-report", notification.account_updater_daily_report.report_url)
        self.assertEqual(date(2016, 1, 14), notification.account_updater_daily_report.report_date)

    def test_grantor_updated_granted_payment_method_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.GrantorUpdatedGrantedPaymentMethod,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        update = notification.granted_payment_instrument_update

        self.assertEqual(WebhookNotification.Kind.GrantorUpdatedGrantedPaymentMethod, notification.kind)
        self.assertEqual("vczo7jqrpwrsi2px", update.grant_owner_merchant_id)
        self.assertEqual("cf0i8wgarszuy6hc", update.grant_recipient_merchant_id)
        self.assertEqual("ee257d98-de40-47e8-96b3-a6954ea7a9a4", update.payment_method_nonce)
        self.assertEqual("abc123z", update.token)
        self.assertEqual(["expiration-month", "expiration-year"], update.updated_fields)

    def test_recipient_updated_granted_payment_method_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.RecipientUpdatedGrantedPaymentMethod,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        update = notification.granted_payment_instrument_update

        self.assertEqual(WebhookNotification.Kind.RecipientUpdatedGrantedPaymentMethod, notification.kind)
        self.assertEqual("vczo7jqrpwrsi2px", update.grant_owner_merchant_id)
        self.assertEqual("cf0i8wgarszuy6hc", update.grant_recipient_merchant_id)
        self.assertEqual("ee257d98-de40-47e8-96b3-a6954ea7a9a4", update.payment_method_nonce)
        self.assertEqual("abc123z", update.token)
        self.assertEqual(["expiration-month", "expiration-year"], update.updated_fields)

    def test_granted_payment_method_revoked_credit_card_webhook(self):
        xml_payload = """
            <notification>
                <source-merchant-id>12345</source-merchant-id>
                <timestamp type="datetime">2018-10-10T22:46:41Z</timestamp>
                <kind>granted_payment_method_revoked</kind>
                <subject>
                    <credit-card>
                        <bin>555555</bin>
                        <card-type>MasterCard</card-type>
                        <cardholder-name>Amber Ankunding</cardholder-name>
                        <commercial>Unknown</commercial>
                        <country-of-issuance>Unknown</country-of-issuance>
                        <created-at type="datetime">2018-10-10T22:46:41Z</created-at>
                        <customer-id>credit_card_customer_id</customer-id>
                        <customer-location>US</customer-location>
                        <debit>Unknown</debit>
                        <default type="boolean">true</default>
                        <durbin-regulated>Unknown</durbin-regulated>
                        <expiration-month>06</expiration-month>
                        <expiration-year>2020</expiration-year>
                        <expired type="boolean">false</expired>
                        <global-id>cGF5bWVudG1ldGhvZF8zcHQ2d2hz</global-id>
                        <healthcare>Unknown</healthcare>
                        <image-url>https://assets.braintreegateway.com/payment_method_logo/mastercard.png?environment=test</image-url>
                        <issuing-bank>Unknown</issuing-bank>
                        <last-4>4444</last-4>
                        <payroll>Unknown</payroll>
                        <prepaid>Unknown</prepaid>
                        <prepaid-reloadable>Unknown</prepaid-reloadable>
                        <product-id>Unknown</product-id>
                        <subscriptions type="array"/>
                        <token>credit_card_token</token>
                        <unique-number-identifier>08199d188e37460163207f714faf074a</unique-number-identifier>
                        <updated-at type="datetime">2018-10-10T22:46:41Z</updated-at>
                        <venmo-sdk type="boolean">false</venmo-sdk>
                        <verifications type="array"/>
                    </credit-card>
                </subject>
            </notification>
            """.encode("utf-8")
        sample_notification = TestHelper.sample_notification_from_xml(xml_payload)

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        metadata = notification.revoked_payment_method_metadata

        self.assertEqual(WebhookNotification.Kind.GrantedPaymentMethodRevoked, notification.kind)
        self.assertEqual("credit_card_customer_id", metadata.customer_id)
        self.assertEqual("credit_card_token", metadata.token)
        self.assertTrue(isinstance(metadata.revoked_payment_method, CreditCard))

    def test_granted_payment_method_revoked_paypal_account_webhook(self):
        xml_payload = """
            <notification>
                <source-merchant-id>12345</source-merchant-id>
                <timestamp type="datetime">2018-10-10T22:46:41Z</timestamp>
                <kind>granted_payment_method_revoked</kind>
                <subject>
                    <paypal-account>
                        <billing-agreement-id>billing_agreement_id</billing-agreement-id>
                        <created-at type="dateTime">2018-10-11T21:10:33Z</created-at>
                        <customer-id>paypal_customer_id</customer-id>
                        <default type="boolean">true</default>
                        <email>johndoe@example.com</email>
                        <global-id>cGF5bWVudG1ldGhvZF9wYXlwYWxfdG9rZW4</global-id>
                        <image-url>https://assets.braintreegateway.com/payment_method_logo/mastercard.png?environment=test</image-url>
                        <subscriptions type="array"></subscriptions>
                        <token>paypal_token</token>
                        <updated-at type="dateTime">2018-10-11T21:10:33Z</updated-at>
                        <payer-id>a6a8e1a4</payer-id>
                    </paypal-account>
                </subject>
            </notification>
            """.encode("utf-8")
        sample_notification = TestHelper.sample_notification_from_xml(xml_payload)
        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        metadata = notification.revoked_payment_method_metadata

        self.assertEqual(WebhookNotification.Kind.GrantedPaymentMethodRevoked, notification.kind)
        self.assertEqual("paypal_customer_id", metadata.customer_id)
        self.assertEqual("paypal_token", metadata.token)
        self.assertTrue(isinstance(metadata.revoked_payment_method, PayPalAccount))

    def test_granted_payment_method_revoked_venmo_account_webhook(self):
        xml_payload = """
            <notification>
                <source-merchant-id>12345</source-merchant-id>
                <timestamp type="datetime">2018-10-10T22:46:41Z</timestamp>
                <kind>granted_payment_method_revoked</kind>
                <subject>
                    <venmo-account>
                        <created-at type="dateTime">2018-10-11T21:28:37Z</created-at>
                        <updated-at type="dateTime">2018-10-11T21:28:37Z</updated-at>
                        <default type="boolean">true</default>
                        <image-url>https://assets.braintreegateway.com/payment_method_logo/mastercard.png?environment=test</image-url>
                        <token>venmo_token</token>
                        <source-description>Venmo Account: venmojoe</source-description>
                        <username>venmojoe</username>
                        <venmo-user-id>456</venmo-user-id>
                        <subscriptions type="array"/>
                        <customer-id>venmo_customer_id</customer-id>
                        <global-id>cGF5bWVudG1ldGhvZF92ZW5tb2FjY291bnQ</global-id>
                    </venmo-account>
                </subject>
            </notification>
            """.encode("utf-8")
        sample_notification = TestHelper.sample_notification_from_xml(xml_payload)

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        metadata = notification.revoked_payment_method_metadata

        self.assertEqual(WebhookNotification.Kind.GrantedPaymentMethodRevoked, notification.kind)
        self.assertEqual("venmo_customer_id", metadata.customer_id)
        self.assertEqual("venmo_token", metadata.token)
        self.assertTrue(isinstance(metadata.revoked_payment_method, VenmoAccount))

    def test_payment_method_revoked_by_customer_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.PaymentMethodRevokedByCustomer,
            "my_payment_method_token"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        metadata = notification.revoked_payment_method_metadata

        self.assertEqual(WebhookNotification.Kind.PaymentMethodRevokedByCustomer, notification.kind)
        self.assertEqual("my_payment_method_token", metadata.token)
        self.assertTrue(isinstance(metadata.revoked_payment_method, PayPalAccount))
        self.assertNotEqual(None, metadata.revoked_payment_method.revoked_at)

    def test_local_payment_completed_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.LocalPaymentCompleted,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        local_payment_completed = notification.local_payment_completed

        self.assertEqual(WebhookNotification.Kind.LocalPaymentCompleted, notification.kind)
        self.assertEqual("a-bic", local_payment_completed.bic)
        self.assertEqual("1234", local_payment_completed.iban_last_chars)
        self.assertEqual("a-payer-id", local_payment_completed.payer_id)
        self.assertEqual("a-payer-name", local_payment_completed.payer_name)
        self.assertEqual("a-payment-id", local_payment_completed.payment_id)
        self.assertEqual("ee257d98-de40-47e8-96b3-a6954ea7a9a4", local_payment_completed.payment_method_nonce)
        self.assertTrue(isinstance(local_payment_completed.transaction, Transaction))

    def test_local_payment_completed_webhook_blik_one_click(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.LocalPaymentCompleted,
            "blik_one_click_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        local_payment_completed = notification.local_payment_completed

        self.assertEqual(WebhookNotification.Kind.LocalPaymentCompleted, notification.kind)
        self.assertEqual("1234", local_payment_completed.iban_last_chars)
        self.assertEqual("a-bic", local_payment_completed.bic)
        self.assertEqual('alias-key-1', local_payment_completed.blik_aliases[0].key)
        self.assertEqual('alias-label-1', local_payment_completed.blik_aliases[0].label)
        self.assertEqual("a-payer-id", local_payment_completed.payer_id)
        self.assertEqual("a-payer-name", local_payment_completed.payer_name)
        self.assertEqual("a-payment-id", local_payment_completed.payment_id)
        self.assertEqual("ee257d98-de40-47e8-96b3-a6954ea7a9a4", local_payment_completed.payment_method_nonce)
        self.assertTrue(isinstance(local_payment_completed.transaction, Transaction))

    def test_local_payment_expired_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.LocalPaymentExpired,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        local_payment_expired = notification.local_payment_expired

        self.assertEqual(WebhookNotification.Kind.LocalPaymentExpired, notification.kind)
        self.assertEqual("a-payment-id", local_payment_expired.payment_id)
        self.assertEqual("a-context-payment-id", local_payment_expired.payment_context_id)

    def test_local_payment_funded_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.LocalPaymentFunded,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        local_payment_funded = notification.local_payment_funded

        self.assertEqual(WebhookNotification.Kind.LocalPaymentFunded, notification.kind)
        self.assertEqual("a-payment-id", local_payment_funded.payment_id)
        self.assertEqual("a-context-payment-id", local_payment_funded.payment_context_id)
        self.assertTrue(isinstance(local_payment_funded.transaction, Transaction))
        self.assertEqual("1", local_payment_funded.transaction.id)
        self.assertEqual("settled", local_payment_funded.transaction.status)
        self.assertEqual("order1234", local_payment_funded.transaction.order_id)

    def test_local_payment_reversed_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.LocalPaymentReversed,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        local_payment_reversed = notification.local_payment_reversed

        self.assertEqual(WebhookNotification.Kind.LocalPaymentReversed, notification.kind)
        self.assertEqual("a-payment-id", local_payment_reversed.payment_id)

    def test_payment_method_customer_data_updated_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.PaymentMethodCustomerDataUpdated,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        payment_method_customer_data_updated = notification.payment_method_customer_data_updated_metadata

        self.assertEqual(WebhookNotification.Kind.PaymentMethodCustomerDataUpdated, notification.kind)

        self.assertEqual(payment_method_customer_data_updated.token, "TOKEN-12345")
        self.assertEqual(payment_method_customer_data_updated.datetime_updated, "2022-01-01T21:28:37Z")

        enriched_customer_data = payment_method_customer_data_updated.enriched_customer_data
        self.assertEqual(enriched_customer_data.fields_updated, ["username"])

        address = {
            "street_address": "Street Address",
            "extended_address": "Extended Address",
            "locality": "Locality",
            "region": "Region",
            "postal_code":"Postal Code"
        }

        profile_data = enriched_customer_data.profile_data
        self.assertEqual(profile_data.first_name, "John")
        self.assertEqual(profile_data.last_name, "Doe")
        self.assertEqual(profile_data.username, "venmo_username")
        self.assertEqual(profile_data.phone_number, "1231231234")
        self.assertEqual(profile_data.email, "john.doe@paypal.com")
        self.assertEqual(profile_data.billing_address, address)
        self.assertEqual(profile_data.shipping_address, address)
