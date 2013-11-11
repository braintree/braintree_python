from tests.test_helper import *
import base64
import urllib
import datetime
import json
import braintree
from braintree.util import Http

class ClientApiHttp(Http):
    def __init__(self, config, options):
        self.config = config
        self.options = options
        self.http = Http(config)

    def get(self, path):
        return self.__http_do("GET", path)

    def post(self, path, params = None):
        return self.__http_do("POST", path, params)

    def __http_do(self, http_verb, path, params=None):
        http_strategy = self.config.http_strategy()
        request_body = json.dumps(params)
        return http_strategy.http_do(http_verb, path, self.__headers(), request_body)

    def set_fingerprint(self, new_fingerprint):
        self.options['authorization_fingerprint'] = new_fingerprint

    def get_cards(self):
        encoded_fingerprint = urllib.quote_plus(self.options["authorization_fingerprint"])
        url = "/client_api/credit_cards.json"
        url += "?authorizationFingerprint=%s" % encoded_fingerprint
        url += "&sessionIdentifier=%s" % self.options["session_identifier"]
        url += "&sessionIdentifierType=%s" % self.options["session_identifier_type"]

        return self.get(url)

    def add_card(self, params):
        url = "/client_api/credit_cards.json"

        if 'authorization_fingerprint' in self.options:
            params['authorizationFingerprint'] = self.options['authorization_fingerprint']

        if 'session_identifier' in self.options:
            params['sessionIdentifier'] = self.options['session_identifier']

        if 'session_identifier_type' in self.options:
            params['sessionIdentifierType'] = self.options['session_identifier_type']

        return self.post(url, params)

    def __headers(self):
        return {
            "Content-type": "application/json",
            "User-Agent": "Braintree Python " + version.Version,
            "X-ApiVersion": Configuration.api_version()
        }

class TestAuthorizationFingerprint(unittest.TestCase):

    def test_is_authorized_with_authorization_fingerprint(self):
        config = Configuration.instantiate()
        fingerprint = AuthorizationFingerprint.generate()

        http = ClientApiHttp(config, {
            "authorization_fingerprint": fingerprint,
            "session_identifier": "fake_identifier",
            "session_identifier_type": "testing"
        })

        status_code, response = http.get_cards()
        self.assertEqual(status_code, 200)

    def test_can_pass_verify_card(self):
        config = Configuration.instantiate()
        result = braintree.Customer.create()
        customer_id = result.customer.id

        fingerprint = AuthorizationFingerprint.generate({
            "customer_id": customer_id,
            "verify_card": True,
        })
        http = ClientApiHttp(config, {
            "authorization_fingerprint": fingerprint,
            "session_identifier": "fake_identifier",
            "session_identifier_type": "testing"
        })

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4000111111111115",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(status_code, 422)

    def test_can_pass_make_default(self):
        config = Configuration.instantiate()
        result = braintree.Customer.create()
        customer_id = result.customer.id

        fingerprint = AuthorizationFingerprint.generate({
            "customer_id": customer_id,
            "make_default": True,
        })
        http = ClientApiHttp(config, {
            "authorization_fingerprint": fingerprint,
            "session_identifier": "fake_identifier",
            "session_identifier_type": "testing"
        })

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(status_code, 200)

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4005519200000004",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(status_code, 200)

        customer = braintree.Customer.find(customer_id)
        self.assertEqual(len(customer.credit_cards), 2)
        for credit_card in customer.credit_cards:
            if credit_card.bin == "400551":
                self.assertTrue(credit_card.default)

    def test_can_pass_fail_on_duplicate_payment_method(self):
        config = Configuration.instantiate()
        result = braintree.Customer.create()
        customer_id = result.customer.id

        fingerprint = AuthorizationFingerprint.generate({
            "customer_id": customer_id,
        })
        http = ClientApiHttp(config, {
            "authorization_fingerprint": fingerprint,
            "session_identifier": "fake_identifier",
            "session_identifier_type": "testing"
        })

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(status_code, 200)

        fingerprint = AuthorizationFingerprint.generate({
            "customer_id": customer_id,
            "fail_on_duplicate_payment_method": True,
        })
        http.set_fingerprint(fingerprint)
        status_code, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(status_code, 422)

        customer = braintree.Customer.find(customer_id)
        self.assertEqual(len(customer.credit_cards), 1)
