import unittest
from braintree.error_result import ErrorResult

class TestErrorResult(unittest.TestCase):
    def test_it_initializes_params_and_errors(self):
        errors = {
            "scope": {
                "errors": [{"code": 123, "message": "something is invalid", "attribute": "something"}]
            }
        }

        result = ErrorResult({"errors": errors, "params": "params"})
        self.assertFalse(result.is_success)
        self.assertEquals("params", result.params)
        self.assertEquals(1, result.errors.size)
        self.assertEquals("something is invalid", result.errors.for_object("scope")[0].message)
        self.assertEquals("something", result.errors.for_object("scope")[0].attribute)
        self.assertEquals(123, result.errors.for_object("scope")[0].code)
