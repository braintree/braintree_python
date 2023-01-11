from base64 import b64decode, encodebytes
from contextlib import contextmanager
from datetime import date, datetime, timedelta
from decimal import Decimal
from enum import Enum
from http.client import HTTPConnection
from subprocess import Popen, PIPE
from urllib.parse import urlencode, quote_plus
import json
import os
import random
import re
import requests
import subprocess
import sys
import time
import unittest
import warnings

from braintree import *
from braintree.exceptions import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from braintree.test.nonces import Nonces
from braintree.testing_gateway import *
from braintree.util import *

def reset_braintree_configuration():
    Configuration.configure(
        Environment.Development,
        "integration_merchant_id",
        "integration_public_key",
        "integration_private_key"
    )
reset_braintree_configuration()

class AdvancedFraudKountIntegrationMerchant:
    def __enter__(self):
        Configuration.configure(
            Environment.Development,
            "advanced_fraud_integration_merchant_id",
            "advanced_fraud_integration_public_key",
            "advanced_fraud_integration_private_key"
        )

    def __exit__(self, type, value, trace):
        reset_braintree_configuration()

class FraudProtectionEnterpriseIntegrationMerchant:
    def __enter__(self):
        Configuration.configure(
            Environment.Development,
            "fraud_protection_enterprise_integration_merchant_id",
            "fraud_protection_enterprise_integration_public_key",
            "fraud_protection_enterprise_integration_private_key"
        )

    def __exit__(self, type, value, trace):
        reset_braintree_configuration()

class EffortlessChargebackProtectionMerchant:
    def __enter__(self):
        Configuration.configure(
            Environment.Development,
            "fraud_protection_effortless_chargeback_protection_merchant_id",
            "effortless_chargeback_protection_public_key",
            "effortless_chargeback_protection_private_key"
        )

    def __exit__(self, type, value, trace):
        reset_braintree_configuration()

class DuplicateCheckingMerchant:
    def __enter__(self):
        Configuration.configure(
            Environment.Development,
            "dup_checking_integration_merchant_id",
            "dup_checking_integration_public_key",
            "dup_checking_integration_private_key"
        )

    def __exit__(self, type, value, trace):
        reset_braintree_configuration()

def showwarning(*_):
    pass
warnings.showwarning = showwarning

