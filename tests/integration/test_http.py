from tests.test_helper import *
from distutils.version import LooseVersion
import platform
import braintree
import requests
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
        if platform.system() == "Darwin":
            return
        environment = Environment(Environment.Sandbox.server, "443", True, Environment.Production.ssl_certificate)
        try:
            config = Configuration(environment, "merchant_id", "public_key", "private_key")
            config._http_strategy = braintree.util.http_strategy.pycurl_strategy.PycurlStrategy(config, config.environment)
            http = config.http()
            http.get("/")
            self.assertTrue(False)
        except pycurl.error, e:
            error_code, error_msg = e
            self.assertEquals(pycurl.E_SSL_CACERT, error_code)
            self.assertTrue(re.search('verif(y|ication) failed', error_msg))
        except AuthenticationError:
            self.fail("Expected to Receive an SSL error from pycurl, but received an Authentication Error instead, check your local openssl installation")

    def test_unsuccessful_connection_to_good_ssl_server_with_wrong_cert_on_requests(self):
        if platform.system() == "Darwin":
            return

        environment = Environment(Environment.Sandbox.server, "443", True, Environment.Production.ssl_certificate)
        config = Configuration(environment, "merchant_id", "public_key", "private_key")
        config._http_strategy = braintree.util.http_strategy.requests_strategy.RequestsStrategy(config, config.environment)
        http = config.http()
        if LooseVersion(requests.__version__) >= LooseVersion('1.0.0'):
            self.assertTrue(False)
            try:
                http.get("/")
                self.assertTrue(False)
            except requests.models.SSLError, e:
                self.assertTrue("SSL3_GET_SERVER_CERTIFICATE:certificate verify failed" in str(e.message))
            except AuthenticationError:
                self.fail("Expected to Receive an SSL error from requests, but received an Authentication Error instead, check your local openssl installation")
        else:
            try:
                http.get("/")
                self.assertTrue(False)
            except requests.models.SSLError, e:
                self.assertTrue("SSL3_GET_SERVER_CERTIFICATE:certificate verify failed" in str(e.message))
            except AuthenticationError:
                self.fail("Expected to Receive an SSL error from requests, but received an Authentication Error instead, check your local openssl installation")


    def test_unsuccessful_connection_to_ssl_server_with_wrong_domain(self):
        environment = Environment("braintreegateway.com", "443", True, Environment.Production.ssl_certificate)
        config = Configuration(environment, "merchant_id", "public_key", "private_key")
        config._http_strategy = braintree.util.http_strategy.requests_strategy.RequestsStrategy(config, config.environment)
        http = config.http()
        if LooseVersion(requests.__version__) >= LooseVersion('1.0.0'):
            try:
                http.get("/")
                self.assertTrue(False)
            except requests.exceptions.SSLError, e:
                self.assertEquals("hostname 'braintreegateway.com' doesn't match u'www.braintreegateway.com'", str(e.message))
            except pycurl.error, e:
                error_code, error_msg = e
                self.assertEquals(pycurl.E_SSL_PEER_CERTIFICATE, error_code)
                self.assertTrue(re.search("SSL: certificate subject name", error_msg))
        else:
            try:
                http.get("/")
                self.assertTrue(False)
            except requests.models.SSLError, e:
                self.assertEquals("hostname 'braintreegateway.com' doesn't match u'www.braintreegateway.com'", str(e.message))
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
