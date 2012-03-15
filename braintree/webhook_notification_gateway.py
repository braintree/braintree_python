import base64
from braintree.exceptions.invalid_signature_error import InvalidSignatureError
from braintree.util.crypto import Crypto
from braintree.util.xml_util import XmlUtil
from braintree.webhook_notification import WebhookNotification

class WebhookNotificationGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def parse(self, signature, payload):
        self.__validate_signature(signature, payload)
        attributes = XmlUtil.dict_from_xml(base64.decodestring(payload))
        return WebhookNotification(self.gateway, attributes['notification'])

    def verify(self, challenge):
        digest = Crypto.hmac_hash(self.config.private_key, challenge)
        return "%s|%s" % (self.config.public_key, digest)

    def __matching_signature(self, signature_pairs):
        for public_key, signature in signature_pairs:
            if public_key == self.config.public_key:
                return signature
        return None

    def __validate_signature(self, signature, payload):
        signature_pairs = [pair.split("|") for pair in signature.split("&") if "|" in pair]
        matching_signature = self.__matching_signature(signature_pairs)
        payload_signature = Crypto.hmac_hash(self.config.private_key, payload)

        if not Crypto.secure_compare(payload_signature, matching_signature):
            raise InvalidSignatureError
