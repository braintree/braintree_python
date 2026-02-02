from tests.test_helper import *

# Visa Checkout is no longer supported for creating new transactions.
# Search functionality is retained for historical transactions only.
class TestVisaCheckout(unittest.TestCase):
    def test_search_by_payment_instrument_type(self):
        collection = Transaction.search([
            TransactionSearch.payment_instrument_type == PaymentInstrumentType.VisaCheckoutCard
        ])

        # Search should work for historical Visa Checkout transactions
        self.assertIsNotNone(collection)
