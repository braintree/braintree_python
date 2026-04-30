import unittest
from decimal import Decimal
import braintree
from braintree import (
    CreateLocalPaymentContextInput,
    LocalPaymentType
)
from braintree.exceptions.not_found_error import NotFoundError


@unittest.skip("LocalPaymentContext tests pending")
class LocalPaymentIT(unittest.TestCase):

    def pwpp_gateway(self):
        return braintree.BraintreeGateway(
            braintree.Configuration(
                environment=braintree.Environment.Development,
                merchant_id="pwpp_multi_account_merchant",
                public_key="pwpp_multi_account_merchant_public_key",
                private_key="pwpp_multi_account_merchant_private_key"
            )
        )

    def test_create_mbway_payment_context(self):
        input = CreateLocalPaymentContextInput(
            amount={
                "value": "10.00",
                "currency_code": "EUR"
            },
            type=LocalPaymentType.MBWAY,
            payer_info={
                "given_name": "John",
                "surname": "Doe",
                "phone_number": "912345678",
                "phone_country_code": "351"
            },
            return_url="https://example.com/return",
            cancel_url="https://example.com/cancel",
            merchant_account_id="eur_pwpp_multi_account_merchant_account"
        )

        result = self.pwpp_gateway().local_payment_context.create(input)

        self.assertTrue(result.is_success)
        self.assertIsNotNone(result.payment_context)
        self.assertIsNotNone(result.payment_context.id)
        self.assertIsNotNone(result.payment_context.legacy_id)
        self.assertEqual("MBWAY", result.payment_context.type)
        self.assertEqual(Decimal("10.00"), result.payment_context.amount.value)
        self.assertEqual("EUR", result.payment_context.amount.currency_code)

    def test_create_mbway_payment_context_with_billing_address(self):
        input = CreateLocalPaymentContextInput(
            amount={
                "value": "50.00",
                "currency_code": "EUR"
            },
            type=LocalPaymentType.MBWAY,
            payer_info={
                "given_name": "Maria",
                "surname": "Garcia",
                "email": "maria.garcia@example.com",
                "phone_number": "912345678",
                "phone_country_code": "351",
                "billing_address": {
                    "street_address": "123 Main St",
                    "locality": "Lisbon",
                    "region": "Lisboa",
                    "postal_code": "1000-001",
                    "country_code_alpha2": "PT"
                },
                "shipping_address": {
                    "street_address": "Av. da República, 123",
                    "locality": "Porto",
                    "postal_code": "4000-001",
                    "country_code_alpha2": "PT"
                }
            },
            order_id="order-123",
            return_url="https://example.com/return",
            cancel_url="https://example.com/cancel",
            merchant_account_id="eur_pwpp_multi_account_merchant_account"
        )

        result = self.pwpp_gateway().local_payment_context.create(input)

        self.assertTrue(result.is_success)
        self.assertIsNotNone(result.payment_context)
        self.assertIsNotNone(result.payment_context.legacy_id)
        self.assertEqual("MBWAY", result.payment_context.type)

    def test_create_crypto_payment_context(self):
        input = CreateLocalPaymentContextInput(
            amount={
                "value": "25.00",
                "currency_code": "USD"
            },
            type=LocalPaymentType.CRYPTO,
            payer_info={
                "given_name": "John",
                "surname": "Doe",
                "email": "john.doe@example.com"
            },
            return_url="https://example.com/return",
            cancel_url="https://example.com/cancel",
            merchant_account_id="usd_pwpp_multi_account_merchant_account"
        )

        result = self.pwpp_gateway().local_payment_context.create(input)

        self.assertTrue(result.is_success)
        self.assertIsNotNone(result.payment_context)
        self.assertIsNotNone(result.payment_context.legacy_id)
        self.assertEqual("CRYPTO", result.payment_context.type)

    def test_returns_error_for_invalid_input(self):
        input = CreateLocalPaymentContextInput(
            amount={
                "value": "invalid",
                "currency_code": "EUR"
            },
            type=LocalPaymentType.MBWAY,
            payer_info={
                "given_name": "John",
                "surname": "Doe",
                "phone_number": "912345678",
                "phone_country_code": "351"
            },
            return_url="https://example.com/return",
            cancel_url="https://example.com/cancel",
            merchant_account_id="eur_pwpp_multi_account_merchant_account"
        )

        result = self.pwpp_gateway().local_payment_context.create(input)

        self.assertFalse(result.is_success)
        self.assertGreater(len(result.errors.deep_errors), 0)

    def test_find_payment_context_by_id(self):
        input = CreateLocalPaymentContextInput(
            amount={
                "value": "10.00",
                "currency_code": "EUR"
            },
            type=LocalPaymentType.MBWAY,
            payer_info={
                "given_name": "John",
                "surname": "Doe",
                "phone_number": "912345678",
                "phone_country_code": "351"
            },
            return_url="https://example.com/return",
            cancel_url="https://example.com/cancel",
            merchant_account_id="eur_pwpp_multi_account_merchant_account"
        )

        create_result = self.pwpp_gateway().local_payment_context.create(input)
        self.assertTrue(create_result.is_success)

        payment_context_id = create_result.payment_context.id
        find_result = self.pwpp_gateway().local_payment_context.find(payment_context_id)

        self.assertTrue(find_result.is_success)
        self.assertIsNotNone(find_result.payment_context)
        self.assertEqual(payment_context_id, find_result.payment_context.id)
        self.assertEqual("MBWAY", find_result.payment_context.type)

    def test_raises_not_found_error_for_non_existent_id(self):
        with self.assertRaises(NotFoundError):
            self.pwpp_gateway().local_payment_context.find("non-existent-id-123")

    def test_create_with_only_required_fields(self):
        input = CreateLocalPaymentContextInput(
            amount={
                "value": "15.00",
                "currency_code": "EUR"
            },
            type=LocalPaymentType.MBWAY,
            payer_info={
                "given_name": "John",
                "surname": "Doe",
                "phone_number": "912345678",
                "phone_country_code": "351"
            },
            return_url="https://example.com/return",
            cancel_url="https://example.com/cancel",
            merchant_account_id="eur_pwpp_multi_account_merchant_account"
        )

        result = self.pwpp_gateway().local_payment_context.create(input)

        self.assertTrue(result.is_success)
        self.assertIsNotNone(result.payment_context)
        self.assertIsNotNone(result.payment_context.id)
        self.assertIsNotNone(result.payment_context.legacy_id)
        self.assertEqual("MBWAY", result.payment_context.type)
        self.assertEqual("eur_pwpp_multi_account_merchant_account", result.payment_context.merchant_account_id)
        self.assertIsNotNone(result.payment_context.amount)
        self.assertEqual(Decimal("15.00"), result.payment_context.amount.value)
        self.assertEqual("EUR", result.payment_context.amount.currency_code)
