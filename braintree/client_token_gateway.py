import braintree
from braintree.client_token import ClientToken
from braintree.resource import Resource
from braintree import exceptions

class ClientTokenGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config


    def generate(self, params):
        if params:
            Resource.verify_keys(params, ClientToken.generate_signature())
            params = {'client_token': params}

        response = self.config.http().post("/client_token", params)

        if "client_token" in response:
            return response["client_token"]["value"]
        else:
            raise ValueError(response["api_error_response"]["message"])
