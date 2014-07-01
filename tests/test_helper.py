import os
import random
import re
import unittest
import sys
if sys.version_info[0] == 2:
    from urllib import urlencode, quote_plus
    from httplib import HTTPConnection
else:
    from urllib.parse import urlencode, quote_plus
    from http.client import HTTPConnection
import warnings
import json
from braintree import *
from braintree.exceptions import *
from braintree.util import *
from braintree.testing_gateway import *
from datetime import date, datetime, timedelta
from decimal import Decimal
from nose.tools import raises
from random import randint
from contextlib import contextmanager
from base64 import b64decode

Configuration.configure(
    Environment.Development,
    "integration_merchant_id",
    "integration_public_key",
    "integration_private_key"
)

def showwarning(message, category, filename, lineno, file=None, line=None):
    pass
warnings.showwarning = showwarning

class TestHelper(object):

    default_merchant_account_id = "sandbox_credit_card"
    non_default_merchant_account_id = "sandbox_credit_card_non_default"
    non_default_sub_merchant_account_id = "sandbox_sub_merchant_account"
    three_d_secure_merchant_account_id = "three_d_secure_merchant_account"
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
    def simulate_tr_form_post(post_params, url=TransparentRedirect.url()):
        form_data = urlencode(post_params)
        conn = HTTPConnection(Configuration.environment.server_and_port)
        conn.request("POST", url, form_data, TestHelper.__headers())
        response = conn.getresponse()
        query_string = response.getheader("location").split("?", 1)[1]
        conn.close()
        return query_string

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
    def now_in_eastern():
        now  = datetime.utcnow()
        offset  = timedelta(hours=5)
        return (now - offset).strftime("%Y-%m-%d")

    @staticmethod
    def unique(list):
        return set(list)

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
        return b64decode(client_token)

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
        return self.__http_do("GET", path)

    def post(self, path, params = None):
        return self.__http_do("POST", path, params)

    def put(self, path, params = None):
        return self.__http_do("PUT", path, params)

    def __http_do(self, http_verb, path, params=None):
        http_strategy = self.config.http_strategy()
        request_body = json.dumps(params) if params else None
        return http_strategy.http_do(http_verb, path, self.__headers(), request_body)

    def set_authorization_fingerprint(self, authorization_fingerprint):
        self.options['authorization_fingerprint'] = authorization_fingerprint

    def get_cards(self):
        encoded_fingerprint = quote_plus(self.options["authorization_fingerprint"])
        url = "/merchants/%s/client_api/nonces.json" % self.config.merchant_id
        url += "?authorizationFingerprint=%s" % encoded_fingerprint
        url += "&sharedCustomerIdentifier=%s" % self.options["shared_customer_identifier"]
        url += "&sharedCustomerIdentifierType=%s" % self.options["shared_customer_identifier_type"]

        return self.get(url)

    def add_card(self, params):
        url = "/merchants/%s/client_api/nonces.json" % self.config.merchant_id

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
        if status_code == 202:
            nonce = json.loads(response)["creditCards"][0]["nonce"]

        return [status_code, nonce]

    def get_sepa_bank_account_nonce(self, sepa_bank_account_params):
        params = {"sepa_mandate": sepa_bank_account_params}
        url = "/merchants/%s/client_api/v1/sepa_mandates" % self.config.merchant_id
        if 'authorization_fingerprint' in self.options:
            params['authorizationFingerprint'] = self.options['authorization_fingerprint']

        status_code, response = self.post(url, params)
        mandate_reference_number = json.loads(response)["sepaMandates"][0]["mandateReferenceNumber"]

        accept_url = url + "/%s/accept" %  mandate_reference_number

        status_code, response = self.put(accept_url, params)

        nonce = None
        if status_code == 200:
            nonce = json.loads(response)["sepaBankAccounts"][0]["nonce"]

        return nonce

    def __headers(self):
        return {
            "Content-type": "application/json",
            "User-Agent": "Braintree Python " + version.Version,
            "X-ApiVersion": Configuration.api_version()
        }
