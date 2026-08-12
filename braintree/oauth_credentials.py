from braintree.resource import Resource

class OAuthCredentials(Resource):
    def __repr__(self):
        detail_list = ["token_type", "expires_at", "scope"]
        return super(OAuthCredentials, self).__repr__(detail_list)
