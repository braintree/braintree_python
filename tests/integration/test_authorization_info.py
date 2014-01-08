from tests.test_helper import *
import base64
import json
import urllib
import datetime
import braintree
from braintree.util import Http

class TestAuthorizationInfo(unittest.TestCase):

    def test_is_authorized_with_authorization_fingerprint(self):
        config = Configuration.instantiate()
        fingerprint = json.loads(AuthorizationInfo.generate())["fingerprint"]

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

        auth_info = AuthorizationInfo.generate({
            "customer_id": customer_id,
            "verify_card": True,
        })
        fingerprint = json.loads(auth_info)["fingerprint"]
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

        auth_info = AuthorizationInfo.generate({
            "customer_id": customer_id,
            "make_default": True,
        })
        fingerprint = json.loads(auth_info)["fingerprint"]
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

        auth_info = AuthorizationInfo.generate({
            "customer_id": customer_id,
        })
        fingerprint = json.loads(auth_info)["fingerprint"]
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
        self.assertEqual(status_code, 201)

        auth_info = AuthorizationInfo.generate({
            "customer_id": customer_id,
            "fail_on_duplicate_payment_method": True,
        })
        fingerprint = json.loads(auth_info)["fingerprint"]
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
