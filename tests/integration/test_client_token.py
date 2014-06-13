from tests.test_helper import *
import base64
import json
import urllib
import datetime
import braintree
from braintree.util import Http

class TestClientToken(unittest.TestCase):

    def test_is_authorized_with_authorization_fingerprint(self):
        config = Configuration.instantiate()
        client_token = ClientToken.generate()
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]

        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

        status_code, response = http.get_cards()
        self.assertEqual(status_code, 200)

    def test_allows_client_token_version_to_be_specified(self):
        config = Configuration.instantiate()
        client_token = ClientToken.generate({"version": 1})
        version = json.loads(client_token)["version"]

        self.assertEqual(version, 1)

    def test_can_pass_verify_card(self):
        config = Configuration.instantiate()
        result = braintree.Customer.create()
        customer_id = result.customer.id

        client_token = ClientToken.generate({
            "customer_id": customer_id,
            "options": {
                "verify_card": True
            }
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
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

        client_token = ClientToken.generate({
            "customer_id": customer_id,
            "options": {
                "make_default": True
            }
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(status_code, 201)

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4005519200000004",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(status_code, 201)

        customer = braintree.Customer.find(customer_id)
        self.assertEqual(len(customer.credit_cards), 2)
        for credit_card in customer.credit_cards:
            if credit_card.bin == "400551":
                self.assertTrue(credit_card.default)

    def test_can_pass_fail_on_duplicate_payment_method(self):
        config = Configuration.instantiate()
        result = braintree.Customer.create()
        customer_id = result.customer.id

        client_token = ClientToken.generate({
            "customer_id": customer_id,
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

        status_code, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(status_code, 201)

        client_token = ClientToken.generate({
            "customer_id": customer_id,
            "options": {
                "fail_on_duplicate_payment_method": True
            }
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http.set_authorization_fingerprint(authorization_fingerprint)
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

    def test_can_pass_merchant_account_id(self):
        client_token = ClientToken.generate({
            "merchant_account_id": "my_merchant_account"
        })
        merchant_account_id = json.loads(client_token)["merchantAccountId"]

        self.assertEqual(merchant_account_id, "my_merchant_account")

    def test_required_data_cannot_be_overridden(self):
        try:
            client_token = ClientToken.generate({
                "merchant_id": "1234"
            })
            self.fail("Should have raised exception!")
        except Exception as e:
            self.assertEqual("'Invalid keys: merchant_id'", str(e))