class TestHelper(object):
    default_merchant_account_id = "sandbox_credit_card"
    non_default_merchant_account_id = "sandbox_credit_card_non_default"
    non_default_sub_merchant_account_id = "sandbox_sub_merchant_account"
    three_d_secure_merchant_account_id = "three_d_secure_merchant_account"
    fake_amex_direct_merchant_account_id = "fake_amex_direct_usd"
    fake_venmo_account_merchant_account_id = "fake_first_data_venmo_account"
    fake_first_data_merchant_account_id = "fake_first_data_merchant_account"
    us_bank_merchant_account_id = "us_bank_merchant_account"
    another_us_bank_merchant_account_id = "another_us_bank_merchant_account"
    adyen_merchant_account_id = "adyen_ma"
    hiper_brl_merchant_account_id = "hiper_brl"
    card_processor_brl_merchant_account_id = "card_processor_brl"
    aib_swe_ma_merchant_account_id = "aib_swe_ma"

    add_on_discount_plan = {
         "description": "Plan for integration tests -- with add-ons and discounts",
         "id": "integration_plan_with_add_ons_and_discounts",
         "price": Decimal("9.99"),
         "trial_duration": 2,
         "trial_duration_unit": Subscription.TrialDurationUnit.Day,
         "trial_period": True
    }

    billing_day_of_month_plan = {
         "description": "Plan for integration tests -- with billing day of month",
         "id": "integration_plan_with_billing_day_of_month",
         "billing_day_of_month": 5,
         "price": Decimal("8.88"),
    }

    trial_plan = {
        "description": "Plan for integration tests -- with trial",
        "id": "integration_trial_plan",
        "price": Decimal("43.21"),
        "trial_period": True,
        "trial_duration": 2,
        "trial_duration_unit": Subscription.TrialDurationUnit.Day
    }

    trialless_plan = {
        "description": "Plan for integration tests -- without a trial",
        "id": "integration_trialless_plan",
        "price": Decimal("12.34"),
        "trial_period": False
    }

    valid_token_characters = list("bcdfghjkmnpqrstvwxyz23456789")
    text_type = str
    raw_type = bytes

    @staticmethod
    def make_past_due(subscription, number_of_days_past_due=1):
        Configuration.gateway().testing.make_past_due(subscription.id, number_of_days_past_due)

    @staticmethod
    def escrow_transaction(transaction_id):
        Configuration.gateway().testing.escrow_transaction(transaction_id)

    @staticmethod
    def settle_transaction(transaction_id):
        return Configuration.gateway().testing.settle_transaction(transaction_id)

    @staticmethod
    def settlement_confirm_transaction(transaction_id):
        return Configuration.gateway().testing.settlement_confirm_transaction(transaction_id)

    @staticmethod
    def settlement_decline_transaction(transaction_id):
        return Configuration.gateway().testing.settlement_decline_transaction(transaction_id)

    @staticmethod
    def settlement_pending_transaction(transaction_id):
        return Configuration.gateway().testing.settlement_pending_transaction(transaction_id)

    @staticmethod
    def create_3ds_verification(merchant_account_id, params):
        return Configuration.gateway().testing.create_3ds_verification(merchant_account_id, params)

    @staticmethod
    @contextmanager
    def other_merchant(merchant_id, public_key, private_key):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        Configuration.merchant_id = merchant_id
        Configuration.public_key = public_key
        Configuration.private_key = private_key

        try:
            yield
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    @staticmethod
    def includes(collection, expected):
        for item in collection.items:
            if item.id == expected.id:
                return True
        return False

    @staticmethod
    def in_list(collection, expected):
        for item in collection:
            if item == expected:
                return True
        return False

    @staticmethod
    def includes_status(collection, status):
        for item in collection.items:
            if item.status == status:
                return True
        return False

    @staticmethod
    def now_minus_offset(offset):
        now = datetime.utcnow()
        return (now - timedelta(hours=offset)).strftime("%Y-%m-%d")

    @staticmethod
    def unique(some_list):
        return set(some_list)

    @staticmethod
    def __headers():
        return {
            "Accept": "application/xml",
            "Content-type": "application/x-www-form-urlencoded",
        }

    @staticmethod
    def generate_decoded_client_token(params=None):
        client_token = None
        if params:
            client_token = ClientToken.generate(params)
        else:
            client_token = ClientToken.generate()

        decoded_client_token = b64decode(client_token).decode()
        return decoded_client_token

    @staticmethod
    def nonce_for_paypal_account(paypal_account_details):
        client_token = json.loads(TestHelper.generate_decoded_client_token())
        client = ClientApiHttp(Configuration.instantiate(), {
            "authorization_fingerprint": client_token["authorizationFingerprint"]
        })

        _, nonce = client.get_paypal_nonce(paypal_account_details)
        return nonce

    @staticmethod
    def random_token_block(x):
        string = ""
        for i in range(6):
            string += random.choice(TestHelper.valid_token_characters)
        return string

    @staticmethod
    def generate_valid_us_bank_account_nonce(routing_number="021000021", account_number="567891234"):
        query = '''
          mutation TokenizeUsBankAccount($input: TokenizeUsBankAccountInput!) {
            tokenizeUsBankAccount(input: $input) {
              paymentMethod {
                id
              }
            }
          }
        '''

        variables = {
            "input": {
                "usBankAccount": {
                    "accountNumber": account_number,
                    "routingNumber": routing_number,
                    "accountType": "CHECKING",
                    "individualOwner": {
                        "firstName": "Dan",
                        "lastName": "Schulman"
                     },
                    "achMandate": "cl mandate text",
                    "billingAddress": {
                        "streetAddress": "123 Ave",
                        "state": "CA",
                        "city": "San Francisco",
                        "zipCode": "94112"
                     }
                }
            }
        }

        graphql_request = {
            "query": query,
            "variables": variables
        }

        response = TestHelper.__send_graphql_request(graphql_request)
        return response["data"]["tokenizeUsBankAccount"]["paymentMethod"]["id"]

    @staticmethod
    def generate_plaid_us_bank_account_nonce():
        query = '''
          mutation TokenizeUsBankLogin($input: TokenizeUsBankLoginInput!) {
            tokenizeUsBankLogin(input: $input) {
              paymentMethod {
                id
              }
            }
          }
        '''

        variables = {
            "input": {
                "usBankLogin": {
                    "publicToken": "good",
                    "accountId": "plaid_account_id",
                    "accountType": "CHECKING",
                    "businessOwner": {
                        "businessName": "PayPal, Inc."
                     },
                    "achMandate": "cl mandate text",
                    "billingAddress": {
                        "streetAddress": "123 Ave",
                        "state": "CA",
                        "city": "San Francisco",
                        "zipCode": "94112"
                     }
                }
            }
        }

        graphql_request = {
            "query": query,
            "variables": variables
        }

        response = TestHelper.__send_graphql_request(graphql_request)
        return response["data"]["tokenizeUsBankLogin"]["paymentMethod"]["id"]

    @staticmethod
    def generate_invalid_us_bank_account_nonce():
        token = "tokenusbankacct"
        for i in range(4):
            token += "_" + TestHelper.random_token_block('d')
        token += "_xxx"
        return token

    @staticmethod
    def generate_three_d_secure_nonce(gateway, params):
        url = gateway.config.base_merchant_path() + "/three_d_secure/create_nonce/" + TestHelper.three_d_secure_merchant_account_id
        response = gateway.config.http().post(url, params)
        return response["payment_method_nonce"]["nonce"]

    @staticmethod
    def create_disputed_transaction():
        if hasattr(TestHelper, 'disputed_transaction'):
            return TestHelper.disputed_transaction

        disputed_transaction = Transaction.sale({
            "amount": "10.00",
            "credit_card": {
                "number": CreditCardNumbers.Disputes.Chargeback,
                "expiration_date": "04/2018"
                }
            })

        for _ in range(1, 60):
            transactions = Transaction.search([
                TransactionSearch.id == disputed_transaction.transaction.id,
                TransactionSearch.dispute_date == datetime.today()
            ])

            if transactions.maximum_size == 1:
                TestHelper.disputed_transaction = transactions.first
                return TestHelper.disputed_transaction
            else:
                time.sleep(1)

        raise ValueError('Disputed transaction could not be found')

    @staticmethod
    def create_grant(gateway, params):
        config = gateway.config
        response = config.http().post("/oauth_testing/grants", {
            "grant": params
        })

        return response["grant"]["code"]

    @staticmethod
    def create_payment_method_grant_fixtures():
        config = Configuration(
            merchant_id="integration_merchant_public_id",
            public_key="oauth_app_partner_user_public_key",
            private_key="oauth_app_partner_user_private_key",
            environment=Environment.Development
        )

        gateway = BraintreeGateway(config)
        customer = gateway.customer.create().customer
        credit_card = gateway.credit_card.create(
            params={
                "customer_id": customer.id,
                "number": "4111111111111111",
                "expiration_date": "05/2009",
                "billing_address": {
                    "first_name": "Jon",
                    "last_name": "Doe",
                    "postal_code": "95131"
                }
            }
        ).credit_card

        oauth_app_gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret",
            environment=Environment.Development
        )
        code = TestHelper.create_grant(oauth_app_gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "grant_payment_method"
        })
        access_token = oauth_app_gateway.oauth.create_token_from_code({
            "code": code
        }).credentials.access_token

        granting_gateway = BraintreeGateway(
            access_token=access_token,
        )

        return (granting_gateway, credit_card)

    @staticmethod
    def sample_notification_from_xml(xml):
        gateway = Configuration.gateway()
        payload = encodebytes(xml)
        hmac_payload = Crypto.sha1_hmac_hash(gateway.config.private_key, payload)
        signature = "%s|%s" % (gateway.config.public_key, hmac_payload)
        return {'bt_signature': signature, 'bt_payload': payload}

    @staticmethod
    def __send_graphql_request(graphql_request):
        client_token = json.loads(TestHelper.generate_decoded_client_token())
        headers = {
            "Content-Type": "application/json",
            "Braintree-Version": "2016-10-07",
            "Authorization": "Bearer " + client_token["braintree_api"]["access_token"]
        }
        resp = requests.post(client_token["braintree_api"]["url"] + "/graphql", headers=headers, data=json.dumps(graphql_request))
        return json.loads(resp.text)

