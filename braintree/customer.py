from braintree.util.callable import Callable
from braintree.util.http import Http

class Customer:
    @staticmethod
    def create(params):
        response = Http().post("/customers", params)
