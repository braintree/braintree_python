import json
from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from braintree.payment_instrument_type import PaymentInstrumentType
from braintree.transaction import Transaction
from datetime import date

class TestTransactionTransferType(unittest.TestCase):

    def test_transaction_with_valid_transfer_type_for_aft(self):
        request = {
                "type": "sale",
                "amount": "100.00",
                "merchant_account_id": "aft_first_data_wallet_transfer",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "06/2026",
                    "cvv": "123"
                    },
                "transfer": {
                    "type": "wallet_transfer",
                    },
                }

        result = Transaction.create(request)
        transaction = result.transaction

        self.assertTrue(result.is_success)
        self.assertTrue(transaction.account_funding_transaction)
        self.assertEqual(Transaction.Status.Authorized, transaction.status)

    def test_transaction_with_invalid_transfer_type(self):
        request = {
                "type": "sale",
                "amount": "100.00",
                "merchant_account_id": "aft_first_data_wallet_transfer",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "06/2026",
                    "cvv": "123"
                    },
                "transfer": {
                    "type": "invalid_transfer",
                    },
                }

        result = Transaction.create(request)
        transaction = result.transaction

        self.assertFalse(result.is_success)
