from tests.test_helper import unittest 
from decimal import Decimal 
from braintree.graphql import MonetaryAmountInput, PayPalPayeeInput, PayPalPurchaseUnitInput

class TestPayPalPurchaseUnit(unittest.TestCase):
    def test_to_graphql_variables_all_fields(self):
        amount = MonetaryAmountInput(currency_code="USD", value=Decimal("10.00"))
        payee = (
            PayPalPayeeInput.builder()
            .email_address("test@example.com")
            .client_id("client456")
            .build()
        ) 

        purchase_unit = PayPalPurchaseUnitInput.builder(amount).payee(payee).build()
        graphql_variables = purchase_unit.to_graphql_variables()

        self.assertIn("amount", graphql_variables)
        self.assertIn("payee", graphql_variables)  