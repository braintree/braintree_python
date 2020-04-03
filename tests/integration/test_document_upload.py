import os
from nose.exc import SkipTest
from tests.test_helper import *
from braintree.test.nonces import Nonces

class TestDocumentUpload(unittest.TestCase):
    def setUp(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "fixtures/bt_logo.png")
        self.png_file = open(file_path, "rb")

    def test_create_returns_successful_result_if_valid(self):
        result = DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
            "file": self.png_file
        })

        self.assertTrue(result.is_success)
        self.assertTrue(result.document_upload.id != None)
        self.assertEqual(result.document_upload.content_type, "image/png")
        self.assertEqual(result.document_upload.kind, braintree.DocumentUpload.Kind.EvidenceDocument)
        self.assertEqual(result.document_upload.name, "bt_logo.png")
        self.assertEqual(result.document_upload.size, 2443)

    def test_create_returns_error_with_unsupported_file_type(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "fixtures/gif_extension_bt_logo.gif")
        gif_file = open(file_path, "rb")

        result = DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
            "file": gif_file
        })

        self.assertEqual(result.errors.for_object("document_upload")[0].code, ErrorCodes.DocumentUpload.FileTypeIsInvalid)

    def test_create_returns_error_with_malformed_file(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "fixtures/malformed_pdf.pdf")
        bad_pdf_file = open(file_path, "rb")

        result = DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
            "file": bad_pdf_file
        })

        self.assertEqual(result.errors.for_object("document_upload")[0].code, ErrorCodes.DocumentUpload.FileIsMalformedOrEncrypted)

    def test_create_returns_error_with_invalid_kind(self):
        result = DocumentUpload.create({
            "kind": "invalid_kind",
            "file": self.png_file
        })

        self.assertEqual(result.errors.for_object("document_upload")[0].code, ErrorCodes.DocumentUpload.KindIsInvalid)

    def test_create_returns_error_when_file_is_over_4mb(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "fixtures/large_file.png")
        try:
            f = open(file_path, 'w+')
            for i in range(1048577 * 4):
                f.write('a')
            f.close()

            large_file = open(file_path, 'rb')

            result = DocumentUpload.create({
                "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
                "file": large_file
            })

            self.assertEqual(result.errors.for_object("document_upload")[0].code, ErrorCodes.DocumentUpload.FileIsTooLarge)
        finally:
            os.remove(file_path)

    def test_create_returns_error_when_file_is_empty(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "fixtures/empty_file.png")
        try:
            f = open(file_path, 'w')
            f.close()

            empty_file = open(file_path, 'rb')

            result = DocumentUpload.create({
                "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
                "file": empty_file
            })

            self.assertEqual(result.errors.for_object("document_upload")[0].code, ErrorCodes.DocumentUpload.FileIsEmpty)
        finally:
            os.remove(file_path)

    def test_create_returns_error_with_too_long_file(self):
        file_path = os.path.join(os.path.dirname(__file__), "..", "fixtures/too_long.pdf")
        too_long_pdf = open(file_path, "rb")

        result = DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
            "file": too_long_pdf
        })

        self.assertEqual(result.errors.for_object("document_upload")[0].code, ErrorCodes.DocumentUpload.FileIsTooLong)

    @raises_with_regexp(KeyError, "'Invalid keys: invalid_key'")
    def test_create_returns_invalid_keys_errors_with_invalid_signature(self):
        result = DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
            "invalid_key": "do not add"
        })

    @raises_with_regexp(ValueError, "file must be a file handle")
    def test_create_throws_error_when_not_valid_file(self):
        result = DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
            "file": "not_a_file"
        })

    @raises_with_regexp(ValueError, "file must be a file handle")
    def test_create_throws_error_when_none_file(self):
        result = DocumentUpload.create({
            "kind": braintree.DocumentUpload.Kind.EvidenceDocument,
            "file": None
        })
