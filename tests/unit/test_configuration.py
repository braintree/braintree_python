from tests.test_helper import *
import braintree
import os

class TestConfiguration(unittest.TestCase):
    def test_works_with_unconfigured_configuration(self):
        try:
            # reset class level attributes on Configuration set in test helper
            reload(braintree.configuration)
            config = Configuration(
                environment=braintree.Environment.Sandbox,
                merchant_id='my_merchant_id',
                public_key='public_key',
                private_key='private_key'
            )
            config.http_strategy()
        except AttributeError, e:
            print e
            self.assertTrue(False)
        finally:
            # repopulate class level attributes on Configuration
            import tests.test_helper
            reload(tests.test_helper)

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

    def test_configuration_construction_for_partner(self):
        config = Configuration.for_partner(
            environment=braintree.Environment.Sandbox,
            partner_id='my_partner_id',
            public_key='public_key',
            private_key='private_key'
        )
        self.assertEqual(config.merchant_id, 'my_partner_id')
        self.assertEqual(config.public_key, 'public_key')
        self.assertEqual(config.private_key, 'private_key')

    def test_overriding_http_strategy_blows_up_if_setting_an_invalid_strategy(self):
        old_http_strategy = None

        if "PYTHON_HTTP_STRATEGY" in os.environ:
            old_http_strategy = os.environ["PYTHON_HTTP_STRATEGY"]

        try:
            os.environ["PYTHON_HTTP_STRATEGY"] = "invalid"
            strategy = Configuration.instantiate().http_strategy()
            self.assertTrue(False, "Expected StandardError")
        except ValueError, e:
            self.assertEqual("invalid http strategy", e.message)
        finally:
            if old_http_strategy == None:
                del(os.environ["PYTHON_HTTP_STRATEGY"])
            else:
                os.environ["PYTHON_HTTP_STRATEGY"] = old_http_strategy

    def test_overriding_http_strategy(self):
        old_http_strategy = None

        if "PYTHON_HTTP_STRATEGY" in os.environ:
            old_http_strategy = os.environ["PYTHON_HTTP_STRATEGY"]

        try:
            os.environ["PYTHON_HTTP_STRATEGY"] = "httplib"
            strategy = Configuration.instantiate().http_strategy()
            self.assertTrue(isinstance(strategy, braintree.util.http_strategy.httplib_strategy.HttplibStrategy))
        finally:
            if old_http_strategy == None:
                del(os.environ["PYTHON_HTTP_STRATEGY"])
            else:
                os.environ["PYTHON_HTTP_STRATEGY"] = old_http_strategy

    def test_configuring_with_an_http_strategy(self):
        old_http_strategy = Configuration.default_http_strategy

        try:
            Configuration.default_http_strategy = braintree.util.http_strategy.httplib_strategy.HttplibStrategy
            strategy = Configuration.instantiate().http_strategy()
            self.assertTrue(isinstance(strategy, braintree.util.http_strategy.httplib_strategy.HttplibStrategy))
        finally:
            Configuration.default_http_strategy = old_http_strategy
