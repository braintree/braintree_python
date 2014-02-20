from tests.test_helper import *

class TestWebhooks(unittest.TestCase):
    def test_sample_notification_builds_a_parsable_notification(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.SubscriptionWentPastDue, notification.kind)
        self.assertEquals("my_id", notification.subscription.id)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)

    @raises(InvalidSignatureError)
    def test_invalid_signature(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        WebhookNotification.parse("bad_stuff", payload)

    @raises(InvalidSignatureError)
    def test_modified_signature(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        WebhookNotification.parse(signature[:-1] + "!", payload)

    @raises(InvalidSignatureError)
    def test_invalid_public_key(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionWentPastDue,
            "my_id"
        )

        WebhookNotification.parse("bad_stuff" + signature, payload)

    def test_verify_returns_a_correct_challenge_response(self):
        response = WebhookNotification.verify("verification_token")
        self.assertEquals("integration_public_key|c9f15b74b0d98635cd182c51e2703cffa83388c3", response)

    def test_builds_notification_for_approved_sub_merchant_account(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubMerchantAccountApproved,
            "my_id"
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.SubMerchantAccountApproved, notification.kind)
        self.assertEquals("my_id", notification.merchant_account.id)
        self.assertEquals(MerchantAccount.Status.Active, notification.merchant_account.status)
        self.assertEquals("master_ma_for_my_id", notification.merchant_account.master_merchant_account.id)
        self.assertEquals(MerchantAccount.Status.Active, notification.merchant_account.master_merchant_account.status)

    def test_builds_notification_for_declined_sub_merchant_account(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubMerchantAccountDeclined,
            "my_id"
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.SubMerchantAccountDeclined, notification.kind)
        self.assertEquals("my_id", notification.merchant_account.id)
        self.assertEquals(MerchantAccount.Status.Suspended, notification.merchant_account.status)
        self.assertEquals("master_ma_for_my_id", notification.merchant_account.master_merchant_account.id)
        self.assertEquals(MerchantAccount.Status.Suspended, notification.merchant_account.master_merchant_account.status)
        self.assertEquals("Credit score is too low", notification.message)
        self.assertEquals(ErrorCodes.MerchantAccount.DeclinedOFAC, notification.errors.for_object("merchant_account").on("base")[0].code)

    def test_builds_notification_for_disbursed_transactions(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.TransactionDisbursed,
            "my_id"
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.TransactionDisbursed, notification.kind)
        self.assertEquals("my_id", notification.transaction.id)
        self.assertEquals(100, notification.transaction.amount)
        self.assertEquals(datetime(2013, 7, 9, 18, 23, 29), notification.transaction.disbursement_details.disbursement_date)

    def test_builds_notification_for_disbursement_exceptions(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.TransferException,
            "my_id"
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.TransferException, notification.kind)
        self.assertEquals("my_id", notification.disbursement_exception.id)
        self.assertEquals(100, notification.disbursement_exception.amount)
        self.assertEquals("invalid_account_number", notification.disbursement_exception.message)
        self.assertEquals("update", notification.disbursement_exception.follow_up_action)
        self.assertEquals(date(2013, 7, 9), notification.disbursement_exception.disbursement_date)

    def test_builds_notification_for_partner_merchant_connected(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.PartnerMerchantConnected,
            "my_id"
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.PartnerMerchantConnected, notification.kind)
        self.assertEquals("abc123", notification.partner_merchant.partner_merchant_id)
        self.assertEquals("public_key", notification.partner_merchant.public_key)
        self.assertEquals("private_key", notification.partner_merchant.private_key)
        self.assertEquals("public_id", notification.partner_merchant.merchant_public_id)
        self.assertEquals("cse_key", notification.partner_merchant.client_side_encryption_key)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)

    def test_builds_notification_for_partner_merchant_disconnected(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.PartnerMerchantDisconnected,
            "my_id"
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.PartnerMerchantDisconnected, notification.kind)
        self.assertEquals("abc123", notification.partner_merchant.partner_merchant_id)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)

    def test_builds_notification_for_partner_merchant_declined(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.PartnerMerchantDeclined,
            "my_id"
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.PartnerMerchantDeclined, notification.kind)
        self.assertEquals("abc123", notification.partner_merchant.partner_merchant_id)
        self.assertTrue((datetime.utcnow() - notification.timestamp).seconds < 10)
