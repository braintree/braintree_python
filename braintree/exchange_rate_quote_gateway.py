from braintree.exchange_rate_quote_payload import ExchangeRateQuotePayload
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult

class ExchangeRateQuoteGateway(object):
    def __init__(self, gateway, graphql_client = None):
        self.gateway = gateway
        self.config = gateway.config
        self.graphql_client = None if graphql_client is None else graphql_client
      
    def generate(self, request):
        definition = """
          mutation ($exchangeRateQuoteRequest: GenerateExchangeRateQuoteInput!) {
            generateExchangeRateQuote(input: $exchangeRateQuoteRequest) {
              quotes {
                id
                baseAmount {value, currencyCode}
                quoteAmount {value, currencyCode}
                exchangeRate
                tradeRate
                expiresAt
                refreshesAt
              }
            }
          }"""

        param = request.to_graphql_variables()
        graphql_client = self.graphql_client if self.graphql_client is not None else self.gateway.graphql_client
        response = graphql_client.query(definition, param)

        if "data" in response and "generateExchangeRateQuote" in response["data"]:
            result = response["data"]["generateExchangeRateQuote"]
            self.exchange_rate_quote_payload = ExchangeRateQuotePayload(result)
            return SuccessfulResult({"exchange_rate_quote_payload": self.exchange_rate_quote_payload})
        elif "errors" in response:
            error_codes = response["errors"][0]
            error_codes["errors"] = dict()
            return ErrorResult(self.gateway, error_codes)