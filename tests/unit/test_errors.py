import unittest
from braintree.errors import Errors

class TestErrors(unittest.TestCase):
    def test_errors_for_the_given_scope(self):
        errors = Errors({"level1": {"errors": [{"code": "code1", "attribute": "attr", "message": "message"}]}})
        self.assertEquals(1, errors.for_object("level1").size)

