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
