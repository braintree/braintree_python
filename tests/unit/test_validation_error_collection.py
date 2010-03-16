import unittest
from braintree.validation_error_collection import ValidationErrorCollection

class TestValidationErrorCollection(unittest.TestCase):
    def test_it_builds_an_array_of_errors_given_an_array_of_hashes(self):
        hash = {"errors": [{"attribute": "some model attribute", "code": 1, "message": "bad juju"}]}
        errors = ValidationErrorCollection(hash)
        error = errors[0]
        self.assertEquals("some model attribute", error.attribute)
        self.assertEquals(1, error.code)
        self.assertEquals("bad juju", error.message)

    def test_for_object_provides_access_to_nested_attributes(self):
        hash = {
            "errors": [{"attribute": "some model attribute", "code": 1, "message": "bad juju"}],
            "nested": {
                "errors": [{"attribute": "number", "code": 2, "message": "badder juju"}]
            }
        }
        errors = ValidationErrorCollection(hash)
        error = errors.for_object("nested").on("number")[0]

        self.assertEquals("number", error.attribute)
        self.assertEquals(2, error.code)
        self.assertEquals("badder juju", error.message)

    def test_deep_size_non_nested(self):
        hash = {
            "errors": [
                {"attribute": "one", "code": 1, "message": "is too long"},
                {"attribute": "two", "code": 2, "message": "contains invalid chars"},
                {"attribute": "thr", "code": 3, "message": "is invalid"}
            ]
        }

        self.assertEquals(3, ValidationErrorCollection(hash).deep_size)

    def test_deep_size_nested(self):
        hash = {
            "errors": [{"attribute": "one", "code": 1, "message": "is too long"}],
            "nested": {
                "errors": [{"attribute": "two", "code": 2, "message": "contains invalid chars"}]
            }
        }

        self.assertEquals(2, ValidationErrorCollection(hash).deep_size)
    # it "returns the size of nested errors as well" do
    #   errors = Braintree::ValidationErrorCollection.new(
    #     :errors => [{ :attribute => "some model attribute", :code => 1, :message => "bad juju" }],
    #     :nested => {
    #       :errors => [{ :attribute => "number", :code => 2, :message => "badder juju"}]
    #     }
    #   )
    #   errors.deep_size.should == 2
    # end

    # it "returns the size of multiple nestings of errors" do
    #   errors = Braintree::ValidationErrorCollection.new(
    #     :errors => [
    #       { :attribute => "one", :code => 1, :message => "bad juju" },
    #       { :attribute => "two", :code => 1, :message => "bad juju" }],
    #     :nested => {
    #       :errors => [{ :attribute => "three", :code => 2, :message => "badder juju"}],
    #       :nested_again => {
    #         :errors => [{ :attribute => "four", :code => 2, :message => "badder juju"}]
    #       }
    #     },
    #     :same_level => {
    #       :errors => [{ :attribute => "five", :code => 2, :message => "badder juju"}],
    #     }
    #   )
    #   errors.deep_size.should == 5
    # end

