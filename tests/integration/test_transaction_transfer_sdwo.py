from tests.test_helper import *
from braintree.error_codes import ErrorCodes
from braintree.transaction import Transaction

class TestTransactionTransferSdwo(unittest.TestCase):

    TRANSFER_TYPES = ["account_to_account", "boleto_ticket", "person_to_person", "wallet_transfer"]

    def _get_base_request_data(self):
        return {
            "type": "sale",
            "amount": "100.00",
            "merchant_account_id": "card_processor_brl_sdwo",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "06/2026",
                "cvv": "123"
            },
            "descriptor": {
                "name": "companynme12*product1",
                "phone": "1232344444",
                "url": "example.com",
            },
            "billing": {
                "first_name": "Bob James",
                "country_code_alpha2": "CA",
                "extended_address": "",
                "locality": "Trois-Rivires",
                "region": "QC",
                "postal_code": "G8Y 156",
                "street_address": "2346 Boul Lane",
            },
            "transfer": {
                "type": "wallet_transfer",
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
                }
            },
            "options": {
                "store_in_vault_on_success": True,
            },
        }

    def test_transaction_with_transfer_for_sdwo_merchant(self):
        for transfer_type in self.TRANSFER_TYPES:
            request = self._get_base_request_data()
            request["transfer"]["type"] = transfer_type

            result = Transaction.create(request)
            transaction = result.transaction

            self.assertTrue(result.is_success)
            self.assertEqual(Transaction.Status.Authorized, transaction.status)

    def test_transaction_with_empty_transfer_type_for_sdwo_merchant(self):
        request = self._get_base_request_data()
        request["transfer"]["type"] = ""

        result = Transaction.create(request)
        transaction = result.transaction

        self.assertTrue(result.is_success)
        self.assertEqual(Transaction.Status.Authorized, transaction.status)

    def test_transaction_with_invalid_transfer_type(self):
        request = self._get_base_request_data()
        request["transfer"]["type"] = "invalid_transfer_type"

        result = Transaction.create(request)
        transaction = result.transaction

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.TransferTypeIsInvalid,
            result.errors.deep_errors[0].code
        )

    def test_transaction_missing_transfer_details_for_required_merchant(self):
        request = self._get_base_request_data()
        del request["transfer"]

        result = Transaction.create(request)
        transaction = result.transaction

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.TransferDetailsAreRequired,
            result.errors.for_object("transaction").errors[0].code
        )
