from braintree.util.http import Http
from braintree.successful_result import SuccessfulResult

class Customer:
    @staticmethod
    def create(params={}):
        response = Http().post("/customers", {"customer": params})
        if "customer" in response:
            return SuccessfulResult({"customer": Customer(response["customer"])})
        else:
            pass

    def __init__(self, attributes):
        self.attributes = attributes

    def __getattr__(self, key):
        if key in self.attributes:
            return self.attributes[key]
        else:
            return None
