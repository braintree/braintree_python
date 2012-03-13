from tests.test_helper import *

class TestWebhooks(unittest.TestCase):
    def test_sample_notification_builds_a_parsable_notification(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionPastDue,
            "my_id"
        )

        notification = WebhookNotification.parse(signature, payload)

        self.assertEquals(WebhookNotification.Kind.SubscriptionPastDue, notification.kind)
        self.assertEquals("my_id", notification.subscription.id)
        self.assertTrue((datetime.utcnow() - notification.timestamp).total_seconds() < 10)

    @raises(InvalidSignatureError)
    def test_invalid_signature(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionPastDue,
            "my_id"
        )

        WebhookNotification.parse("bad_stuff", payload)

    @raises(InvalidSignatureError)
    def test_modified_signature(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionPastDue,
            "my_id"
        )

        WebhookNotification.parse(signature + "bad_stuff", payload)

    @raises(InvalidSignatureError)
    def test_invalid_public_key(self):
        signature, payload = WebhookTesting.sample_notification(
            WebhookNotification.Kind.SubscriptionPastDue,
            "my_id"
        )

        WebhookNotification.parse("bad_stuff" + signature, payload)

    def test_verify_returns_a_correct_challenge_response(self):
        response = WebhookNotification.verify("verification_token")
        self.assertEquals("integration_public_key|c9f15b74b0d98635cd182c51e2703cffa83388c3", response)
