from tests.test_helper import *

class TestErrors(unittest.TestCase):
    def test_errors_for_the_given_scope(self):
        errors = Errors({"level1": {"errors": [{"code": "code1", "attribute": "attr", "message": "message"}]}})
        self.assertEquals(1, errors.for_object("level1").size)
        self.assertEquals(1, len(errors.for_object("level1")))

    def test_for_object_returns_empty_errors_collection_if_no_errors_at_given_scope(self):
        errors = Errors({"level1": {"errors": [{"code": "code1", "attribute": "attr", "message": "message"}]}})
        self.assertEquals(0, errors.for_object("no_errors_here").size)
        self.assertEquals(0, len(errors.for_object("no_errors_here")))

    def test_size_returns_number_of_errors_at_first_level_if_only_one_level_exists(self):
        hash = {
            "level1": {"errors": [{"code": "code1", "attribute": "attr", "message": "message"}]}
        }
        self.assertEqual(1, Errors(hash).size)
        self.assertEqual(1, len(Errors(hash)))

    def test_size_returns_number_of_errors_at_all_levels(self):
        hash = {
            "level1": {
                "errors": [{"code": "code1", "attribute": "attr", "message": "message"}],
                "level2": {
                    "errors": [
                        {"code": "code2", "attribute": "attr", "message": "message"},
                        {"code": "code3", "attribute": "attr", "message": "message"}
                    ]
                }
            }
        }
        self.assertEqual(3, Errors(hash).size)
        self.assertEqual(3, len(Errors(hash)))

    def test_all_returns_all_errors(self):
        hash = {
            "level1": {
                "errors": [{"code": "code1", "attribute": "attr", "message": "message"}],
                "level2": {
                    "errors": [
                        {"code": "code2", "attribute": "attr", "message": "message"},
                        {"code": "code3", "attribute": "attr", "message": "message"}
                    ]
                }
            }
        }

        errors = Errors(hash).all
        self.assertEquals(["code1", "code2", "code3"], [error.code for error in errors])

