from tests.test_helper import *
from distutils.version import LooseVersion
import platform
import braintree
import requests

class TestHttp(unittest.TestCase):
    if LooseVersion(requests.__version__) >= LooseVersion('1.0.0'):
        SSLError = requests.exceptions.SSLError
    else:
        SSLError = requests.models.SSLError

    def test_successful_connection_sandbox(self):
        http = self.get_http(Environment.Sandbox)
        try:
            http.get("/")
        except AuthenticationError:
            pass
        else:
            self.assertTrue(False)

    def test_successful_connection_production(self):
        http = self.get_http(Environment.Production)
        try:
            http.get("/")
        except AuthenticationError:
            pass
        else:
            self.assertTrue(False)

    def test_unsafe_ssl_connection(self):
        Configuration.use_unsafe_ssl = True;
        environment = Environment(Environment.Sandbox.server, "443", True, Environment.Production.ssl_certificate)
        http = self.get_http(environment)
        try:
            http.get("/")
        except AuthenticationError:
            pass
        finally:
            Configuration.use_unsafe_ssl = False;

class TestPyCurl(CommonHttpTests, unittest.TestCase):
    def get_http(self, environment):
        config = Configuration(environment, "merchant_id", "public_key", "private_key")
        config._http_strategy = braintree.util.http_strategy.pycurl_strategy.PycurlStrategy(config, config.environment)
        return config.http()

    def test_unsuccessful_connection_to_good_ssl_server_with_wrong_cert(self):
        if platform.system() == "Darwin":
            return

        environment = Environment("www.google.com", "443", True, Environment.Production.ssl_certificate)
        http = self.get_http(environment)
        try:
            http.get("/")
        except pycurl.error as e:
            error_code, error_msg = e
            self.assertEquals(pycurl.E_SSL_CACERT, error_code)
            self.assertTrue(re.search('verif(y|ication) failed', error_msg))
        except AuthenticationError:
            self.fail("Expected to receive an SSL error but received an Authentication Error instead, check your local openssl installation")
        else:
            self.fail("Expected to receive an SSL error but no exception was raised")

    def test_unsuccessful_connection_to_ssl_server_with_wrong_domain(self):
        #ip address of api.braintreegateway.com
        environment = Environment("204.109.13.121", "443", True, Environment.Production.ssl_certificate)
        http = self.get_http(environment)
        try:
            http.get("/")
        except pycurl.error as e:
            error_code, error_msg = e
            self.assertEquals(pycurl.E_SSL_PEER_CERTIFICATE, error_code)
            self.assertTrue(re.search("SSL: certificate subject name", error_msg))
        else:
            self.fail("Expected to receive an SSL error but no exception was raised")

class TestRequests(CommonHttpTests, unittest.TestCase):
    if LooseVersion(requests.__version__) >= LooseVersion('1.0.0'):
        SSLError = requests.exceptions.SSLError
    else:
        SSLError = requests.models.SSLError

    def get_http(self, environment):
        config = Configuration(environment, "merchant_id", "public_key", "private_key")
        return config.http()

    def test_unsuccessful_connection_to_good_ssl_server_with_wrong_cert(self):
        if platform.system() == "Darwin":
            return

        environment = Environment("www.google.com", "443", True, Environment.Production.ssl_certificate)
        http = self.get_http(environment)
        try:
            http.get("/")
        except self.SSLError as e:
            self.assertTrue("SSL3_GET_SERVER_CERTIFICATE:certificate verify failed" in str(e))
        except AuthenticationError:
            self.fail("Expected to receive an SSL error but received an Authentication Error instead, check your local openssl installation")
        else:
            self.fail("Expected to receive an SSL error but no exception was raised")

    def test_unsuccessful_connection_to_ssl_server_with_wrong_domain(self):
        #ip address of api.braintreegateway.com
        environment = Environment("204.109.13.121", "443", True, Environment.Production.ssl_certificate)
        http = self.get_http(environment)
        try:
            http.get("/")
        except self.SSLError as e:
            pass
        else:
            self.fail("Expected to receive an SSL error but no exception was raised")
