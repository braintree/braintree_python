from tests.test_helper import *

class TestEnvironment(unittest.TestCase):
    def test_server_and_port_for_development(self):
        port = os.getenv("GATEWAY_PORT") or '3000'
        self.assertEquals("localhost:" + port, Environment.DEVELOPMENT.server_and_port)

    def test_server_and_port_for_sandbox(self):
        self.assertEquals("sandbox.braintreegateway.com:443", Environment.SANDBOX.server_and_port)

    def test_server_and_port_for_production(self):
        self.assertEquals("www.braintreegateway.com:443", Environment.PRODUCTION.server_and_port)

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
