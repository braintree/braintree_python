from braintree.exchange_rate_quote_input import ExchangeRateQuoteInput

class ExchangeRateQuoteRequest(object):
    def __init__(self):
        self.quotes = list()

    def add_exchange_rate_quote_input(self,attributes):
        new_input = ExchangeRateQuoteInput(self,attributes)
        self.quotes.append(new_input)
        return new_input

    def to_graphql_variables(self):
        variables = dict()
        input = dict()
        
        quote_list = list()
        for quote in self.quotes:
            quote_list.append(quote.to_graphql_variables())
        input["quotes"] = quote_list
        variables["exchangeRateQuoteRequest"] = input
        return variables