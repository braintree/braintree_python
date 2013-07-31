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

    def get_http(self, environment):
        config = Configuration(environment, "merchant_id", "public_key", "private_key")
        return config.http()

    def test_unsuccessful_connection_to_good_ssl_server_with_wrong_cert(self):
        if platform.system() == "Darwin":
            return

        environment = Environment(Environment.Sandbox.server, "443", True, Environment.Production.ssl_certificate)
        http = self.get_http(environment)
        try:
            http.get("/")
        except self.SSLError as e:
            self.assertTrue("SSL3_GET_SERVER_CERTIFICATE:certificate verify failed" in str(e.message))
        except AuthenticationError:
            self.fail("Expected to receive an SSL error but received an Authentication Error instead, check your local openssl installation")
        else:
            self.fail("Expected to receive an SSL error but no exception was raised")

    def test_unsuccessful_connection_to_ssl_server_with_wrong_domain(self):
        environment = Environment("www.braintreepayments.com", "443", True, Environment.Production.ssl_certificate)
        http = self.get_http(environment)
        try:
            http.get("/")
        except self.SSLError as e:
            pass
        else:
            self.fail("Expected to receive an SSL error but no exception was raised")
