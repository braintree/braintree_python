import json
from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from braintree.test.nonces import Nonces
from braintree.dispute import Dispute
from braintree.payment_instrument_type import PaymentInstrumentType
from braintree.transaction import Transaction
from datetime import date

class TestTransactionPaymentFacilitator(unittest.TestCase):

    def test_transaction_with_sub_merchant_and_payment_facilitatator(self):

        request = {
            "type": "sale",
            "amount": "100.00",
            "merchant_account_id": "card_processor_brl_payfac",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "06/2026",
                "cvv": "123"
            },
            "descriptor": {
                "name": "companynme12*product12",
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
            "payment_facilitator": {
                "payment_facilitator_id": "98765432109",
                "sub_merchant": {
                    "reference_number": "123456789012345",
                    "tax_id": "99112233445577",
                    "legal_name": "Fooda",
                    "address": {
                        "street_address": "10880 Ibitinga",
                        "locality": "Araraquara",
                        "region": "SP",
                        "country_code_alpha2": "BR",
                        "postal_code": "13525000",
                        "international_phone": {
                            "country_code": "55",
                            "national_number": "9876543210",
                        },
                    },
                },
            },
            "options": {
                "store_in_vault_on_success": True,
            },
        }

        result = Transaction.create(request)
        transaction = result.transaction

        self.assertTrue(result.is_success)
        self.assertEqual(Transaction.Status.Authorized, transaction.status)
      
    def test_transaction_with_sub_merchant_and_payment_facilitatator_non_brazil_merchant(self):

        request = {
            "type": "sale",
            "amount": "100.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "06/2026",
                "cvv": "123"
            },
            "descriptor": {
                "name": "companynme12*product12",
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
            "payment_facilitator": {
                "payment_facilitator_id": "98765432109",
                "sub_merchant": {
                    "reference_number": "123456789012345",
                    "tax_id": "99112233445577",
                    "legal_name": "Fooda",
                    "address": {
                        "street_address": "10880 Ibitinga",
                        "locality": "Araraquara",
                        "region": "SP",
                        "country_code_alpha2": "BR",
                        "postal_code": "13525000",
                        "international_phone": {
                            "country_code": "55",
                            "national_number": "9876543210",
                        },
                    },
                },
            },
            "options": {
                "store_in_vault_on_success": True,
            },
        }

        config = Configuration(
            environment=Environment.Development,
            merchant_id="pp_credit_ezp_merchant",
            public_key="pp_credit_ezp_merchant_public_key",
            private_key="pp_credit_ezp_merchant_private_key"
        )
        ezp_gateway = BraintreeGateway(config)

        result = ezp_gateway.transaction.create(request)
        transaction = result.transaction

        self.assertFalse(result.is_success)
        self.assertEqual(
            '97405',
            result.errors.for_object("transaction").errors[0].code
        )
      
