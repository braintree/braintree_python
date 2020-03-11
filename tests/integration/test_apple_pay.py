from tests.test_helper import *

class TestApplePay(unittest.TestCase):
    @staticmethod
    def get_gateway():
        config = Configuration("development", "integration_merchant_id",
                               public_key="integration_public_key",
                               private_key="integration_private_key")
        return BraintreeGateway(config)

    def test_register_domain_registers_an_apple_pay_domain(self):
        result = self.get_gateway().apple_pay.register_domain("www.example.com")

        self.assertTrue(result.is_success)

    def test_register_domain_gets_a_validation_error_when_attempting_to_register_no_domains(self):
        result = self.get_gateway().apple_pay.register_domain("")

        self.assertFalse(result.is_success)
        self.assertEqual(result.errors.for_object("apple_pay")[0].message, "Domain name is required.")

    def test_unregister_domain_unregisters_an_apple_pay_domain(self):
        result = self.get_gateway().apple_pay.unregister_domain("example.org")
        self.assertTrue(result.is_success)

    def test_unregister_domain_unregisters_an_apple_pay_domain_with_schem_in_url(self):
        result = self.get_gateway().apple_pay.unregister_domain("http://example.org")
        self.assertTrue(result.is_success)

    def test_unregister_domain_escapes_the_unregistered_domain_query_parameter(self):
        result = self.get_gateway().apple_pay.unregister_domain("ex&mple.org")
        self.assertTrue(result.is_success)

    def test_registered_domains_returns_stubbed_registered_domains(self):
        result = self.get_gateway().apple_pay.registered_domains()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "www.example.com")
