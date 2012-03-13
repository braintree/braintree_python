from braintree.util.crypto import Crypto
import base64
from datetime import datetime

class WebhookTestingGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def sample_notification(self, kind, id):
        payload = base64.encodestring(self.__sample_xml(kind, id))
        hmac_payload = Crypto.hmac_hash(self.gateway.config.private_key, payload)
        signature = "%s|%s" % (self.gateway.config.public_key, hmac_payload)
        return signature, payload

    def __sample_xml(self, kind, id):
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return """
            <notification>
                <timestamp type="datetime">%s</timestamp>
                <kind>%s</kind>
                <subject>%s</subject>
            </notification>
        """ % (timestamp, kind, self.__subscription_sample_xml(id))

    def __subscription_sample_xml(self, id):
        return """
            <subscription>
                <id>%s</id>
                <transactions type="array"></transactions>
                <add_ons type="array"></add_ons>
                <discounts type="array"></discounts>
            </subscription>
        """ % id
