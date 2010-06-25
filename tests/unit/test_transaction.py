from tests.test_helper import *

class TestTransaction(unittest.TestCase):
    def test_sale_raises_exception_with_bad_keys(self):
        try:
            Transaction.sale({"bad_key": "value"})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_sale_raises_exception_with_nested_bad_keys(self):
        try:
            Transaction.sale({"credit_card": {"bad_key": "value"}})
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: credit_card[bad_key]'", str(e))

    def test_tr_data_for_sale_raises_error_with_bad_keys(self):
        try:
            Transaction.tr_data_for_sale({"bad_key": "value"}, "http://example.com")
            self.assertTrue(False)
        except KeyError, e:
            self.assertEquals("'Invalid keys: bad_key'", str(e))

    def test_gateway_rejection_reason_available(self):
        transaction = Transaction({"amount": 1, "gateway_rejection_reason": "avs_and_cvv"})
        self.assertEquals(Transaction.GatewayRejectionReason.AvsAndCvv, transaction.gateway_rejection_reason)

