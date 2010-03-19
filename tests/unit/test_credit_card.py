import unittest
import tests.test_helper
from nose.tools import raises
from braintree.exceptions.down_for_maintenance_error import DownForMaintenanceError
from braintree.configuration import Configuration
from braintree.environment import Environment
from braintree.credit_card import CreditCard

class TestCreditCard(unittest.TestCase):
    def test_create_raises_exception_with_bad_keys(self):
        try:
            CreditCard.create({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_update_raises_exception_with_bad_keys(self):
        try:
            CreditCard.update("token", {"bad_key": "value"})
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_tr_data_for_create_raises_exceiption_with_bad_keys(self):
        try:
            CreditCard.tr_data_for_create({"bad_key": "value"}, "http://example.com")
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_tr_data_for_update_raises_exceiption_with_bad_keys(self):
        try:
            CreditCard.tr_data_for_update({"bad_key": "value"}, "http://example.com")
            self.assertTrue(False)
        except KeyError as e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_transparent_redirect_create_url(self):
        self.assertEquals(
            "http://localhost:3000/merchants/integration_merchant_id/payment_methods/all/create_via_transparent_redirect_request",
            CreditCard.transparent_redirect_create_url()
        )

    def test_transparent_redirect_update_url(self):
        self.assertEquals(
            "http://localhost:3000/merchants/integration_merchant_id/payment_methods/all/update_via_transparent_redirect_request",
            CreditCard.transparent_redirect_update_url()
        )

    @raises(DownForMaintenanceError)
    def test_confirm_transaprant_redirect_raises_error_given_503_status_in_query_string(self):
        CreditCard.confirm_transparent_redirect(
            "http_status=503&id=6kdj469tw7yck32j&hash=1b3d29199a282e63074a7823b76bccacdf732da6"
        )

    def test_create_signature_includes_customer_id(self):
        self.assertTrue("customer_id" in CreditCard.create_signature())

    def test_update_signature_does_not_include_customer_id(self):
        self.assertFalse("customer_id" in CreditCard.update_signature())
