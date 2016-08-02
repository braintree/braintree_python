from tests.test_helper import *

class TestSuccessfulResult(unittest.TestCase):
    def test_is_success(self):
        self.assertTrue(SuccessfulResult({}).is_success)

    def test_attributes_are_exposed(self):
        result = SuccessfulResult({"name": "drew"})
        self.assertEqual("drew", result.name)
