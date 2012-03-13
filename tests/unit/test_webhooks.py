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
