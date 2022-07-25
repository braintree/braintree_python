from braintree.exchange_rate_quote_gateway import ExchangeRateQuoteGateway
from braintree.exchange_rate_quote_request import ExchangeRateQuoteRequest
from tests.test_helper import *
from unittest.mock import Mock

class TestExchangeRateQuoteGateway(unittest.TestCase):
    @staticmethod
    def get_gateway():
        config = Configuration("development", "integration_merchant_id",
                               public_key="integration_public_key",
                               private_key="integration_private_key")
        return BraintreeGateway(config)

    def test_generate_success(self):
        attribute1 = {"base_currency":"USD",
                      "quote_currency":"EUR",
                      "base_amount":"12.19",
                      "markup":"1.89"}

        request = ExchangeRateQuoteRequest().add_exchange_rate_quote_input(attribute1).done()

        raw_response = """
                    {
                      "data": {
                      "generateExchangeRateQuote": {
                        "quotes": [
                        {
                          "id": "ZXhjaGFuZ2VyYXRlcXVvdGVfMDEyM0FCQw",
                          "baseAmount": {
                              "value": "12.19",
                              "currencyCode": "USD"
                          },
                          "quoteAmount": {
                            "value": "12.16",
                            "currencyCode": "EUR"
                          },
                          "exchangeRate": "0.997316360864",
                            "expiresAt": "2021-06-16T02:00:00.000000Z",
                            "refreshesAt": "2021-06-16T00:00:00.000000Z"
                        }
                        ]
                      }
                    },
                      "extensions": {
                      "requestId": "5ef2e69a-fb0e-4d71-82a3-ea59722ac64d"
                      }
                    }
                """
        response = json.loads(raw_response)
        self.graphql_client = self.get_gateway().graphql_client
        self.graphql_client.query = Mock(return_value=response)
        exchange_rate_quote_gateway = ExchangeRateQuoteGateway(self.get_gateway(),self.graphql_client)
        result = exchange_rate_quote_gateway.generate(request)
        quotes = result.exchange_rate_quote_payload.get_quotes()
        self.assertIsNotNone(quotes)
        self.assertEqual(1,len(quotes))

        quote1 = quotes[0]
        self.assertEqual("12.19", str(quote1.base_amount.value))
        self.assertEqual("USD", quote1.base_amount.currency_code)
        self.assertEqual("12.16", str(quote1.quote_amount.value))
        self.assertEqual("EUR", quote1.quote_amount.currency_code)
        self.assertEqual("0.997316360864", quote1.exchange_rate)
        self.assertEqual("2021-06-16T02:00:00.000000Z", quote1.expires_at)
        self.assertEqual("2021-06-16T00:00:00.000000Z", quote1.refreshes_at)
        self.assertEqual("ZXhjaGFuZ2VyYXRlcXVvdGVfMDEyM0FCQw", quote1.id)

    def test_generate_error(self):
        attribute1 = {"base_currency":"USD"}
        request = ExchangeRateQuoteRequest().add_exchange_rate_quote_input(attribute1).done()

        raw_response = """
                {
                  "errors": [
                    {
                      "message": "Field 'quoteCurrency' of variable 'exchangeRateQuoteRequest' has coerced Null value for NonNull type 'CurrencyCodeAlpha!'",
                      "locations": [
                        {
                          "line": 1,
                          "column": 11
                        }
                      ]
                    }
                  ],
                  "extensions": {
                    "requestId": "96c023c9-0192-4008-8f28-25a7f8714bab"
                  }
                }
                """
        response = json.loads(raw_response)
        self.graphql_client = self.get_gateway().graphql_client
        self.graphql_client.query = Mock(return_value=response)
        exchange_rate_quote_gateway = ExchangeRateQuoteGateway(self.get_gateway(),self.graphql_client)
        result = exchange_rate_quote_gateway.generate(request)
        self.assertTrue("'quoteCurrency'" in result.message)