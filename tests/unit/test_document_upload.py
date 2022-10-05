from tests.test_helper import *

class TestDocumentUpload(unittest.TestCase):
    def test_create_raises_exception_with_bad_keys(self):
        with self.assertRaisesRegex(KeyError, "'Invalid keys: bad_key'"):
            DocumentUpload.create({"bad_key": "value"})
