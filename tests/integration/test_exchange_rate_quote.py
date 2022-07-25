from tests.test_helper import *
from braintree.exchange_rate_quote_request import ExchangeRateQuoteRequest

class TestExchangeRateQuote(unittest.TestCase):
    @staticmethod
    def get_gateway():
        config = Configuration("development", "integration_merchant_id",
                               public_key="integration_public_key",
                               private_key="integration_private_key")
        return BraintreeGateway(config)

    def test_exchange_rate_quote_with_full_graphql(self):
        attribute1 = {"base_currency":"USD",
                      "quote_currency":"EUR",
                      "base_amount":"12.19",
                      "markup":"12.14"}

        attribute2 = {"base_currency":"EUR",
                      "quote_currency":"CAD",
                      "base_amount":"15.16",
                      "markup":"2.64"}

        request = ExchangeRateQuoteRequest().add_exchange_rate_quote_input(
            attribute1).done().add_exchange_rate_quote_input(attribute2).done()

        result = self.get_gateway().exchange_rate_quote.generate(request)
        self.assertTrue(result.is_success)
        quotes = result.exchange_rate_quote_payload.get_quotes()
        self.assertEqual(2, len(quotes))

        quote1 = quotes[0]
        self.assertEqual("12.19", str(quote1.base_amount.value))
        self.assertEqual("USD", quote1.base_amount.currency_code)
        self.assertEqual("12.16", str(quote1.quote_amount.value))
        self.assertEqual("EUR", quote1.quote_amount.currency_code)
        self.assertEqual("0.997316360864", quote1.exchange_rate)
        self.assertEqual("0.01", quote1.trade_rate)
        self.assertEqual("2021-06-16T02:00:00.000000Z", quote1.expires_at)
        self.assertEqual("2021-06-16T00:00:00.000000Z", quote1.refreshes_at)
        self.assertEqual("ZXhjaGFuZ2VyYXRlcXVvdGVfMDEyM0FCQw", quote1.id)

        quote2 = quotes[1]
        self.assertEqual("15.16", str(quote2.base_amount.value))
        self.assertEqual("EUR", quote2.base_amount.currency_code)
        self.assertEqual("23.30", str(quote2.quote_amount.value))
        self.assertEqual("CAD", quote2.quote_amount.currency_code)
        self.assertEqual("1.536744692129366", quote2.exchange_rate)
        self.assertIsNone(quote2.trade_rate)
        self.assertEqual("2021-06-16T02:00:00.000000Z", quote2.expires_at)
        self.assertEqual("2021-06-16T00:00:00.000000Z", quote2.refreshes_at)
        self.assertEqual("ZXhjaGFuZ2VyYXRlcXVvdGVfQUJDMDEyMw", quote2.id)

    def test_exchange_rate_quote_with_graphqul_quote_currency_validation_error(self):
        attribute1 = {"base_currency":"USD",
                      "base_amount":"12.19",
                      "markup":"12.14"}

        attribute2 = {"base_currency":"EUR",
                      "quote_currency":"CAD",
                      "base_amount":"15.16",
                      "markup":"2.64"}
        request = ExchangeRateQuoteRequest().add_exchange_rate_quote_input(
            attribute1).done().add_exchange_rate_quote_input(attribute2).done()

        result = self.get_gateway().exchange_rate_quote.generate(request)
        self.assertFalse(result.is_success)
        self.assertTrue("'quoteCurrency'" in result.message)

    def test_exchange_rate_quote_with_graphql_base_currency_validation_error(self):
        attribute1 = {"base_currency":"USD",
                      "quote_currency":"EUR",
                      "base_amount":"12.19",
                      "markup":"12.14"}

        attribute2 = {"quote_currency":"CAD",
                      "base_amount":"15.16",
                      "markup":"2.64"}

        request = ExchangeRateQuoteRequest().add_exchange_rate_quote_input(
            attribute1).done().add_exchange_rate_quote_input(attribute2).done()

        result = self.get_gateway().exchange_rate_quote.generate(request)
        self.assertFalse(result.is_success)
        self.assertTrue("'baseCurrency'" in result.message)

    def test_exchange_rate_quote_with_graphql_without_base_amount(self):
        attribute1 = {"base_currency":"USD",
                      "quote_currency":"EUR"}

        attribute2 = {"base_currency":"EUR",
                      "quote_currency":"CAD"}

        request = ExchangeRateQuoteRequest().add_exchange_rate_quote_input(
            attribute1).done().add_exchange_rate_quote_input(attribute2).done()
                
        result = self.get_gateway().exchange_rate_quote.generate(request)
        self.assertTrue(result.is_success)

    def test_exchange_rate_quote_with_graphql_without_base_and_quote_currency(self):
        attribute1 = {"base_amount":"12.19",
                      "markup":"12.14"}

        request = ExchangeRateQuoteRequest().add_exchange_rate_quote_input(
            attribute1).done()

        result = self.get_gateway().exchange_rate_quote.generate(request)
        self.assertFalse(result.is_success)
        self.assertTrue("'baseCurrency'" in result.message)