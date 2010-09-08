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

    def test_successful_connection_sandbox_using_pycurl(self):
        try:
            Configuration.ssl_package = 'pycurl'
            config = Configuration(
                Environment.Sandbox,
                "merchant_id", "public_key", "private_key"
            )
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except AuthenticationError:
            pass
        finally:
            Configuration.ssl_package = 'm2crypto'

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

    def test_successful_connection_production_using_pycurl(self):
        try:
            Configuration.ssl_package = 'pycurl'
            config = Configuration(
                Environment.Production,
                "merchant_id", "public_key", "private_key"
            )
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except AuthenticationError:
            pass
        finally:
            Configuration.ssl_package = 'm2crypto'

    def test_invalid_ssl_package(self):
        try:
            Configuration.ssl_package = "bad"
            config = Configuration(
                Environment.Sandbox,
                "merchant_id", "public_key", "private_key"
            )
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except Exception, e:
            self.assertTrue(re.search("bad is not a valid value for Configuration.ssl_package", e.message))
        finally:
            Configuration.ssl_package = "m2crypto"

    def test_unsuccessful_connection_to_good_ssl_server_with_wrong_cert(self):
        environment = Environment(Environment.Sandbox.server, "443", True, Environment.Production.ssl_certificate)
        try:
            config = Configuration(environment, "merchant_id", "public_key", "private_key")
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except SSL.SSLError, e:
            self.assertTrue(re.search("certificate verify failed", e.message))

    def test_unsuccessful_connection_to_good_ssl_server_with_wrong_cert_using_pycurl(self):
        environment = Environment(Environment.Sandbox.server, "443", True, Environment.Production.ssl_certificate)
        try:
            Configuration.ssl_package = 'pycurl'
            config = Configuration(environment, "merchant_id", "public_key", "private_key")
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except pycurl.error, e:
            error_code, error_msg = e
            self.assertEquals(pycurl.E_SSL_CACERT, error_code)
            self.assertTrue(re.search("SSL certificate problem", error_msg))
        finally:
            Configuration.ssl_package = 'm2crypto'

    def test_unsuccessful_connection_to_ssl_server_with_wrong_domain(self):
        try:
            environment = Environment("braintreegateway.com", "443", True, Environment.Production.ssl_certificate)
            config = Configuration(environment, "merchant_id", "public_key", "private_key")
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except SSL.Checker.WrongHost, e:
            self.assertTrue(re.search("Peer certificate commonName does not match host", str(e)))

    def test_unsuccessful_connection_to_ssl_server_with_wrong_domain_using_pycurl(self):
        try:
            Configuration.ssl_package = 'pycurl'
            environment = Environment("braintreegateway.com", "443", True, Environment.Production.ssl_certificate)
            config = Configuration(environment, "merchant_id", "public_key", "private_key")
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except pycurl.error, e:
            print e
            error_code, error_msg = e
            self.assertEquals(pycurl.E_SSL_PEER_CERTIFICATE, error_code)
            self.assertTrue(re.search("SSL: certificate subject name", error_msg))
        finally:
            Configuration.ssl_package = 'm2crypto'

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

