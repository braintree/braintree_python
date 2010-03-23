from tests.test_helper import *

class TestHttp(unittest.TestCase):

    def test_successful_connection_to_good_ssl_server(self):
        environment = Environment("qa-master.braintreegateway.com", "443", True, "braintree/ssl/valicert_ca.crt")
        http = Http(environment)
        http.get("/customers")

    def test_unsuccessful_connection_to_good_ssl_server_with_wrong_cert(self):
        environment = Environment("qa-master.braintreegateway.com", "443", True, "braintree/ssl/securetrust_ca.crt")
        try:
            http = Http(environment)
            http.get("/customers")
            self.assertTrue(False)
        except SSL.SSLError, e:
            self.assertTrue(re.search("certificate verify failed", e.message))

    def test_unsuccessful_connection_to_ssl_server_with_wrong_domain(self):
        try:
            environment = Environment("braintreegateway.com", "443", True, "braintree/ssl/securetrust_ca.crt")
            http = Http(environment)
            http.get("/customers")
            self.assertTrue(False)
        except SSL.Checker.WrongHost, e:
            self.assertTrue(re.search("Peer certificate commonName does not match host", str(e)))
