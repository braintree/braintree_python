from tests.test_helper import *

class TestAddress(unittest.TestCase):
    def test_create_returns_successful_result_if_valid(self):
        customer = Customer.create().customer
        result = Address.create({
            "customer_id": customer.id,
            "first_name": "Ben",
            "last_name": "Moore",
            "company": "Moore Co.",
            "street_address": "1811 E Main St",
            "extended_address": "Suite 200",
            "locality": "Chicago",
            "region": "Illinois",
            "postal_code": "60622",
            "phone_number": "8675309",
            "international_phone": {"country_code": "1", "national_number": "3121234567"},
            "country_name": "United States of America",
            "country_code_alpha2": "US",
            "country_code_alpha3": "USA",
            "country_code_numeric": "840"
        })

        self.assertTrue(result.is_success)
        address = result.address
        self.assertEqual(customer.id, address.customer_id)
        self.assertEqual("Ben", address.first_name)
        self.assertEqual("Moore", address.last_name)
        self.assertEqual("Moore Co.", address.company)
        self.assertEqual("1811 E Main St", address.street_address)
        self.assertEqual("Suite 200", address.extended_address)
        self.assertEqual("Chicago", address.locality)
        self.assertEqual("Illinois", address.region)
        self.assertEqual("60622", address.postal_code)
        self.assertEqual("8675309", address.phone_number)
        self.assertEqual("1", address.international_phone["country_code"])
        self.assertEqual("3121234567", address.international_phone["national_number"])
        self.assertEqual("US", address.country_code_alpha2)
        self.assertEqual("USA", address.country_code_alpha3)
        self.assertEqual("840", address.country_code_numeric)
        self.assertEqual("United States of America", address.country_name)

    def test_error_response_if_invalid(self):
        customer = Customer.create().customer
        result = Address.create({
            "customer_id": customer.id,
            "country_name": "zzzzzz",
            "country_code_alpha2": "zz",
            "country_code_alpha3": "zzz",
            "country_code_numeric": "000"
        })

        self.assertFalse(result.is_success)

        country_name_errors = result.errors.for_object("address").on("country_name")
        self.assertEqual(1, len(country_name_errors))
        self.assertEqual(ErrorCodes.Address.CountryNameIsNotAccepted, country_name_errors[0].code)

        country_code_alpha2_errors = result.errors.for_object("address").on("country_code_alpha2")
        self.assertEqual(1, len(country_code_alpha2_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted, country_code_alpha2_errors[0].code)

        country_code_alpha3_errors = result.errors.for_object("address").on("country_code_alpha3")
        self.assertEqual(1, len(country_code_alpha3_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeAlpha3IsNotAccepted, country_code_alpha3_errors[0].code)

        country_code_numeric_errors = result.errors.for_object("address").on("country_code_numeric")
        self.assertEqual(1, len(country_code_numeric_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeNumericIsNotAccepted, country_code_numeric_errors[0].code)

    def test_error_response_if_inconsistent_country(self):
        customer = Customer.create().customer
        result = Address.create({
            "customer_id": customer.id,
            "country_code_alpha2": "US",
            "country_code_alpha3": "MEX"
        })

        self.assertFalse(result.is_success)

        address_errors = result.errors.for_object("address").on("base")
        self.assertEqual(1, len(address_errors))
        self.assertEqual(ErrorCodes.Address.InconsistentCountry, address_errors[0].code)

    def test_delete_with_valid_customer_id_and_address_id(self):
        customer = Customer.create().customer
        address = Address.create({"customer_id": customer.id, "street_address": "123 Main St."}).address
        result = Address.delete(customer.id, address.id)

        self.assertTrue(result.is_success)

    def test_delete_with_valid_customer_id_and_non_existing_address(self):
        with self.assertRaises(NotFoundError):
            customer = Customer.create().customer
            Address.delete(customer.id, "notreal")

    def test_find_with_valid_customer_id_and_address_id(self):
        customer = Customer.create().customer
        address = Address.create({"customer_id": customer.id, "street_address": "123 Main St."}).address
        found_address = Address.find(customer.id, address.id)

        self.assertEqual(address.street_address, found_address.street_address)

    def test_find_with_invalid_customer_id_and_address_id(self):
        with self.assertRaisesRegex(NotFoundError, "address for customer 'notreal' with id 'badaddress' not found"):
            Address.find("notreal", "badaddress")

    def test_update_with_valid_values(self):
        customer = Customer.create().customer
        address = Address.create({
            "customer_id": customer.id,
            "street_address": "1811 E Main St",
            "extended_address": "Suite 200",
            "locality": "Chicago",
            "region": "Illinois",
            "postal_code": "60622",
            "country_name": "United States of America"
        }).address

        result = Address.update(customer.id, address.id, {
            "street_address": "123 E New St",
            "extended_address": "New Suite 3",
            "locality": "Chicago",
            "region": "Illinois",
            "postal_code": "60621",
            "country_code_alpha2": "MX",
            "country_code_alpha3": "MEX",
            "country_code_numeric": "484",
            "country_name": "Mexico",
            "phone_number": "8675309",
            "international_phone": {"country_code": "1", "national_number": "3121234567"}
        })

        self.assertTrue(result.is_success)
        address = result.address
        self.assertEqual(customer.id, address.customer_id)
        self.assertEqual("123 E New St", address.street_address)
        self.assertEqual("New Suite 3", address.extended_address)
        self.assertEqual("Chicago", address.locality)
        self.assertEqual("Illinois", address.region)
        self.assertEqual("60621", address.postal_code)
        self.assertEqual("MX", address.country_code_alpha2)
        self.assertEqual("MEX", address.country_code_alpha3)
        self.assertEqual("484", address.country_code_numeric)
        self.assertEqual("Mexico", address.country_name)
        self.assertEqual("8675309", address.phone_number)
        self.assertEqual("1", address.international_phone["country_code"])
        self.assertEqual("3121234567", address.international_phone["national_number"])

    def test_update_with_invalid_values(self):
        customer = Customer.create().customer
        address = Address.create({
            "customer_id": customer.id,
            "street_address": "1811 E Main St",
            "extended_address": "Suite 200",
            "locality": "Chicago",
            "region": "Illinois",
            "postal_code": "60622",
            "country_name": "United States of America"
        }).address

        result = Address.update(customer.id, address.id, {
            "street_address": "123 E New St",
            "country_name": "United States of Invalid"
        })

        self.assertFalse(result.is_success)

        country_name_errors = result.errors.for_object("address").on("country_name")
        self.assertEqual(1, len(country_name_errors))
        self.assertEqual(ErrorCodes.Address.CountryNameIsNotAccepted, country_name_errors[0].code)

    def test_update_raises_not_found_error_if_given_bad_address(self):
        with self.assertRaises(NotFoundError):
            customer = Customer.create().customer
            Address.update(customer.id, "notfound", {"street_address": "123 Main St."})
