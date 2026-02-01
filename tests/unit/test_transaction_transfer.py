from tests.test_helper import *
from datetime import date

transfer_type = ["account_to_account", "person_to_person", "wallet_transfer", "fund_transfer", "fund_disbursement", "payroll_disbursement", "prepaid_top_up"]
class TestTransactionTransferType(unittest.TestCase):
    def test_aft_transfer_type(self):
        for type in transfer_type:
            attributes = {
                    "amount": TransactionAmounts.Authorize,
                    "transfer": {
                        "type": type,
                        "sender": {
                            "first_name": "Alice",
                            "middle_name": "A",
                            "last_name": "Silva",
                            "account_reference_number": "1000012345",
                            "address": {
                                "street_address": "1st Main Road",
                                "locality": "Los Angeles",
                                "region": "CA",
                                "country_code_alpha2": "US",
                                },
                            "date_of_birth": date(2012,4,10)
                            },
                        "receiver": {
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

            transaction = Transaction(None, attributes)
            self.assertEqual(transaction.transfer.type, type)
            self.assertIsInstance(transaction.transfer, Transfer)
            self.assertIsInstance(transaction.transfer.sender, Sender)
            self.assertIsInstance(transaction.transfer.receiver, Receiver)

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
