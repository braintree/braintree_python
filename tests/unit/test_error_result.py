from tests.test_helper import *

class TestErrorResult(unittest.TestCase):
    def test_it_initializes_params_and_errors(self):
        errors = {
            "scope": {
                "errors": [{"code": 123, "message": "something is invalid", "attribute": "something"}]
            }
        }

        result = ErrorResult("gateway", {"errors": errors, "params": "params", "message": "brief description"})
        self.assertFalse(result.is_success)
        self.assertEquals("params", result.params)
        self.assertEquals(1, result.errors.size)
        self.assertEquals("something is invalid", result.errors.for_object("scope")[0].message)
        self.assertEquals("something", result.errors.for_object("scope")[0].attribute)
        self.assertEquals(123, result.errors.for_object("scope")[0].code)

    def test_it_ignores_other_params(self):
        errors = {
            "scope": {
                "errors": [{"code": 123, "message": "something is invalid", "attribute": "something"}]
            }
        }

        result = ErrorResult("gateway", {"errors": errors, "params": "params", "message": "brief description", "other": "stuff"})
        self.assertFalse(result.is_success)

    def test_transaction_is_none_if_not_set(self):
        result = ErrorResult("gateway", {"errors": {}, "params": {}, "message": "brief description"})
        self.assertTrue(result.transaction == None)

    def test_verification_is_none_if_not_set(self):
        result = ErrorResult("gateway", {"errors": {}, "params": {}, "message": "brief description"})
        self.assertTrue(result.credit_card_verification == None)
