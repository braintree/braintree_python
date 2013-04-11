from decimal import Decimal
from braintree.resource import Resource

class DepositDetail(Resource):
    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)

        if self.settlement_amount != None:
            self.settlement_amount = Decimal(self.settlement_amount)
        if self.settlement_currency_exchange_rate != None:
            self.settlement_currency_exchange_rate = Decimal(self.settlement_currency_exchange_rate)
