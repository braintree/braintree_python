from tests.test_helper import *

class TestDocumentUpload(unittest.TestCase):
    @raises_with_regexp(KeyError, "'Invalid keys: bad_key'")
    def test_create_raises_exception_with_bad_keys(self):
        DocumentUpload.create({"bad_key": "value"})
