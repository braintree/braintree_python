from tests.test_helper import *
import base64
import urllib
import datetime
from braintree.util import Http

class ClientApiHttp(Http):
    def __init__(self, config, options):
        self.config = config
        self.options = options
        self.http = Http(config)

    def get(self, path):
        return self.__http_do("GET", path)

    def __http_do(self, http_verb, path, params=None):
        http_strategy = self.config.http_strategy()
        request_body = XmlUtil.xml_from_dict(params) if params else ''

        return http_strategy.http_do(http_verb, path, self.__headers(), request_body)

    def get_cards(self):
        encoded_fingerprint = urllib.quote_plus(self.options["authorization_fingerprint"])
        url = "/client_api/credit_cards.json?"
        url += "authorizationFingerprint=%s" % encoded_fingerprint
        url += "&sessionIdentifier=%s" % self.options["session_identifier"]
        url += "&sessionIdentifierType=%s" % self.options["session_identifier_type"]

        return self.get(url)

    def __headers(self):
        return {
            "Accept": "application/xml",
            "Content-type": "application/xml",
            "User-Agent": "Braintree Python " + version.Version,
            "X-ApiVersion": Configuration.api_version()
        }

class TestAuthorizationFingerprint(unittest.TestCase):

    def test_is_authorized_with_authorization_fingerprint(self):
        config = Configuration.instantiate()
        fingerprint = AuthorizationFingerprint.generate()

        http = ClientApiHttp(config, {
            "authorization_fingerprint": fingerprint,
            "session_identifier": "fake_identifier",
            "session_identifier_type": "testing"
        })

        status_code, response = http.get_cards()
        self.assertEqual(status_code, 200)
