from tests.test_helper import *

class TestEnvironment(unittest.TestCase):
    def test_server_and_port_for_development(self):
        port = os.getenv("GATEWAY_PORT") or "3000"
        self.assertEquals("localhost:" + port, Environment.Development.server_and_port)

    def test_base_url(self):
        self.assertEquals("https://api.sandbox.braintreegateway.com:443", Environment.Sandbox.base_url)
        self.assertEquals("https://api.braintreegateway.com:443", Environment.Production.base_url)

    def test_server_and_port_for_sandbox(self):
        self.assertEquals("api.sandbox.braintreegateway.com:443", Environment.Sandbox.server_and_port)

    def test_server_and_port_for_production(self):
        self.assertEquals("api.braintreegateway.com:443", Environment.Production.server_and_port)

    def test_server_for_development(self):
        self.assertEquals("localhost", Environment.Development.server)

    def test_server_for_sandbox(self):
        self.assertEquals("api.sandbox.braintreegateway.com", Environment.Sandbox.server)

    def test_server_for_production(self):
        self.assertEquals("api.braintreegateway.com", Environment.Production.server)

    def test_port_for_development(self):
        port = os.getenv("GATEWAY_PORT") or "3000"
        port = int(port)
        self.assertEquals(port, Environment.Development.port)

    def test_port_for_sandbox(self):
        self.assertEquals(443, Environment.Sandbox.port)

    def test_port_for_production(self):
        self.assertEquals(443, Environment.Production.port)

    def test_is_ssl_for_development(self):
        self.assertFalse(Environment.Development.is_ssl)

    def test_is_ssl_for_sandbox(self):
        self.assertTrue(Environment.Sandbox.is_ssl)

    def test_is_ssl_for_production(self):
        self.assertTrue(Environment.Production.is_ssl)

    def test_protocol_for_development(self):
        self.assertEquals("http://", Environment.Development.protocol)

    def test_protocol_for_sandbox(self):
        self.assertEquals("https://", Environment.Sandbox.protocol)

    def test_protocol_for_production(self):
        self.assertEquals("https://", Environment.Production.protocol)

    def test_ssl_certificate_for_development(self):
        self.assertEquals(None, Environment.Development.ssl_certificate)

