from tests.test_helper import *
from datetime import date
from braintree.dispute import Dispute

class TestWebhooks(unittest.TestCase):
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

    @raises(InvalidSignatureError)
    def test_completely_invalid_signature(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

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

    def test_ideal_payment_complete_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.IdealPaymentComplete,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])
        ideal_payment = notification.ideal_payment

        self.assertEqual(WebhookNotification.Kind.IdealPaymentComplete, notification.kind)
        self.assertEqual("my_id", ideal_payment.id)
        self.assertEqual("COMPLETE", ideal_payment.status);
        self.assertEqual("ORDERABC", ideal_payment.order_id);
        self.assertEqual("10.00", ideal_payment.amount);
        self.assertEqual("https://example.com", ideal_payment.approval_url);
        self.assertEqual("1234567890", ideal_payment.ideal_transaction_id);

    def test_ideal_payment_failed_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.IdealPaymentFailed,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification['bt_signature'], sample_notification['bt_payload'])
        ideal_payment = notification.ideal_payment

        self.assertEqual(WebhookNotification.Kind.IdealPaymentFailed, notification.kind)
        self.assertEqual("my_id", ideal_payment.id)
        self.assertEqual("FAILED", ideal_payment.status);
        self.assertEqual("ORDERABC", ideal_payment.order_id);
        self.assertEqual("10.00", ideal_payment.amount);
        self.assertEqual("https://example.com", ideal_payment.approval_url);
        self.assertEqual("1234567890", ideal_payment.ideal_transaction_id);

    def test_granted_payment_instrument_update_webhook(self):
        sample_notification = WebhookTesting.sample_notification(
            WebhookNotification.Kind.GrantedPaymentInstrumentUpdate,
            "my_id"
        )

        notification = WebhookNotification.parse(sample_notification["bt_signature"], sample_notification["bt_payload"])
        update = notification.granted_payment_instrument_update

        self.assertEqual(WebhookNotification.Kind.GrantedPaymentInstrumentUpdate, notification.kind)
        self.assertEqual("vczo7jqrpwrsi2px", update.grant_owner_merchant_id)
        self.assertEqual("cf0i8wgarszuy6hc", update.grant_recipient_merchant_id)
        self.assertEqual("ee257d98-de40-47e8-96b3-a6954ea7a9a4", update.payment_method_nonce)
        self.assertEqual("abc123z", update.token)
        self.assertEqual(["expiration-month", "expiration-year"], update.updated_fields)
