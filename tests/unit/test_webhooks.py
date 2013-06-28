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
            {
                "id": "sub_merchant_account_id",
                "status": MerchantAccount.Status.Active,
                "master_merchant_account": {
                    "id": "master_merchant_account_id",
                    "status": MerchantAccount.Status.Active
                }
            }
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.SubMerchantAccountApproved, notification.kind)
        self.assertEquals("sub_merchant_account_id", notification.merchant_account.id)
        self.assertEquals(MerchantAccount.Status.Active, notification.merchant_account.status)
        self.assertEquals("master_merchant_account_id", notification.merchant_account.master_merchant_account.id)
        self.assertEquals(MerchantAccount.Status.Active, notification.merchant_account.master_merchant_account.status)

    def test_builds_notification_for_declined_sub_merchant_account(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubMerchantAccountDeclined,
            {
                "message": "Applicant declined due to OFAC.",
                "merchant_account": {
                    "id": "sub_merchant_account_id",
                    "status": MerchantAccount.Status.Suspended,
                    "master_merchant_account": {
                        "id": "master_merchant_account_id",
                        "status": MerchantAccount.Status.Active
                    }
                },
                "errors": [{
                    "attribute": "base",
                    "code": "82621",
                    "message": "Applicant declined due to OFAC."
                }]
            }
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.SubMerchantAccountDeclined, notification.kind)
        self.assertEquals("sub_merchant_account_id", notification.errors.merchant_account.id)
        self.assertEquals(MerchantAccount.Status.Suspended, notification.errors.merchant_account.status)
        self.assertEquals("master_merchant_account_id", notification.errors.merchant_account.master_merchant_account.id)
        self.assertEquals(MerchantAccount.Status.Active, notification.errors.merchant_account.master_merchant_account.status)
        self.assertEquals("Applicant declined due to OFAC.", notification.errors.message)
        self.assertEquals(ErrorCodes.MerchantAccount.ApplicantDetails.DeclinedOFAC, notification.errors.errors.for_object("merchant_account").on("base")[0].code)
