from tests.test_helper import *
import braintree
import os

class TestConfiguration(unittest.TestCase):
    def test_base_merchant_path_for_development(self):
        self.assertTrue("/merchants/integration_merchnat_id", Configuration.instantiate().base_merchant_path())

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
