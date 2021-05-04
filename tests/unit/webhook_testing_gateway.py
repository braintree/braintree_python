from tests.test_helper import *
import base64
import xml.etree.ElementTree as ET

class TestWebhookTestingGateway(unittest.TestCase):
    def test_granted_payment_method_revoked(self):
        webhook_testing_gateway = WebhookTestingGateway(BraintreeGateway(Configuration.instantiate()))

        sample_notification = webhook_testing_gateway.sample_notification(WebhookNotification.Kind.GrantedPaymentMethodRevoked, '1234')

        payload = base64.b64decode(sample_notification['bt_payload']).decode('UTF-8')
        tree = ET.fromstring(payload)

        subject = tree.find('subject')

        self.assertEqual('venmo-account', subject.find('venmo-account').tag)
        self.assertEqual('1234', subject.find('venmo-account').find('token').text)
