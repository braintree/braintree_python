from tests.test_helper import *

from braintree.test.nonces import Nonces
from braintree.exceptions.not_found_error import NotFoundError
from braintree.error_codes import ErrorCodes

class TestCoinbase(unittest.TestCase):

    def test_customer(self):
        result = Customer.create({"payment_method_nonce": Nonces.Coinbase})

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.PaymentMethod.PaymentMethodNoLongerSupported, result.errors.for_object("coinbase_account").on("base")[0].code)

    def test_vault(self):
        result = Customer.create()
        result = PaymentMethod.create({
            "customer_id": result.customer.id,
            "payment_method_nonce": Nonces.Coinbase
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.PaymentMethod.PaymentMethodNoLongerSupported, result.errors.for_object("coinbase_account").on("base")[0].code)

    def test_transaction(self):
        result = Transaction.sale({"payment_method_nonce": Nonces.Coinbase, "amount": "1.00"})

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.PaymentMethod.PaymentMethodNoLongerSupported, result.errors.for_object("transaction").on("base")[0].code)
