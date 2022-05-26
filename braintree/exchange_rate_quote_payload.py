from braintree.exchange_rate_quote import ExchangeRateQuote
from braintree.montary_amount import MontaryAmount

class ExchangeRateQuotePayload(object):
    def __init__(self, data):
        quote_objs = data.get("quotes")
        if(quote_objs is not None):
            self.quotes = list()
            for quote_obj in quote_objs:
                base_amount_obj = quote_obj.get("baseAmount")
                quote_amount_obj = quote_obj.get("quoteAmount")
                base_attrs = {"value":base_amount_obj.get("value"),
                              "currency_code":base_amount_obj.get("currencyCode")}
                base_amount = MontaryAmount(base_attrs)
                quote_attrs = {"value":quote_amount_obj.get("value"),
                               "currency_code":quote_amount_obj.get("currencyCode")}
                quote_amount = MontaryAmount(quote_attrs)
                attributes = {"id":quote_obj.get("id"),
                              "exchange_rate":quote_obj.get("exchangeRate"),
                              "trade_rate":quote_obj.get("tradeRate"),
                              "expires_at":quote_obj.get("expiresAt"),
                              "refreshes_at":quote_obj.get("refreshesAt"),
                              "base_amount":base_amount,
                              "quote_amount":quote_amount}
                quote = ExchangeRateQuote(attributes)
                self.quotes.append(quote)

    def get_quotes(self):
        return self.quotes