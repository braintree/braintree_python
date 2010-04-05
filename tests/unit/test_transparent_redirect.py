from tests.test_helper import *

class TestTransparentRedirect(unittest.TestCase):
    def test_tr_data(self):
        data = TransparentRedirect.tr_data({"key": "val"}, "http://example.com/path?foo=bar")
        self.__assert_valid_tr_data(data)

    def __assert_valid_tr_data(self, data):
        hash, content = data.split("|", 1)
        self.assertEquals(hash, Crypto.hmac_hash(Configuration.private_key, content))

    @raises(ForgedQueryStringError)
    def test_parse_and_validate_query_string_raises_for_invalid_hash(self):
        TransparentRedirect.parse_and_validate_query_string(
            "http_status=200&id=7kdj469tw7yck32j&hash=99c9ff20cd7910a1c1e793ff9e3b2d15586dc6b9"
        )

    @raises(AuthenticationError)
    def test_parse_and_validate_query_string_raises_for_http_status_401(self):
        TransparentRedirect.parse_and_validate_query_string(
            "http_status=401&id=6kdj469tw7yck32j&hash=5a26e3cde5ebedb0ec1ba8d35724360334fbf419"
        )

    @raises(AuthorizationError)
    def test_parse_and_validate_query_string_raises_for_http_status_403(self):
        TransparentRedirect.parse_and_validate_query_string(
            "http_status=403&id=6kdj469tw7yck32j&hash=126d5130b71a4907e460fad23876ed70dd41dcd2"
        )

    @raises(NotFoundError)
    def test_parse_and_validate_query_string_raises_for_http_status_404(self):
        TransparentRedirect.parse_and_validate_query_string(
            "http_status=404&id=6kdj469tw7yck32j&hash=0d3724a45cf1cda5524aa68f1f28899d34d2ff3a"
        )

    @raises(ServerError)
    def test_parse_and_validate_query_string_raises_for_http_status_500(self):
        TransparentRedirect.parse_and_validate_query_string(
            "http_status=500&id=6kdj469tw7yck32j&hash=a839a44ca69d59a3d6f639c294794989676632dc"
        )

    @raises(DownForMaintenanceError)
    def test_parse_and_validate_query_string_raises_for_http_status_503(self):
        TransparentRedirect.parse_and_validate_query_string(
            "http_status=503&id=6kdj469tw7yck32j&hash=1b3d29199a282e63074a7823b76bccacdf732da6"
        )

    @raises(UnexpectedError)
    def test_parse_and_validate_query_string_raises_for_unexpected_http_status(self):
        TransparentRedirect.parse_and_validate_query_string(
            "http_status=600&id=6kdj469tw7yck32j&hash=740633356f93384167d887de0c1d9745e3de8fb6"
        )
