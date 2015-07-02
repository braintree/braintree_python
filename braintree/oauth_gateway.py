import braintree
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from braintree.exceptions.not_found_error import NotFoundError
from braintree.oauth_credentials import OAuthCredentials

class OAuthGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def create_token_from_code(self, params):
        params["grant_type"] = "authorization_code"
        return self._create_token(params)

    def _create_token(self, params):
        response = self.config.http().post("/oauth/access_tokens", {
                "credentials": params
        })
        if response["credentials"]:
            return SuccessfulResult({"credentials": OAuthCredentials(self.gateway, response["credentials"])})
