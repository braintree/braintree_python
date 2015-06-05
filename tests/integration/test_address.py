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
            "country_name": "United States of America",
            "country_code_alpha2": "US",
            "country_code_alpha3": "USA",
            "country_code_numeric": "840"
        })

        self.assertTrue(result.is_success)
        address = result.address
        self.assertEquals(customer.id, address.customer_id)
        self.assertEquals("Ben", address.first_name)
        self.assertEquals("Moore", address.last_name)
        self.assertEquals("Moore Co.", address.company)
        self.assertEquals("1811 E Main St", address.street_address)
        self.assertEquals("Suite 200", address.extended_address)
        self.assertEquals("Chicago", address.locality)
        self.assertEquals("Illinois", address.region)
        self.assertEquals("60622", address.postal_code)
        self.assertEquals("US", address.country_code_alpha2)
        self.assertEquals("USA", address.country_code_alpha3)
        self.assertEquals("840", address.country_code_numeric)
        self.assertEquals("United States of America", address.country_name)

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
        self.assertEquals(ErrorCodes.Address.CountryNameIsNotAccepted, result.errors.for_object("address").on("country_name")[0].code)
        self.assertEquals(ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted, result.errors.for_object("address").on("country_code_alpha2")[0].code)
        self.assertEquals(ErrorCodes.Address.CountryCodeAlpha3IsNotAccepted, result.errors.for_object("address").on("country_code_alpha3")[0].code)
        self.assertEquals(ErrorCodes.Address.CountryCodeNumericIsNotAccepted, result.errors.for_object("address").on("country_code_numeric")[0].code)

    def test_error_response_if_inconsistent_country(self):
        customer = Customer.create().customer
        result = Address.create({
            "customer_id": customer.id,
            "country_code_alpha2": "US",
            "country_code_alpha3": "MEX"
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.Address.InconsistentCountry, result.errors.for_object("address").on("base")[0].code)

    def test_delete_with_valid_customer_id_and_address_id(self):
        customer = Customer.create().customer
        address = Address.create({"customer_id": customer.id, "street_address": "123 Main St."}).address
        result = Address.delete(customer.id, address.id)

        self.assertTrue(result.is_success)

    @raises(NotFoundError)
    def test_delete_with_valid_customer_id_and_non_existing_address(self):
        customer = Customer.create().customer
        result = Address.delete(customer.id, "notreal")

    def test_find_with_valid_customer_id_and_address_id(self):
        customer = Customer.create().customer
        address = Address.create({"customer_id": customer.id, "street_address": "123 Main St."}).address
        found_address = Address.find(customer.id, address.id)

        self.assertEquals(address.street_address, found_address.street_address)

    def test_find_with_invalid_customer_id_and_address_id(self):
        try:
            Address.find("notreal", "badaddress")
            self.assertTrue(False)
        except NotFoundError as e:
            self.assertEquals("address for customer 'notreal' with id 'badaddress' not found", str(e))

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
            "country_name": "Mexico"
        })

        self.assertTrue(result.is_success)
        address = result.address
        self.assertEquals(customer.id, address.customer_id)
        self.assertEquals("123 E New St", address.street_address)
        self.assertEquals("New Suite 3", address.extended_address)
        self.assertEquals("Chicago", address.locality)
        self.assertEquals("Illinois", address.region)
        self.assertEquals("60621", address.postal_code)
        self.assertEquals("MX", address.country_code_alpha2)
        self.assertEquals("MEX", address.country_code_alpha3)
        self.assertEquals("484", address.country_code_numeric)
        self.assertEquals("Mexico", address.country_name)

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
        self.assertEquals(ErrorCodes.Address.CountryNameIsNotAccepted, result.errors.for_object("address").on("country_name")[0].code)

    @raises(NotFoundError)
    def test_update_raises_not_found_error_if_given_bad_address(self):
        customer = Customer.create().customer
        Address.update(customer.id, "notfound", {"street_address": "123 Main St."})

