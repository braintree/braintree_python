import unittest
from braintree.environment import Environment
from braintree.configuration import Configuration

class TestConfiguration(unittest.TestCase):
    def test_server_for_development(self):
        Configuration.environment = Environment.DEVELOPMENT
        self.assertEquals("localhost", Configuration().server())

    def test_server_for_production(self):
        Configuration.environment = Environment.PRODUCTION
        self.assertEquals("www.braintreegateway.com", Configuration().server())

    def test_server_for_sandbox(self):
        Configuration.environment = Environment.SANDBOX
        self.assertEquals("sandbox.braintreegateway.com", Configuration().server())

    def test_port_for_development(self):
        Configuration.environment = Environment.DEVELOPMENT
        self.assertEquals(3000, Configuration().port())

    def test_port_for_production(self):
        Configuration.environment = Environment.PRODUCTION
        self.assertEquals(443, Configuration().port())

    def test_server_and_port(self):
        Configuration.environment = Environment.DEVELOPMENT
        self.assertEquals("localhost:3000", Configuration.server_and_port())

    def test_ssl_for_development(self):
        Configuration.environment = Environment.DEVELOPMENT
        self.assertFalse(Configuration.ssl())

    def test_ssl_for_production(self):
        Configuration.environment = Environment.PRODUCTION
        self.assertTrue(Configuration.ssl())

    def test_base_merchant_path_for_development(self):
        self.assertTrue("/merchants/integration_merchnat_id", Configuration.base_merchant_path())
