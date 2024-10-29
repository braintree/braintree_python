from tests.test_helper import *
import json
import urllib
import datetime
import braintree
from braintree.util import Http
from base64 import b64decode

class TestClientTokenGenerate(unittest.TestCase):
    def test_allows_client_token_version_to_be_specified(self):
        client_token = ClientToken.generate({"version": 1})
        version = json.loads(client_token)["version"]
        self.assertEqual(1, version)

    def test_allows_client_token_domains_to_be_specified(self):
        client_token = ClientToken.generate({"domains": ["example.com"]})
        self.assertIsNotNone(client_token)

    def test_error_for_invalid_domain_format(self):
        self.assertRaises(ValueError, ClientToken.generate, {"domains": ["example"]
        })

    def test_error_for_too_many_domains(self):
        self.assertRaises(ValueError, ClientToken.generate,
            {"domains": [
                "example1.com",
                "example2.com",
                "example3.com",
                "example4.com",
                "example5.com",
                "example6.com",
            ]}
        )

    def test_error_in_generate_raises_value_error(self):
        self.assertRaises(ValueError, ClientToken.generate, {
            "customer_id": "i_am_not_a_real_customer"
        })

class TestClientToken(unittest.TestCase):
    def test_is_authorized_with_authorization_fingerprint(self):
        config = Configuration.instantiate()
        client_token = TestHelper.generate_decoded_client_token()
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]

        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

        status_code, _ = http.get_cards()
        self.assertEqual(200, status_code)

    def test_client_token_version_defaults_to_two(self):
        client_token = TestHelper.generate_decoded_client_token()
        version = json.loads(client_token)["version"]

        self.assertEqual(2, version)

    def test_can_pass_verify_card(self):
        config = Configuration.instantiate()
        result = braintree.Customer.create()
        customer_id = result.customer.id

        client_token = TestHelper.generate_decoded_client_token({
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

        status_code, _ = http.add_card({
            "credit_card": {
                "number": "4000111111111115",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(422, status_code)

    def test_can_pass_make_default(self):
        config = Configuration.instantiate()
        result = braintree.Customer.create()
        customer_id = result.customer.id

        client_token = TestHelper.generate_decoded_client_token({
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

        status_code, _ = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(201, status_code)

        status_code, _ = http.add_card({
            "credit_card": {
                "number": "4005519200000004",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(201, status_code)

        customer = braintree.Customer.find(customer_id)
        self.assertEqual(2, len(customer.credit_cards))
        for credit_card in customer.credit_cards:
            if credit_card.bin == "400551":
                self.assertTrue(credit_card.default)

    def test_can_pass_fail_on_duplicate_payment_method(self):
        config = Configuration.instantiate()
        result = braintree.Customer.create()
        customer_id = result.customer.id

        client_token = TestHelper.generate_decoded_client_token({
            "customer_id": customer_id,
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

        status_code, _ = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(201, status_code)

        client_token = TestHelper.generate_decoded_client_token({
            "customer_id": customer_id,
            "options": {
                "fail_on_duplicate_payment_method": True
            }
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http.set_authorization_fingerprint(authorization_fingerprint)
        status_code, _ = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(422, status_code)

        customer = braintree.Customer.find(customer_id)
        self.assertEqual(1, len(customer.credit_cards))

    def test_can_pass_fail_on_duplicate_payment_method_for_customer(self):
        config = Configuration.instantiate()
        result = braintree.Customer.create()
        customer_id = result.customer.id

        client_token = TestHelper.generate_decoded_client_token({
            "customer_id": customer_id,
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })

        status_code, _ = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(201, status_code)

        client_token = TestHelper.generate_decoded_client_token({
            "customer_id": customer_id,
            "options": {
                "fail_on_duplicate_payment_method_for_customer": True
            }
        })
        authorization_fingerprint = json.loads(client_token)["authorizationFingerprint"]
        http.set_authorization_fingerprint(authorization_fingerprint)
        status_code, _ = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            }
        })
        self.assertEqual(422, status_code)

        customer = braintree.Customer.find(customer_id)
        self.assertEqual(1, len(customer.credit_cards))

    def test_can_pass_merchant_account_id(self):
        expected_merchant_account_id = TestHelper.non_default_merchant_account_id
        client_token = TestHelper.generate_decoded_client_token({
            "merchant_account_id": expected_merchant_account_id
        })
        merchant_account_id = json.loads(client_token)["merchantAccountId"]

        self.assertEqual(expected_merchant_account_id, merchant_account_id)

    def test_required_data_cannot_be_overridden(self):
        with self.assertRaisesRegex(Exception, "'Invalid keys: merchant_id'"):
            TestHelper.generate_decoded_client_token({
                "merchant_id": "1234"
            })
