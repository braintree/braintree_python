from tests.test_helper import *

class TestCustomerSearch(unittest.TestCase):
    def test_advanced_search_no_results(self):
        collection = Transaction.search([
            TransactionSearch.billing_first_name == "no_such_person"
        ])
        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_searches_all_text_fields(self):
        token = "creditcard%s" % randint(1, 100000)

        customer = Customer.create({
            "first_name": "Timmy",
            "last_name": "O'Toole",
            "company": "O'Toole and Son(s)",
            "email": "timmy@example.com",
            "fax": "3145551234",
            "phone": "5551231234",
            "website": "http://example.com",
            "credit_card": {
                "cardholder_name": "Tim Toole",
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "token": token,
                "billing_address": {
                    "first_name": "Thomas",
                    "last_name": "Otool",
                    "street_address": "1 E Main St",
                    "extended_address": "Suite 3",
                    "locality": "Chicago",
                    "region": "Illinois",
                    "postal_code": "60622",
                    "country_name": "United States of America"
                }
            }
        }).customer

        search_criteria = {
            "first_name": "Timmy",
            "last_name": "O'Toole",
            "company": "O'Toole and Son(s)",
            "email": "timmy@example.com",
            "phone": "5551231234",
            "fax": "3145551234",
            "website": "http://example.com",
            "address_first_name": "Thomas",
            "address_last_name": "Otool",
            "address_street_address": "1 E Main St",
            "address_postal_code": "60622",
            "address_extended_address": "Suite 3",
            "address_locality": "Chicago",
            "address_region": "Illinois",
            "address_country_name": "United States of America",
            "payment_method_token": token,
            "cardholder_name": "Tim Toole",
            "credit_card_number": "4111111111111111",
            "credit_card_expiration_date": "05/2010"
        }

        criteria = [getattr(CustomerSearch, search_field) == value for search_field, value in search_criteria.items()]
        criteria.append(CustomerSearch.id == customer.id)

        collection = Customer.search(criteria)

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(customer.id, collection.first.id)

        for search_field, value in search_criteria.items():
            collection = Customer.search(
                CustomerSearch.id == customer.id,
                getattr(CustomerSearch, search_field) == value
            )

            self.assertEquals(1, collection.maximum_size)
            self.assertEquals(customer.id, collection.first.id)

    def test_advanced_search_range_node_created_at(self):
        customer = Customer.create().customer

        past = customer.created_at - timedelta(minutes=10)
        future = customer.created_at + timedelta(minutes=10)

        collection = Customer.search(
            CustomerSearch.id == customer.id,
            CustomerSearch.created_at.between(past, future)
        )

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(customer.id, collection.first.id)

        collection = Customer.search(
            CustomerSearch.id == customer.id,
            CustomerSearch.created_at <= future
        )

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(customer.id, collection.first.id)

        collection = Customer.search(
            CustomerSearch.id == customer.id,
            CustomerSearch.created_at >= past
        )

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(customer.id, collection.first.id)