class ClientApiHttp(Http):
    def __init__(self, config, options):
        self.config = config
        self.options = options
        self.http = Http(config)

    @staticmethod
    def create():
        config = Configuration.instantiate()
        client_token = TestHelper.generate_decoded_client_token()
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        return ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

    def get(self, path):
        return self._make_request("GET", path)

    def post(self, path, params=None):
        return self._make_request("POST", path, params)

    def put(self, path, params=None):
        return self._make_request("PUT", path, params)

    def _make_request(self, http_verb, path, params=None):
        http_strategy = self.config.http_strategy()
        request_body = json.dumps(params) if params else None
        return http_strategy.http_do(http_verb, path, self.__headers(), request_body)

    def set_authorization_fingerprint(self, authorization_fingerprint):
        self.options['authorization_fingerprint'] = authorization_fingerprint

    def get_configuration(self):
        encoded_fingerprint = quote_plus(self.options["authorization_fingerprint"])
        url = "/merchants/%s/client_api/v1/configuration" % self.config.merchant_id
        url += "?authorizationFingerprint=%s" % encoded_fingerprint
        url += "&configVersion=3"

        return self.get(url)

    def get_cards(self):
        encoded_fingerprint = quote_plus(self.options["authorization_fingerprint"])
        url = "/merchants/%s/client_api/v1/payment_methods.json" % self.config.merchant_id
        url += "?authorizationFingerprint=%s" % encoded_fingerprint
        url += "&sharedCustomerIdentifier=%s" % self.options["shared_customer_identifier"]
        url += "&sharedCustomerIdentifierType=%s" % self.options["shared_customer_identifier_type"]

        return self.get(url)

    def add_card(self, params):
        url = "/merchants/%s/client_api/v1/payment_methods/credit_cards.json" % self.config.merchant_id

        if 'authorization_fingerprint' in self.options:
            params['authorizationFingerprint'] = self.options['authorization_fingerprint']

        if 'shared_customer_identifier' in self.options:
            params['sharedCustomerIdentifier'] = self.options['shared_customer_identifier']

        if 'shared_customer_identifier_type' in self.options:
            params['sharedCustomerIdentifierType'] = self.options['shared_customer_identifier_type']

        return self.post(url, params)

    def get_paypal_nonce(self, paypal_params):
        url = "/merchants/%s/client_api/v1/payment_methods/paypal_accounts" % self.config.merchant_id
        params = {"paypal_account": paypal_params}
        if 'authorization_fingerprint' in self.options:
            params['authorizationFingerprint'] = self.options['authorization_fingerprint']

        status_code, response = self.post(url, params)

        nonce = None
        if status_code == 202:
            nonce = json.loads(response)["paypalAccounts"][0]["nonce"]

        return [status_code, nonce]

    def get_credit_card_nonce(self, credit_card_params):
        url = "/merchants/%s/client_api/v1/payment_methods/credit_cards" % self.config.merchant_id
        params = {"credit_card": credit_card_params}
        if 'authorization_fingerprint' in self.options:
            params['authorizationFingerprint'] = self.options['authorization_fingerprint']

        status_code, response = self.post(url, params)

        nonce = None
        if status_code in [201, 202]:
            nonce = json.loads(response)["creditCards"][0]["nonce"]

        return [status_code, nonce]

    def __headers(self):
        return {
            "Content-type": "application/json",
            "User-Agent": "Braintree Python " + version.Version, #pylint: disable=E0602
            "X-ApiVersion": Configuration.api_version()
        }

class ExpirationHelper(Enum):
    ADYEN = "03/2030"
