from tests.test_helper import *

class TestEnvironment(unittest.TestCase):
    def test_server_and_port_for_development(self):
        port = os.getenv("GATEWAY_PORT") or "3000"
        self.assertEquals("localhost:" + port, Environment.DEVELOPMENT.server_and_port)

    def test_server_and_port_for_sandbox(self):
        self.assertEquals("sandbox.braintreegateway.com:443", Environment.SANDBOX.server_and_port)

    def test_server_and_port_for_production(self):
        self.assertEquals("www.braintreegateway.com:443", Environment.PRODUCTION.server_and_port)

    def test_server_for_development(self):
        self.assertEquals("localhost", Environment.DEVELOPMENT.server)

    def test_server_for_sandbox(self):
        self.assertEquals("sandbox.braintreegateway.com", Environment.SANDBOX.server)

    def test_server_for_production(self):
        self.assertEquals("www.braintreegateway.com", Environment.PRODUCTION.server)

    def test_port_for_development(self):
        port = os.getenv("GATEWAY_PORT") or "3000"
        port = int(port)
        self.assertEquals(port, Environment.DEVELOPMENT.port)

    def test_port_for_sandbox(self):
        self.assertEquals(443, Environment.SANDBOX.port)

    def test_port_for_production(self):
        self.assertEquals(443, Environment.PRODUCTION.port)

    def test_is_ssl_for_development(self):
        self.assertFalse(Environment.DEVELOPMENT.is_ssl)

    def test_is_ssl_for_sandbox(self):
        self.assertTrue(Environment.SANDBOX.is_ssl)

    def test_is_ssl_for_production(self):
        self.assertTrue(Environment.PRODUCTION.is_ssl)

    def test_protocol_for_development(self):
        self.assertEquals("http://", Environment.DEVELOPMENT.protocol)

    def test_protocol_for_sandbox(self):
        self.assertEquals("https://", Environment.SANDBOX.protocol)

    def test_protocol_for_production(self):
        self.assertEquals("https://", Environment.PRODUCTION.protocol)

    def test_ssl_certificate_for_development(self):
        self.assertEquals(None, Environment.DEVELOPMENT.ssl_certificate)

    def test_ssl_certificate_for_sandbox(self):
        self.assertEquals("braintree/ssl/valicert_ca.crt", Environment.SANDBOX.ssl_certificate)

    def test_ssl_certificate_for_production(self):
        self.assertEquals("braintree/ssl/securetrust_ca.crt", Environment.PRODUCTION.ssl_certificate)
