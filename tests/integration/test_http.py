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

    @staticmethod
    def get_http(environment):
        config = Configuration(environment, "merchant_id", public_key="public_key", private_key="private_key")
        return config.http()

    def test_successful_connection_sandbox(self):
        with self.assertRaises(Exception):
            http = self.get_http(Environment.Sandbox)
            http.get("/")

    def test_successful_connection_production(self):
        with self.assertRaises(Exception):
            http = self.get_http(Environment.Production)
            http.get("/")

    def test_wrapping_http_exceptions(self):
        config = Configuration(
            Environment("test", "localhost", "1", False, None, Environment.Production.ssl_certificate),
            "integration_merchant_id",
            public_key="integration_public_key",
            private_key="integration_private_key",
            wrap_http_exceptions=True
        )

        gateway = braintree.braintree_gateway.BraintreeGateway(config)

        try:
            gateway.transaction.find("my_id")
        except braintree.exceptions.unexpected_error.UnexpectedError:
            correct_exception = True
        except Exception:
            correct_exception = False

        self.assertTrue(correct_exception)

    def test_unsuccessful_connection_to_good_ssl_server_with_wrong_cert(self):
        if platform.system() == "Darwin":
            return

        #any endpoint that returns valid XML with a status of 3xx or less and serves SSL
        environment = Environment("test", "github.com", "443", "http://auth.venmo.dev:9292", True, Environment.Production.ssl_certificate)
        http = self.get_http(environment)
        try:
            http.get("/")
        except self.SSLError as e:
            self.assertTrue("certificate verify failed" in str(e))
        except AuthenticationError:
            self.fail("Expected to receive an SSL error but received an Authentication Error instead, check your local openssl installation")
        else:
            self.fail("Expected to receive an SSL error but no exception was raised")

    def test_unsuccessful_connection_to_ssl_server_with_wrong_domain(self):
        environment = Environment("test", "52.40.66.148", "443", "http://auth.venmo.dev:9292", True, Environment.Production.ssl_certificate)
        http = self.get_http(environment)
        try:
            http.get("/")
        except self.SSLError:
            pass
        else:
            self.fail("Expected to receive an SSL error but no exception was raised")

    def test_timeouts(self):
        config = Configuration(
            Environment.Development,
            "integration_merchant_id",
            public_key="integration_public_key",
            private_key="integration_private_key",
            wrap_http_exceptions=True,
            timeout=0.001
        )

        gateway = braintree.braintree_gateway.BraintreeGateway(config)

        try:
            gateway.transaction.find("my_id")
        except braintree.exceptions.http.timeout_error.TimeoutError:
            correct_exception = True
        except Exception:
            correct_exception = False

        self.assertTrue(correct_exception)

    def test_sessions_include_proxy_environments(self):
        proxies = {'https': 'http://i-clearly-dont-work', 'http': 'https://i-clearly-dont-work'}
        os.environ['HTTP_PROXY'] = proxies['http']
        os.environ['HTTPS_PROXY'] = proxies['https']
        self.assertEqual(requests.utils.getproxies(), proxies)

        config = Configuration(
            Environment.Development,
            "integration_merchant_id",
            public_key="integration_public_key",
            private_key="integration_private_key",
            wrap_http_exceptions=True,
        )
        gateway = braintree.braintree_gateway.BraintreeGateway(config)

        try:
            gateway.plan.all()
            os.environ.clear()
            assert False, "The proxy is invalid this request should not be successful."
        except Exception as e:
            os.environ.clear()
            assert 'Cannot connect to proxy' in str(e)
