from tests.test_helper import *
import braintree
import os
import imp

class TestConfiguration(unittest.TestCase):
    def test_works_with_unconfigured_configuration(self):
        try:
            # reset class level attributes on Configuration set in test helper
            imp.reload(braintree.configuration)
            config = Configuration(
                environment=braintree.Environment.Sandbox,
                merchant_id='my_merchant_id',
                public_key='public_key',
                private_key='private_key'
            )
            config.http_strategy()
        except AttributeError as e:
            print(e)
            self.assertTrue(False)
        finally:
            # repopulate class level attributes on Configuration
            import tests.test_helper
            imp.reload(tests.test_helper)

    def test_base_merchant_path_for_development(self):
        self.assertEqual("/merchants/integration_merchant_id", Configuration.instantiate().base_merchant_path())

    def test_configuration_construction_for_merchant(self):
        config = Configuration(
            environment=braintree.Environment.Sandbox,
            merchant_id='my_merchant_id',
            public_key='public_key',
            private_key='private_key'
        )
        self.assertEqual(config.merchant_id, 'my_merchant_id')
        self.assertEqual(config.public_key, 'public_key')
        self.assertEqual(config.private_key, 'private_key')

    def test_configuration_configure_allows_strings_for_environment(self):
        try:
            for environment_string, environment_object in braintree.Environment.All.items():
                braintree.Configuration.configure(
                    environment_string,
                    'my_merchant_id',
                    'public_key',
                    'private_key'
                )
                self.assertEqual(braintree.Configuration.environment, environment_object)
        finally:
            reset_braintree_configuration()

    def test_configuration_construction_allows_strings_for_environment(self):
        config = Configuration(
            environment='sandbox',
            merchant_id='my_merchant_id',
            public_key='public_key',
            private_key='private_key'
        )

        self.assertEqual(config.environment, braintree.Environment.Sandbox)

    def test_configuration_construction_allows_empty_parameter_list(self):
        config = Configuration()

        self.assertIsInstance(config, braintree.Configuration)

    def test_configuration_raises_configuration_error_for_invalid_environment(self):
        for environment in [42, 'not_an_env']:
            def setup_bad_configuration():
                Configuration(
                    environment=environment,
                    merchant_id='my_merchant_id',
                    public_key='public_key',
                    private_key='private_key'
                )

            self.assertRaises(ConfigurationError, setup_bad_configuration)

    def test_configuration_construction_for_partner(self):
        config = Configuration.for_partner(
            braintree.Environment.Sandbox,
            'my_partner_id',
            'public_key',
            'private_key'
        )
        self.assertEqual(config.merchant_id, 'my_partner_id')
        self.assertEqual(config.public_key, 'public_key')
        self.assertEqual(config.private_key, 'private_key')

    def test_configuring_with_an_http_strategy(self):
        old_http_strategy = Configuration.default_http_strategy

        class FakeStrategy(object):
            def __init__(self, config, environment):
                pass

        try:
            Configuration.default_http_strategy = FakeStrategy
            strategy = Configuration.instantiate().http_strategy()
            self.assertTrue(isinstance(strategy, FakeStrategy))
        finally:
            Configuration.default_http_strategy = old_http_strategy

    def test_configuring_with_partial_client_credentials(self):
        with self.assertRaises(ConfigurationError) as error:
            Configuration(client_id='client_id$development$integration_client_id')

        self.assertIn("Missing client_secret when constructing BraintreeGateway", str(error.exception))
