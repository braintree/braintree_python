from braintree.util.http import Http

class Customer:
    @staticmethod
    def create(params):
        response = Http().post("/customers", {"customer": params})
