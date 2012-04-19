import braintree
from braintree.configuration import Configuration

class WebhookTesting(object):
    @staticmethod
    def sample_notification(kind, id):
        return Configuration.gateway().webhook_testing.sample_notification(kind, id)
