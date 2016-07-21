import os
from nose.exc import SkipTest
from tests.test_helper import *
from braintree.test.nonces import Nonces

class TestDocumentUpload(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "fixtures/bt_logo.png")
        self.png_file = open(file_path, "rb")

    def test_create_returns_successful_result_if_valid(self):
        raise SkipTest("[BTMKPL-796] Will not work until Gateway controller changes are made")
        result = DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.IdentityDocument,
            "file": self.png_file
        })

        self.assertTrue(result.is_success)
