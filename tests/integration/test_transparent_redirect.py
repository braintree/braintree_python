from tests.test_helper import *

class TestTransparentRedirect(unittest.TestCase):
    @raises(DownForMaintenanceError)
    def test_parse_and_validate_query_string_checks_http_status_before_hash(self):
        customer = Customer.create().customer
        tr_data = {
            "credit_card": {
                "customer_id": customer.id
            }
        }
        post_params = {
            "tr_data": CreditCard.tr_data_for_create(tr_data, "http://example.com/path?foo=bar"),
            "credit_card[cardholder_name]": "Card Holder",
            "credit_card[number]": "4111111111111111",
            "credit_card[expiration_date]": "05/2012",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Configuration.base_merchant_url() + "/test/maintenance")
        CreditCard.confirm_transparent_redirect(query_string)

    @raises(AuthenticationError)
    def test_parse_and_validate_query_string_raises_authentication_error_with_bad_credentials(self):
        customer = Customer.create().customer
        tr_data = {
            "credit_card": {
                "customer_id": customer.id
            }
        }

        old_private_key = Configuration.private_key
        try:
            Configuration.private_key = "bad"

            post_params = {
                "tr_data": CreditCard.tr_data_for_create(tr_data, "http://example.com/path?foo=bar"),
                "credit_card[cardholder_name]": "Card Holder",
                "credit_card[number]": "4111111111111111",
                "credit_card[expiration_date]": "05/2012",
            }
            query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_create_url())
            CreditCard.confirm_transparent_redirect(query_string)
        finally:
            Configuration.private_key = old_private_key

    def test_transaction_sale_from_transparent_redirect_with_successful_result(self):
        tr_data = {
            "transaction": {
                "amount": "1000.00",
            }
        }
        post_params = {
            "tr_data": Transaction.tr_data_for_sale(tr_data, "http://example.com/path"),
            "transaction[credit_card][number]": "4111111111111111",
            "transaction[credit_card][expiration_date]": "05/2010",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params)
        result = TransparentRedirect.confirm(query_string)
        self.assertTrue(result.is_success)

        transaction = result.transaction
        self.assertEquals(Decimal("1000.00"), transaction.amount)
        self.assertEquals(Transaction.Type.Sale, transaction.type)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2010", transaction.credit_card_details.expiration_date)

    def test_transaction_credit_from_transparent_redirect_with_successful_result(self):
        tr_data = {
            "transaction": {
                "amount": "1000.00",
            }
        }
        post_params = {
            "tr_data": Transaction.tr_data_for_credit(tr_data, "http://example.com/path"),
            "transaction[credit_card][number]": "4111111111111111",
            "transaction[credit_card][expiration_date]": "05/2010",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params)
        result = TransparentRedirect.confirm(query_string)
        self.assertTrue(result.is_success)

        transaction = result.transaction
        self.assertEquals(Decimal("1000.00"), transaction.amount)
        self.assertEquals(Transaction.Type.Credit, transaction.type)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2010", transaction.credit_card_details.expiration_date)

    def test_customer_create_from_transparent_redirect(self):
        tr_data = {
            "customer": {
                "first_name": "John",
                "last_name": "Doe",
                "company": "Doe Co",
            }
        }
        post_params = {
            "tr_data": Customer.tr_data_for_create(tr_data, "http://example.com/path"),
            "customer[email]": "john@doe.com",
            "customer[phone]": "312.555.2323",
            "customer[fax]": "614.555.5656",
            "customer[website]": "www.johndoe.com"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params)
        result = TransparentRedirect.confirm(query_string)
        self.assertTrue(result.is_success)
        customer = result.customer
        self.assertEquals("John", customer.first_name)
        self.assertEquals("Doe", customer.last_name)
        self.assertEquals("Doe Co", customer.company)
        self.assertEquals("john@doe.com", customer.email)
        self.assertEquals("312.555.2323", customer.phone)
        self.assertEquals("614.555.5656", customer.fax)
        self.assertEquals("www.johndoe.com", customer.website)

    def test_customer_update_from_transparent_redirect(self):
        customer = Customer.create({"first_name": "Sarah", "last_name": "Humphrey"}).customer

        tr_data = {
            "customer_id": customer.id,
            "customer": {
                "first_name": "Stan",
            }
        }
        post_params = {
            "tr_data": Customer.tr_data_for_update(tr_data, "http://example.com/path"),
            "customer[last_name]": "Humphrey",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params)
        result = TransparentRedirect.confirm(query_string)
        self.assertTrue(result.is_success)

        customer = Customer.find(customer.id)
        self.assertEquals("Stan", customer.first_name)
        self.assertEquals("Humphrey", customer.last_name)
