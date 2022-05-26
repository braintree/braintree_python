from braintree.exchange_rate_quote_request import ExchangeRateQuoteRequest
from tests.test_helper import *

class TestExchangeRateQuoteRequest(unittest.TestCase):
    def test_to_graphql_variables(self):
        attribute1 = {"base_currency":"USD",
                      "quote_currency":"EUR",
                      "base_amount":"5.00",
                      "markup":"3.00"}

        attribute2 = {"base_currency":"EUR",
                      "quote_currency":"CAD",
                      "base_amount":"15.00",
                      "markup":"2.64"}

        request = ExchangeRateQuoteRequest().add_exchange_rate_quote_input(
            attribute1).done().add_exchange_rate_quote_input(attribute2).done()

        request_map = request.to_graphql_variables().get("exchangeRateQuoteRequest")
        self.assertIsNotNone(request_map)
        
        quotes = request_map.get("quotes")
        self.assertIsNotNone(quotes)
        self.assertEqual(2,len(quotes))

        quote1 = quotes[0]
        self.assertEqual("USD", quote1.get("baseCurrency"))
        self.assertEqual("EUR", quote1.get("quoteCurrency"))
        self.assertEqual("5.00", quote1.get("baseAmount"))
        self.assertEqual("3.00", quote1.get("markup"))

        quote2 = quotes[1]
        self.assertEqual("EUR", quote2.get("baseCurrency"))
        self.assertEqual("CAD", quote2.get("quoteCurrency"))
        self.assertEqual("15.00", quote2.get("baseAmount"))
        self.assertEqual("2.64", quote2.get("markup"))

    def test_to_graphql_variables_with_missing_fields(self):
        attribute1 = {"base_currency":"USD",
                      "quote_currency":"EUR",
                      "base_amount":"5.00"}

        attribute2 = {"base_currency":"EUR",
                      "quote_currency":"CAD"}

        request = ExchangeRateQuoteRequest().add_exchange_rate_quote_input(attribute1
                ).done().add_exchange_rate_quote_input(attribute2).done()

        request_map = request.to_graphql_variables().get("exchangeRateQuoteRequest")
        self.assertIsNotNone(request_map)
        
        quotes = request_map.get("quotes")
        self.assertIsNotNone(quotes)
        self.assertEqual(2,len(quotes))

        quote1 = quotes[0]
        self.assertEqual("USD", quote1.get("baseCurrency"))
        self.assertEqual("EUR", quote1.get("quoteCurrency"))
        self.assertEqual("5.00", quote1.get("baseAmount"))
        self.assertIsNone(quote1.get("markup"))

        quote2 = quotes[1]
        self.assertEqual("EUR", quote2.get("baseCurrency"))
        self.assertEqual("CAD", quote2.get("quoteCurrency"))
        self.assertIsNone(quote2.get("baseAmount"))
        self.assertIsNone(quote2.get("markup"))