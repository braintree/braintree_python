import traceback

from tests.test_helper import *
from braintree.attribute_getter import AttributeGetter

class TestHttp(unittest.TestCase):
    def test_raise_exception_from_status_for_upgrade_required(self):
        try:
            Http.raise_exception_from_status(426)
            self.assertTrue(False)
        except UpgradeRequiredError:
            pass

    def test_backtrace_preserved_when_not_wrapping_exceptions(self):
        class Error(Exception):
            pass
        def raise_error(*_):
            raise Error
        http_strategy = AttributeGetter({"http_do": raise_error})
        config = AttributeGetter({
                "base_url": (lambda: ""),
                "has_access_token": (lambda: False),
                "has_client_credentials": (lambda: False),
                "http_strategy": (lambda: http_strategy),
                "public_key": "",
                "private_key": "",
                "wrap_http_exceptions": False})

        try:
            Http(config, "a")._Http__http_do("a", "b")
        except Error as e:
            _, _, tb = sys.exc_info()
            self.assertEqual('raise_error', traceback.extract_tb(tb)[-1][2])
