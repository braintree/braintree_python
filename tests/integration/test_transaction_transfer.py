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
                    "sender": {
                        "first_name": "Alice",
                        "middle_name": "A",
                        "last_name": "Silva",
                        "account_reference_number": "9876543210",
                        "account_reference_number_type": "PHONE_NUMBER",
                        "address": {
                            "street_address": "1st Main Road",
                            "locality": "Los Angeles",
                            "region": "CA",
                            "country_code_alpha2": "US",
                            },
                        "date_of_birth": date(2012,4,10)
                        },
                    "receiver": {
                        "account_reference_number": "1000012345",
                        "account_reference_number_type": "IBAN",
                        "first_name": "Bob",
                        "middle_name": "A",
                        "last_name": "Souza",
                        "address": {
                            "street_address": "2nd Main Road",
                            "locality": "Los Angeles",
                            "region": "CA",
                            "country_code_alpha2": "US",
                            }
                        }
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

        self.assertFalse(result.is_success)

    def test_transaction_with_invalid_sender_account_reference_number_type(self):
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
                    "sender": {
                        "account_reference_number": "1000012345",
                        "account_reference_number_type": "INVALID_ACCOUNT_REFERENCE_NUMBER_TYPE",
                        "first_name": "Bob",
                        "middle_name": "A",
                        "last_name": "Souza",
                        "address": {
                            "street_address": "2nd Main Road",
                            "locality": "Los Angeles",
                            "region": "CA",
                            "country_code_alpha2": "US",
                            }
                        }
                    },
                }
        result = Transaction.create(request)

        self.assertFalse(result.is_success)
        self.assertEqual(ErrorCodes.Transaction.TransferSenderAccountReferenceNumberTypeIsNotValid, result.errors.for_object("account_funding_transaction").on("sender_account_reference_number_type")[0].code)
    
    def test_transaction_with_invalid_receiver_account_reference_number_type(self):
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
                    "receiver": {
                        "account_reference_number": "1000012345",
                        "account_reference_number_type": "INVALID_ACCOUNT_REFERENCE_NUMBER_TYPE",
                        "first_name": "Bob",
                        "middle_name": "A",
                        "last_name": "Souza",
                        "address": {
                            "street_address": "2nd Main Road",
                            "locality": "Los Angeles",
                            "region": "CA",
                            "country_code_alpha2": "US",
                            }
                        }
                    },
                }
        result = Transaction.create(request)

        self.assertFalse(result.is_success)
        self.assertEqual(ErrorCodes.Transaction.TransferReceiverAccountReferenceNumberTypeIsNotValid, result.errors.for_object("account_funding_transaction").on("receiver_account_reference_number_type")[0].code)