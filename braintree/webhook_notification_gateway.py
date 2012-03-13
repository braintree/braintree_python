import base64
from braintree.webhook_notification import WebhookNotification
from braintree.util.xml_util import XmlUtil

class WebhookNotificationGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def parse(self, signature, payload):
        attributes = XmlUtil.dict_from_xml(base64.decodestring(payload))
        return WebhookNotification(self.gateway, attributes['notification'])
