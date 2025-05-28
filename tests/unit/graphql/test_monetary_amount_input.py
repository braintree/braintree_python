from tests.test_helper import unittest
from decimal import Decimal 
from braintree.graphql import MonetaryAmountInput

class TestMonetaryAmountInput(unittest.TestCase):
    def test_monetary_amount_input_to_graphql_variables(self):
        input = MonetaryAmountInput(currency_code="EUR", value=Decimal("15.50"))

        graphql_variables = input.to_graphql_variables()

        self.assertEqual("EUR", graphql_variables["currencyCode"])
        self.assertEqual("15.50", graphql_variables["value"])

    
