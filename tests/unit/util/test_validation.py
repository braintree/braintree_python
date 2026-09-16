from tests.test_helper import *
from braintree.util.validation import is_invalid_path_segment

class TestValidation(unittest.TestCase):
    def test_valid_segments_return_false(self):
        for segment in ["customer123", "CUSTOMER_123", "a-b_c-D9", "1234567890", "a"]:
            self.assertFalse(is_invalid_path_segment(segment), segment)

    def test_invalid_segments_return_true(self):
        for segment in [
            "",
            "   ",
            ".",
            "..",
            "foo/bar",
            "foo\\bar",
            "foo%bar",
            "..%2f..%2fvictim",
            "%2e%2e",
            "../../victim_customer/addresses/victim_address",
            "abc.def",
            "abc def",
            None,
            123,
            {},
            [],
        ]:
            self.assertTrue(is_invalid_path_segment(segment), repr(segment))
