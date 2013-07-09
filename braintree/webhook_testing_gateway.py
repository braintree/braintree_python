from braintree.util.crypto import Crypto
from braintree.webhook_notification import WebhookNotification
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
        """ % (timestamp, kind, self.__subject_sample_xml(kind, id))

    def __subject_sample_xml(self, kind, id):
        if kind == WebhookNotification.Kind.SubMerchantAccountApproved:
            return self.__merchant_account_approved_sample_xml(id)
        elif kind == WebhookNotification.Kind.SubMerchantAccountDeclined:
            return self.__merchant_account_declined_sample_xml(id)
        elif kind == WebhookNotification.Kind.TransactionDisbursed:
            return self.__transaction_disbursed_sample_xml(id)
        else:
            return self.__subscription_sample_xml(id)

    def __transaction_disbursed_sample_xml(self, id):
        return """
            <transaction>
              <id>%s</id>
              <amount>100</amount>
              <tax-amount>10</tax-amount>
              <disbursement-details>
                <settlement-amount>100</settlement-amount>
                <settlement-currency-exchange-rate>10</settlement-currency-exchange-rate>
                <disbursement-date type="datetime">2013-07-09T18:23:29Z</disbursement-date>
              </disbursement-details>
            </transaction>
        """ % id

    def __subscription_sample_xml(self, id):
        return """
            <subscription>
                <id>%s</id>
                <transactions type="array"></transactions>
                <add_ons type="array"></add_ons>
                <discounts type="array"></discounts>
            </subscription>
        """ % id

    def __merchant_account_approved_sample_xml(self, id):
        return """
            <merchant-account>
                <id>%s</id>
                <status>active</status>
                <master-merchant-account>
                    <id>master_ma_for_%s</id>
                    <status>active</status>
                </master-merchant-account>
            </merchant-account>
        """ % (id, id)

    def __merchant_account_declined_sample_xml(self, id):
        return """
            <api-error-response>
                <message>Credit score is too low</message>
                <errors>
                    <errors type="array"/>
                        <merchant-account>
                            <errors type="array">
                                <error>
                                    <code>82621</code>
                                    <message>Credit score is too low</message>
                                    <attribute type="symbol">base</attribute>
                                </error>
                            </errors>
                        </merchant-account>
                    </errors>
                    <merchant-account>
                        <id>%s</id>
                        <status>suspended</status>
                        <master-merchant-account>
                            <id>master_ma_for_%s</id>
                            <status>suspended</status>
                        </master-merchant-account>
                    </merchant-account>
            </api-error-response>
            """ % (id, id)
