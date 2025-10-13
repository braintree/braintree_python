from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from braintree.payment_facilitator import PaymentFacilitator
from braintree.sub_merchant import SubMerchant
from braintree.meta_checkout_card import MetaCheckoutCard
from braintree.meta_checkout_token import MetaCheckoutToken
from datetime import datetime
from datetime import date
from braintree.authorization_adjustment import AuthorizationAdjustment
from unittest.mock import MagicMock


class TestTransactionTransferType(unittest.TestCase):
    def test_aft_transfer_type(self):
        attributes = {
                "amount": TransactionAmounts.Authorize,
                "transfer": {
                    "type": "wallet_transfer",
                    },
                }

        transaction = Transaction(None, attributes)
        self.assertEqual(transaction.transfer.type, 'wallet_transfer')

    def test_transfer_staged_digital_wallet_operator(self):
        transfer_types = ["account_to_account", "boleto_ticket", "person_to_person", "wallet_transfer"]
        
        for transfer_type in transfer_types:
            attributes = {
                "amount": "100.00",
                "transfer": {
                    "sender": {
                        "first_name": "Alice",
                        "last_name": "Silva",
                        "account_reference_number": "1000012345",
                        "tax_id": "12345678900",
                        "address": {
                            "street_address": "Rua das Flores, 100",
                            "extended_address": "2B",
                            "locality": "São Paulo",
                            "region": "SP",
                            "postal_code": "01001-000",
                            "country_code_alpha2": "BR",
                            "international_phone": {
                                "country_code": "55",
                                "national_number": "1234567890"
                            }
                        }
                    },
                    "receiver": {
                        "first_name": "Bob",
                        "last_name": "Souza",
                        "account_reference_number": "2000012345",
                        "tax_id": "98765432100",
                        "address": {
                            "street_address": "Avenida Brasil, 200",
                            "extended_address": "2B",
                            "locality": "Rio de Janeiro",
                            "region": "RJ",
                            "postal_code": "20040-002",
                            "country_code_alpha2": "BR",
                            "international_phone": {
                                "country_code": "55",
                                "national_number": "9876543210"
                            }
                        }
                    },
                    "type": transfer_type
                }
            }

            transaction = Transaction(None, attributes)
            
            self.assertIsInstance(transaction.transfer, Transfer)
            self.assertIsInstance(transaction.transfer.sender, Sender)
            self.assertIsInstance(transaction.transfer.receiver, Receiver)
            self.assertEqual(transaction.transfer.type, transfer_type)
