from braintree.util.crypto import Crypto
from braintree.webhook_notification import WebhookNotification
import base64
from datetime import datetime

class WebhookTestingGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def sample_notification(self, kind, data):
        if not isinstance(data, dict):
            data = {"id": data}

        payload = base64.encodestring(self.__sample_xml(kind, data))
        hmac_payload = Crypto.hmac_hash(self.gateway.config.private_key, payload)
        signature = "%s|%s" % (self.gateway.config.public_key, hmac_payload)
        return signature, payload

    def __sample_xml(self, kind, data):
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return """
            <notification>
                <timestamp type="datetime">%s</timestamp>
                <kind>%s</kind>
                <subject>%s</subject>
            </notification>
        """ % (timestamp, kind, self.__subject_sample_xml(kind, data))

    def __subject_sample_xml(self, kind, data):
        if kind == WebhookNotification.Kind.SubMerchantAccountApproved:
            return self.__merchant_account_sample_xml(data)
        elif kind == WebhookNotification.Kind.SubMerchantAccountDeclined:
            return self.__merchant_account_declined_sample_xml(data)
        else:
            return self.__subscription_sample_xml(data)

    def __subscription_sample_xml(self, data):
        return """
            <subscription>
                <id>%s</id>
                <transactions type="array"></transactions>
                <add_ons type="array"></add_ons>
                <discounts type="array"></discounts>
            </subscription>
        """ % data["id"]

    def __merchant_account_sample_xml(self, data):
        sub_merchant_account_id = data["id"]
        sub_merchant_account_status = data["status"]
        master_merchant_account_id = data["master_merchant_account"]["id"]
        master_merchant_account_status = data["master_merchant_account"]["status"]
        return """
            <merchant_account>
                <id>%s</id>
                    <master_merchant_account>
                        <id>%s</id>
                        <status>%s</status>
                    </master_merchant_account>
                <status>%s</status>
            </merchant_account>
        """ % (sub_merchant_account_id, master_merchant_account_id, master_merchant_account_status, sub_merchant_account_status)

    def __merchant_account_declined_sample_xml(self, data):
        message = data["message"]
        return """
            <api-error-response>
              <message>%s</message>
              <errors>
                <merchant-account>
                  <errors type="array">%s</errors>
                </merchant-account>
              </errors>
              %s
            </api-error-response>
        """ % (message, self.__errors_sample_xml(data["errors"]), self.__merchant_account_sample_xml(data["merchant_account"]))

    def __errors_sample_xml(self, errors):
        return "\n".join([self.__error_sample_xml(error) for error in errors])

    def __error_sample_xml(self, error):
        attribute = error["attribute"]
        code = error["code"]
        message = error["message"]
        return """
            <error>
                <attribute>%s</attribute>
                <code>%s</code>
                <message>%s</message>
            </error>
        """ % (attribute, code, message)
