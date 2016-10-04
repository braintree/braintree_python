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
        hmac_payload = Crypto.sha1_hmac_hash(self.gateway.config.private_key, payload)
        signature = "%s|%s" % (self.gateway.config.public_key, hmac_payload)
        return {'bt_signature': signature, 'bt_payload': payload}

    def __sample_xml(self, kind, id):
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        sample_xml = """
            <notification>
                <timestamp type="datetime">%s</timestamp>
                <kind>%s</kind>
                <subject>%s</subject>
            </notification>
        """ % (timestamp, kind, self.__subject_sample_xml(kind, id))
        return sample_xml.encode('utf-8')

    def __subject_sample_xml(self, kind, id):
        if kind == WebhookNotification.Kind.Check:
            return self.__check_sample_xml()
        if kind == WebhookNotification.Kind.SubMerchantAccountApproved:
            return self.__merchant_account_approved_sample_xml(id)
        elif kind == WebhookNotification.Kind.SubMerchantAccountDeclined:
            return self.__merchant_account_declined_sample_xml(id)
        elif kind == WebhookNotification.Kind.TransactionDisbursed:
            return self.__transaction_disbursed_sample_xml(id)
        elif kind == WebhookNotification.Kind.TransactionSettled:
            return self.__transaction_settled_sample_xml(id)
        elif kind == WebhookNotification.Kind.TransactionSettlementDeclined:
            return self.__transaction_settlement_declined_sample_xml(id)
        elif kind == WebhookNotification.Kind.PartnerMerchantConnected:
            return self.__partner_merchant_connected_sample_xml()
        elif kind == WebhookNotification.Kind.PartnerMerchantDisconnected:
            return self.__partner_merchant_disconnected_sample_xml()
        elif kind == WebhookNotification.Kind.PartnerMerchantDeclined:
            return self.__partner_merchant_declined_sample_xml()
        elif kind == WebhookNotification.Kind.DisbursementException:
            return self.__disbursement_exception_sample_xml(id)
        elif kind == WebhookNotification.Kind.Disbursement:
            return self.__disbursement_sample_xml(id)
        elif kind == WebhookNotification.Kind.DisputeOpened:
            return self.__dispute_opened_sample_xml(id)
        elif kind == WebhookNotification.Kind.DisputeLost:
            return self.__dispute_lost_sample_xml(id)
        elif kind == WebhookNotification.Kind.DisputeWon:
            return self.__dispute_won_sample_xml(id)
        elif kind == WebhookNotification.Kind.SubscriptionChargedSuccessfully:
            return self.__subscription_charged_successfully_sample_xml(id)
        elif kind == WebhookNotification.Kind.AccountUpdaterDailyReport:
            return self.__account_updater_daily_report_sample_xml()
        else:
            return self.__subscription_sample_xml(id)

    def __check_sample_xml(self):
        return """
            <check type="boolean">
              true
            </check>
        """

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

    def __transaction_settled_sample_xml(self, id):
        return """
            <transaction>
              <id>%s</id>
              <status>settled</status>
              <type>sale</type>
              <currency-iso-code>USD</currency-iso-code>
              <amount>100.00</amount>
              <merchant-account-id>ogaotkivejpfayqfeaimuktty</merchant-account-id>
              <payment-instrument-type>us_bank_account</payment-instrument-type>
              <us-bank-account>
                <routing-number>123456789</routing-number>
                <last-4>1234</last-4>
                <account-type>checking</account-type>
                <account-description>PayPal Checking - 1234</account-description>
                <account-holder-name>Dan Schulman</account-holder-name>
              </us-bank-account>
              <tax-amount>0</tax-amount>
            </transaction>
        """ % id

    def __transaction_settlement_declined_sample_xml(self, id):
        return """
            <transaction>
              <id>%s</id>
              <status>settlement_declined</status>
              <type>sale</type>
              <currency-iso-code>USD</currency-iso-code>
              <amount>100.00</amount>
              <merchant-account-id>ogaotkivejpfayqfeaimuktty</merchant-account-id>
              <payment-instrument-type>us_bank_account</payment-instrument-type>
              <us-bank-account>
                <routing-number>123456789</routing-number>
                <last-4>1234</last-4>
                <account-type>checking</account-type>
                <account-description>PayPal Checking - 1234</account-description>
                <account-holder-name>Dan Schulman</account-holder-name>
              </us-bank-account>
              <tax-amount>0</tax-amount>
            </transaction>
        """ % id

    def __disbursement_exception_sample_xml(self, id):
        return """
            <disbursement>
              <id>%s</id>
              <transaction-ids type="array">
                <item>afv56j</item>
                <item>kj8hjk</item>
              </transaction-ids>
              <success type="boolean">false</success>
              <retry type="boolean">false</retry>
              <merchant-account>
                <id>merchant_account_token</id>
                <currency-iso-code>USD</currency-iso-code>
                <sub-merchant-account type="boolean">false</sub-merchant-account>
                <status>active</status>
              </merchant-account>
              <amount>100.00</amount>
              <disbursement-date type="date">2014-02-09</disbursement-date>
              <exception-message>bank_rejected</exception-message>
              <follow-up-action>update_funding_information</follow-up-action>
            </disbursement>
        """ % id

    def __disbursement_sample_xml(self, id):
        return """
            <disbursement>
              <id>%s</id>
              <transaction-ids type="array">
                <item>afv56j</item>
                <item>kj8hjk</item>
              </transaction-ids>
              <success type="boolean">true</success>
              <retry type="boolean">false</retry>
              <merchant-account>
                <id>merchant_account_token</id>
                <currency-iso-code>USD</currency-iso-code>
                <sub-merchant-account type="boolean">false</sub-merchant-account>
                <status>active</status>
              </merchant-account>
              <amount>100.00</amount>
              <disbursement-date type="date">2014-02-09</disbursement-date>
              <exception-message nil="true"/>
              <follow-up-action nil="true"/>
            </disbursement>
        """ % id

    def __dispute_opened_sample_xml(self, id):
        return """
            <dispute>
              <amount>250.00</amount>
              <currency-iso-code>USD</currency-iso-code>
              <received-date type="date">2014-03-01</received-date>
              <reply-by-date type="date">2014-03-21</reply-by-date>
              <kind>chargeback</kind>
              <status>open</status>
              <reason>fraud</reason>
              <id>%s</id>
              <transaction>
                <id>%s</id>
                <amount>250.00</amount>
              </transaction>
              <date-opened type="date">2014-03-28</date-opened>
            </dispute>
        """ % (id, id)

    def __dispute_lost_sample_xml(self, id):
        return """
            <dispute>
              <amount>250.00</amount>
              <currency-iso-code>USD</currency-iso-code>
              <received-date type="date">2014-03-01</received-date>
              <reply-by-date type="date">2014-03-21</reply-by-date>
              <kind>chargeback</kind>
              <status>lost</status>
              <reason>fraud</reason>
              <id>%s</id>
              <transaction>
                <id>%s</id>
                <amount>250.00</amount>
              </transaction>
              <date-opened type="date">2014-03-28</date-opened>
            </dispute>
        """ % (id, id)

    def __dispute_won_sample_xml(self, id):
        return """
            <dispute>
              <amount>250.00</amount>
              <currency-iso-code>USD</currency-iso-code>
              <received-date type="date">2014-03-01</received-date>
              <reply-by-date type="date">2014-03-21</reply-by-date>
              <kind>chargeback</kind>
              <status>won</status>
              <reason>fraud</reason>
              <id>%s</id>
              <transaction>
                <id>%s</id>
                <amount>250.00</amount>
              </transaction>
              <date-opened type="date">2014-03-28</date-opened>
              <date-won type="date">2014-09-01</date-won>
            </dispute>
        """ % (id, id)

    def __subscription_sample_xml(self, id):
        return """
            <subscription>
                <id>%s</id>
                <transactions type="array"></transactions>
                <add_ons type="array"></add_ons>
                <discounts type="array"></discounts>
            </subscription>
        """ % id

    def __subscription_charged_successfully_sample_xml(self, id):
        return """
            <subscription>
                <id>%s</id>
                <transactions type="array">
                    <transaction>
                        <status>submitted_for_settlement</status>
                        <amount>49.99</amount>
                        <tax_amount></tax_amount>
                    </transaction>
                </transactions>
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

    def __partner_merchant_connected_sample_xml(self):
        return """
            <partner-merchant>
                <partner-merchant-id>abc123</partner-merchant-id>
                <public-key>public_key</public-key>
                <private-key>private_key</private-key>
                <merchant-public-id>public_id</merchant-public-id>
                <client-side-encryption-key>cse_key</client-side-encryption-key>
            </partner-merchant>
            """

    def __partner_merchant_disconnected_sample_xml(self):
        return """
            <partner-merchant>
                <partner-merchant-id>abc123</partner-merchant-id>
            </partner-merchant>
            """

    def __partner_merchant_declined_sample_xml(self):
        return """
            <partner-merchant>
                <partner-merchant-id>abc123</partner-merchant-id>
            </partner-merchant>
            """

    def __account_updater_daily_report_sample_xml(self):
        return """
            <account-updater-daily-report>
                <report-date type="date">2016-01-14</report-date>
                <report-url>link-to-csv-report</report-url>
            </account-updater-daily-report>
            """
