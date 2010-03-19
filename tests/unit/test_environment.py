import os
import unittest
import tests.test_helper
from braintree.environment import Environment

class TestEnvironment(unittest.TestCase):
    def test_server_for_development(self):
        self.assertEquals("localhost", Environment.DEVELOPMENT.server)

    def test_server_for_production(self):
        self.assertEquals("www.braintreegateway.com", Environment.PRODUCTION.server)

    def test_server_for_sandbox(self):
        self.assertEquals("sandbox.braintreegateway.com", Environment.SANDBOX.server)

    def test_port_for_development(self):
        self.assertEquals('3000', Environment.DEVELOPMENT.port)

    def test_port_for_development(self):
        port = os.getenv("GATEWAY_PORT") or '3000'
        self.assertEquals(port, Environment.DEVELOPMENT.port)

    def test_port_for_sandbox(self):
        self.assertEquals('443', Environment.SANDBOX.port)

    def test_port_for_production(self):
        self.assertEquals('443', Environment.PRODUCTION.port)

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
