import unittest
from braintree.successful_result import SuccessfulResult

class TestSuccessfulResult(unittest.TestCase):
    def test_is_success(self):
        self.assertTrue(SuccessfulResult({}).is_success)
