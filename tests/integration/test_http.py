from tests.test_helper import *
import pycurl

class TestHttp(unittest.TestCase):

    def test_successful_connection_sandbox(self):
        try:
            config = Configuration(
                Environment.Sandbox,
                "merchant_id", "public_key", "private_key"
            )
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except AuthenticationError:
            pass

    def test_successful_connection_to_production(self):
        try:
            config = Configuration(
                Environment.Production,
                "merchant_id", "public_key", "private_key"
            )
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except AuthenticationError:
            pass

    def test_unsuccessful_connection_to_good_ssl_server_with_wrong_cert(self):
        environment = Environment(Environment.Sandbox.server, "443", True, Environment.Production.ssl_certificate)
        try:
            config = Configuration(environment, "merchant_id", "public_key", "private_key")
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except pycurl.error, e:
            error_code, error_msg = e
            self.assertEquals(pycurl.E_SSL_CACERT, error_code)
            self.assertTrue(re.search('verif(y|ication) failed', error_msg))

    def test_unsuccessful_connection_to_ssl_server_with_wrong_domain(self):
        try:
            environment = Environment("braintreegateway.com", "443", True, Environment.Production.ssl_certificate)
            config = Configuration(environment, "merchant_id", "public_key", "private_key")
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except pycurl.error, e:
            error_code, error_msg = e
            self.assertEquals(pycurl.E_SSL_PEER_CERTIFICATE, error_code)
            self.assertTrue(re.search("SSL: certificate subject name", error_msg))

    def test_unsafe_ssl_connection(self):
        try:
            Configuration.use_unsafe_ssl = True;
            environment = Environment(Environment.Sandbox.server, "443", True, Environment.Production.ssl_certificate)
            config = Configuration(environment, "merchant_id", "public_key", "private_key")
            http = config.http()
            http.get("/")
        except AuthenticationError:
            pass
        finally:
            Configuration.use_unsafe_ssl = False;

