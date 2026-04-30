from tests.test_helper import unittest
from braintree.graphql.inputs.create_local_payment_context_input import CreateLocalPaymentContextInput
from braintree import LocalPaymentType


class TestCreateLocalPaymentContextInput(unittest.TestCase):
    def test_create_local_payment_context_input_with_attributes(self):
        input_data = {
            "amount": {"value": "10.00", "currency_code": "EUR"},
            "type": LocalPaymentType.MBWAY,
            "payer_info": {
                "given_name": "John",
                "surname": "Doe"
            },
            "order_id": "order-123"
        }

        input = CreateLocalPaymentContextInput(**input_data)

        self.assertEqual(LocalPaymentType.MBWAY, input._type)
        self.assertEqual("order-123", input._order_id)
        self.assertIsNotNone(input._amount)
        self.assertIsNotNone(input._payer_info)

    def test_to_graphql_variables_with_camel_case_keys(self):
        input_data = {
            "amount": {"value": "10.00", "currency_code": "EUR"},
            "type": LocalPaymentType.MBWAY,
            "payer_info": {
                "given_name": "John",
                "surname": "Doe"
            },
            "order_id": "order-123"
        }

        input = CreateLocalPaymentContextInput(**input_data)
        variables = input.to_graphql_variables()

        self.assertIn("paymentContext", variables)
        payment_context = variables["paymentContext"]

        self.assertEqual({"value": "10.00", "currencyCode": "EUR"}, payment_context["amount"])
        self.assertEqual(LocalPaymentType.MBWAY, payment_context["type"])
        self.assertEqual({"givenName": "John", "surname": "Doe"}, payment_context["payerInfo"])
        self.assertEqual("order-123", payment_context["orderId"])

    def test_to_graphql_variables_omits_nil_values(self):
        input_data = {
            "amount": {"value": "10.00", "currency_code": "EUR"},
            "type": LocalPaymentType.MBWAY
        }

        input = CreateLocalPaymentContextInput(**input_data)
        variables = input.to_graphql_variables()

        payment_context = variables["paymentContext"]
        self.assertEqual({"value": "10.00", "currencyCode": "EUR"}, payment_context["amount"])
        self.assertEqual(LocalPaymentType.MBWAY, payment_context["type"])
        self.assertNotIn("payerInfo", payment_context)
        self.assertNotIn("orderId", payment_context)
