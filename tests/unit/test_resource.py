from tests.test_helper import *
from braintree.resource import Resource

class TestResource(unittest.TestCase):
    def test_verify_keys_allows_wildcard_keys(self):
        signature = [
            {"foo": [{"bar": ["__any_key__"]}]}
        ]
        params = {
            "foo[bar][lower]": "lowercase",
            "foo[bar][UPPER]": "uppercase",
            "foo[bar][123]": "numeric",
            "foo[bar][under_scores]": "underscores",
            "foo[bar][dash-es]": "dashes",
            "foo[bar][ABC-abc_123]": "all together"
        }
        Resource.verify_keys(params, signature)

    def test_verify_keys_escapes_brackets_in_signature(self):
        signature = [
            {"customer": [{"custom_fields": ["__any_key__"]}]}
        ]
        params = {
            "customer_id": "value",
        }
        with self.assertRaises(KeyError):
            Resource.verify_keys(params, signature)

    def test_verify_keys_works_with_array_param(self):
        signature = [
            {"customer": ["one", "two"]}
        ]
        params = {
            "customer": {
                "one": "foo"
            }
        }
        Resource.verify_keys(params, signature)

    def test_verify_keys_raises_on_bad_array_param(self):
        signature = [
            {"customer": ["one", "two"]}
        ]
        params = {
            "customer": {
                "invalid": "foo"
            }
        }
        with self.assertRaises(KeyError):
            Resource.verify_keys(params, signature)

    def test_verify_keys_works_with_arrays(self):
        signature = [
            {"add_ons": [{"update": ["existing_id", "quantity"]}]}
        ]
        params = {
            "add_ons": {
                "update": [
                    {
                        "existing_id": "foo",
                        "quantity": 10
                    }
                ]
            }
        }
        Resource.verify_keys(params, signature)

    def test_verify_keys_raises_with_invalid_param_in_arrays(self):
        signature = [
            {"add_ons": [{"update": ["existing_id", "quantity"]}]}
        ]
        params = {
            "add_ons": {
                "update": [
                    {
                        "invalid": "foo",
                        "quantity": 10
                    }
                ]
            }
        }
        with self.assertRaises(KeyError):
            Resource.verify_keys(params, signature)

    def test_verify_keys_allows_text(self):
        text_string = u"text_string"
        assert isinstance(text_string, TestHelper.text_type)

        signature = [
            {"customer": [{"custom_fields": [text_string]}]}
        ]
        params = {
            "customer": {
                "custom_fields": {
                    text_string : text_string
                }
            }
        }
        Resource.verify_keys(params, signature)

    def test_verify_keys_allows_raw_data(self):
        raw_string = str.encode("raw_string")
        assert isinstance(raw_string, TestHelper.raw_type)

        signature = [
            {"customer": [{"custom_fields": [raw_string]}]}
        ]
        params = {
            "customer": {
                "custom_fields": {
                    raw_string : raw_string
                }
            }
        }
        Resource.verify_keys(params, signature)
