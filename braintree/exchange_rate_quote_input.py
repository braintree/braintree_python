from braintree.attribute_getter import AttributeGetter

class ExchangeRateQuoteInput(AttributeGetter):
    def __init__(self,parent,attributes):
        self.parent = parent
        AttributeGetter.__init__(self,attributes)

    def done(self):
        return self.parent

    def to_graphql_variables(self):
        variables = dict()
        variables["baseCurrency"] = self.base_currency if getattr(self,"base_currency",None) is not None else None
        variables["quoteCurrency"] = self.quote_currency if getattr(self,"quote_currency",None) is not None else None
        variables["baseAmount"] = self.base_amount if getattr(self,"base_amount",None) is not None else None
        variables["markup"] = self.markup if getattr(self,"markup",None) is not None else None
        return variables