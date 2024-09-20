from tests.test_helper import *
from braintree.configuration import Configuration

class TestTransactionGateway(unittest.TestCase):

    def setUp(self):
        config = Configuration(
            environment=Environment.Development,
            merchant_id="integration_merchant_id",
            public_key="integration_public_key",
            private_key="integration_private_key"
        )
        self.gateway = BraintreeGateway(config)

    def test_credit_with_a_successful_result(self):
        result = self.gateway.transaction.credit({
            "amount": Decimal(TransactionAmounts.Authorize),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search(r"\A\w{6,}\Z", transaction.id))
        self.assertEqual(Transaction.Type.Credit, transaction.type)
        self.assertEqual(Decimal(TransactionAmounts.Authorize), transaction.amount)
        cc_details = transaction.credit_card_details
        self.assertEqual("411111", cc_details.bin)
        self.assertEqual("1111", cc_details.last_4)
        self.assertEqual("05/2009", cc_details.expiration_date)

    def test_shared_vault_transaction_with_nonce(self):
        config = Configuration(
            merchant_id="integration_merchant_public_id",
            public_key="oauth_app_partner_user_public_key",
            private_key="oauth_app_partner_user_private_key",
            environment=Environment.Development
        )

        gateway = BraintreeGateway(config)
        customer = gateway.customer.create({"first_name": "Bob"}).customer
        address = gateway.address.create({
            "customer_id": customer.id,
            "first_name": "Joe",
        }).address

        credit_card = gateway.credit_card.create(
            params={
                "customer_id": customer.id,
                "number": "4111111111111111",
                "expiration_date": "05/2009",
            }
        ).credit_card

        shared_nonce = gateway.payment_method_nonce.create(
            credit_card.token
        ).payment_method_nonce.nonce

        oauth_app_gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret",
            environment=Environment.Development
        )
        code = TestHelper.create_grant(oauth_app_gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "grant_payment_method,shared_vault_transactions"
        })
        access_token = oauth_app_gateway.oauth.create_token_from_code({
            "code": code
        }).credentials.access_token

        recipient_gateway = BraintreeGateway(access_token=access_token)

        result = recipient_gateway.transaction.sale({
            "shared_payment_method_nonce": shared_nonce,
            "shared_customer_id": customer.id,
            "shared_shipping_address_id": address.id,
            "shared_billing_address_id": address.id,
            "amount": "100"
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.shipping_details.first_name, address.first_name)
        self.assertEqual(result.transaction.billing_details.first_name, address.first_name)
        self.assertEqual(result.transaction.customer_details.first_name, customer.first_name)

    def test_shared_vault_transaction_with_token(self):
        config = Configuration(
            merchant_id="integration_merchant_public_id",
            public_key="oauth_app_partner_user_public_key",
            private_key="oauth_app_partner_user_private_key",
            environment=Environment.Development
        )

        gateway = BraintreeGateway(config)
        customer = gateway.customer.create({"first_name": "Bob"}).customer
        address = gateway.address.create({
            "customer_id": customer.id,
            "first_name": "Joe",
        }).address

        credit_card = gateway.credit_card.create(
            params={
                "customer_id": customer.id,
                "number": "4111111111111111",
                "expiration_date": "05/2009",
            }
        ).credit_card

        oauth_app_gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret",
            environment=Environment.Development
        )
        code = TestHelper.create_grant(oauth_app_gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "grant_payment_method,shared_vault_transactions"
        })
        access_token = oauth_app_gateway.oauth.create_token_from_code({
            "code": code
        }).credentials.access_token

        recipient_gateway = BraintreeGateway(
            access_token=access_token,
        )

        result = recipient_gateway.transaction.sale({
            "shared_payment_method_token": credit_card.token,
            "shared_customer_id": customer.id,
            "shared_shipping_address_id": address.id,
            "shared_billing_address_id": address.id,
            "amount": "100"
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.shipping_details.first_name, address.first_name)
        self.assertEqual(result.transaction.billing_details.first_name, address.first_name)
        self.assertEqual(result.transaction.customer_details.first_name, customer.first_name)

    def test_sale_with_gateway_rejected_with_incomplete_application(self):
        gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret",
            environment=Environment.Development
        )

        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "GBR",
            "payment_methods": ["credit_card", "paypal"]
        })

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
            environment=Environment.Development
        )

        result = gateway.transaction.sale({
            "amount": "4000.00",
            "billing": {
                "street_address": "200 Fake Street"
            },
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertFalse(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.GatewayRejectionReason.ApplicationIncomplete, transaction.gateway_rejection_reason)

    def test_sale_with_apple_pay_params(self):
        result = self.gateway.transaction.sale({
            "amount": Decimal(TransactionAmounts.Authorize),
            "apple_pay_card": {
                "cardholder_name": "Evelyn Boyd Granville",
                "cryptogram": "AAAAAAAA/COBt84dnIEcwAA3gAAGhgEDoLABAAhAgAABAAAALnNCLw==",
                "eci_indicator": "07",
                "expiration_month": "10",
                "expiration_year": "14",
                "number": "370295001292109"
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(Transaction.Status.Authorized, result.transaction.status)

    def test_sale_with_google_pay_params(self):
        result = self.gateway.transaction.sale({
            "amount": Decimal(TransactionAmounts.Authorize),
            "android_pay_card": {
                "cryptogram": "AAAAAAAA/COBt84dnIEcwAA3gAAGhgEDoLABAAhAgAABAAAALnNCLw==",
                "eci_indicator": "07",
                "expiration_month": "10",
                "expiration_year": "14",
                "google_transaction_id": "12345",
                "number": "4012888888881881",
                "source_card_last_four": "1881",
                "source_card_type": "Visa"
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(Transaction.Status.Authorized, result.transaction.status)
        self.assertEqual("android_pay_card", result.transaction.payment_instrument_type)
        self.assertEqual("10", result.transaction.android_pay_card_details.expiration_month)
        self.assertEqual("14", result.transaction.android_pay_card_details.expiration_year)
        self.assertEqual("12345", result.transaction.android_pay_card_details.google_transaction_id)
        self.assertEqual("1881", result.transaction.android_pay_card_details.source_card_last_4)
        self.assertEqual("Visa", result.transaction.android_pay_card_details.source_card_type)

    def test_create_can_set_recurring_flag(self):
        result = self.gateway.transaction.sale({
            "amount": "100",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
                },
            "recurring": True
            })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(True, transaction.recurring)

    def test_create_recurring_flag_sends_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = self.gateway.transaction.sale({
                "amount": "100",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "05/2009"
                },
                "recurring": True
            })

            self.assertTrue(result.is_success)
            transaction = result.transaction
            self.assertEqual(True, transaction.recurring)
            assert len(w) > 0
            assert issubclass(w[-1].category, DeprecationWarning)
            assert "Use transaction_source parameter instead" in str(w[-1].message)
