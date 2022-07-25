from braintree.exchange_rate_quote_request import ExchangeRateQuoteInput
from tests.test_helper import *

class TestExchangeRateQuoteInput(unittest.TestCase):
    def test_to_graphql_variables(self):
        attributes = {"base_currency":"USD",
                      "quote_currency":"EUR",
                      "base_amount":"10.15",
                      "markup":"5.00"}
        input = ExchangeRateQuoteInput(None,attributes)

        map = input.to_graphql_variables()
        self.assertEqual(map.get("baseCurrency"), "USD")
        self.assertEqual(map.get("quoteCurrency"), "EUR")
        self.assertEqual(map.get("baseAmount"), "10.15")
        self.assertEqual(map.get("markup"), "5.00")

    def test_to_graphql_variables_without_markup_and_base_amount(self):
        attributes = {"base_currency":"USD",
                      "quote_currency":"CAD"}
        input = ExchangeRateQuoteInput(None,attributes)

        map = input.to_graphql_variables()
        self.assertEqual(map.get("baseCurrency"), "USD")
        self.assertEqual(map.get("quoteCurrency"), "CAD")
        self.assertIsNone(map.get("baseAmount"))
        self.assertIsNone(map.get("markup"))

    def test_to_graphql_variables_with_all_empty_fields(self):
        input = ExchangeRateQuoteInput(None, None)

        map = input.to_graphql_variables()
        self.assertIsNone(map.get("baseCurrency"))
        self.assertIsNone(map.get("quoteCurrency"))
        self.assertIsNone(map.get("baseAmount"))
        self.assertIsNone(map.get("markup"))