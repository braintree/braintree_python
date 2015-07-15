import braintree
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from braintree.exceptions.not_found_error import NotFoundError
from braintree.oauth_credentials import OAuthCredentials
from urllib import quote_plus

class OAuthGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def create_token_from_code(self, params):
        params["grant_type"] = "authorization_code"
        return self._create_token(params)

    def create_token_from_refresh_token(self, params):
        params["grant_type"] = "refresh_token"
        return self._create_token(params)

    def _create_token(self, params):
        self.config.assert_has_client_credentials()
        response = self.config.http().post("/oauth/access_tokens", {
            "credentials": params
        })

        if "credentials" in response:
            return SuccessfulResult({"credentials": OAuthCredentials(self.gateway, response["credentials"])})
        else:
            return ErrorResult(self.gateway, response["api_error_response"])

    def connect_url(self, params):
        params["client_id"] = self.config.client_id
        user_params = self._sub_query(params, "user")
        business_params = self._sub_query(params, "business")

        def clean_values(accumulator, (key, value)):
            if isinstance(value, list):
                accumulator += map(lambda v: (key + "[]", v), value)
            else:
                accumulator += [(key, value)]
            return accumulator

        params = reduce(clean_values, params.items(), [])
        query = params + user_params + business_params
        query_string = "&".join(map(lambda (k, v): quote_plus(k) + "=" + quote_plus(v), query))
        return self._sign_url(self.config.environment.base_url + "/oauth/connect?" + query_string)

    def _sub_query(self, params, root):
        if root in params:
            sub_query = params.pop(root)
        else:
            sub_query = {}
        query = map(lambda (k,v): (root + "[" + k + "]",str(v)), sub_query.items())
        return query

    def _sign_url(self, url):
        return url
