from tests.test_helper import *

class TestTransactionSearch(unittest.TestCase):
    def test_advanced_search_no_results(self):
        collection = Transaction.search([
            TransactionSearch.billing_first_name == "no_such_person"
        ])
        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_searches_all_text_fields_at_once(self):
        first_name = "Tim%s" % randint(1, 100000)
        token = "creditcard%s" % randint(1, 100000)
        customer_id = "customer%s" % randint(1, 100000)

        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Tom Smith",
                "token": token,
            },
            "billing": {
                "company": "Braintree",
                "country_name": "United States of America",
                "extended_address": "Suite 123",
                "first_name": first_name,
                "last_name": "Smith",
                "locality": "Chicago",
                "postal_code": "12345",
                "region": "IL",
                "street_address": "123 Main St"
            },
            "customer": {
                "company": "Braintree",
                "email": "smith@example.com",
                "fax": "5551231234",
                "first_name": "Tom",
                "id": customer_id,
                "last_name": "Smith",
                "phone": "5551231234",
                "website": "http://example.com",
            },
            "options": {
                "store_in_vault": True,
                "submit_for_settlement": True
            },
            "order_id": "myorder",
            "shipping": {
                "company": "Braintree P.S.",
                "country_name": "Mexico",
                "extended_address": "Apt 456",
                "first_name": "Thomas",
                "last_name": "Smithy",
                "locality": "Braintree",
                "postal_code": "54321",
                "region": "MA",
                "street_address": "456 Road"
            }
        }).transaction

        TestHelper.settle_transaction(transaction.id)
        transaction = Transaction.find(transaction.id)

        collection = Transaction.search([
            TransactionSearch.billing_company == "Braintree",
            TransactionSearch.billing_country_name == "United States of America",
            TransactionSearch.billing_extended_address == "Suite 123",
            TransactionSearch.billing_first_name == first_name,
            TransactionSearch.billing_last_name == "Smith",
            TransactionSearch.billing_locality == "Chicago",
            TransactionSearch.billing_postal_code == "12345",
            TransactionSearch.billing_region == "IL",
            TransactionSearch.billing_street_address == "123 Main St",
            TransactionSearch.credit_card_cardholder_name == "Tom Smith",
            TransactionSearch.credit_card_expiration_date == "05/2012",
            TransactionSearch.credit_card_number == "4111111111111111",
            TransactionSearch.customer_company == "Braintree",
            TransactionSearch.customer_email == "smith@example.com",
            TransactionSearch.customer_fax == "5551231234",
            TransactionSearch.customer_first_name == "Tom",
            TransactionSearch.customer_id == customer_id,
            TransactionSearch.customer_last_name == "Smith",
            TransactionSearch.customer_phone == "5551231234",
            TransactionSearch.customer_website == "http://example.com",
            TransactionSearch.order_id == "myorder",
            TransactionSearch.payment_method_token == token,
            TransactionSearch.processor_authorization_code == transaction.processor_authorization_code,
            TransactionSearch.settlement_batch_id == transaction.settlement_batch_id,
            TransactionSearch.shipping_company == "Braintree P.S.",
            TransactionSearch.shipping_country_name == "Mexico",
            TransactionSearch.shipping_extended_address == "Apt 456",
            TransactionSearch.shipping_first_name == "Thomas",
            TransactionSearch.shipping_last_name == "Smithy",
            TransactionSearch.shipping_locality == "Braintree",
            TransactionSearch.shipping_postal_code == "54321",
            TransactionSearch.shipping_region == "MA",
            TransactionSearch.shipping_street_address == "456 Road",
            TransactionSearch.id == transaction.id
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

    def test_advanced_search_search_each_text_field(self):
        first_name = "Tim%s" % randint(1, 100000)
        token = "creditcard%s" % randint(1, 100000)
        customer_id = "customer%s" % randint(1, 100000)

        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Tom Smith",
                "token": token,
            },
            "billing": {
                "company": "Braintree",
                "country_name": "United States of America",
                "extended_address": "Suite 123",
                "first_name": first_name,
                "last_name": "Smith",
                "locality": "Chicago",
                "postal_code": "12345",
                "region": "IL",
                "street_address": "123 Main St"
            },
            "customer": {
                "company": "Braintree",
                "email": "smith@example.com",
                "fax": "5551231234",
                "first_name": "Tom",
                "id": customer_id,
                "last_name": "Smith",
                "phone": "5551231234",
                "website": "http://example.com",
            },
            "options": {
                "store_in_vault": True
            },
            "order_id": "myorder",
            "shipping": {
                "company": "Braintree P.S.",
                "country_name": "Mexico",
                "extended_address": "Apt 456",
                "first_name": "Thomas",
                "last_name": "Smithy",
                "locality": "Braintree",
                "postal_code": "54321",
                "region": "MA",
                "street_address": "456 Road"
            }
        }).transaction

        search_criteria = {
            "billing_company": "Braintree",
            "billing_country_name": "United States of America",
            "billing_extended_address": "Suite 123",
            "billing_first_name": first_name,
            "billing_last_name": "Smith",
            "billing_locality": "Chicago",
            "billing_postal_code": "12345",
            "billing_region": "IL",
            "billing_street_address": "123 Main St",
            "credit_card_cardholder_name": "Tom Smith",
            "credit_card_expiration_date": "05/2012",
            "credit_card_number": "4111111111111111",
            "customer_company": "Braintree",
            "customer_email": "smith@example.com",
            "customer_fax": "5551231234",
            "customer_first_name": "Tom",
            "customer_id": customer_id,
            "customer_last_name": "Smith",
            "customer_phone": "5551231234",
            "customer_website": "http://example.com",
            "order_id": "myorder",
            "payment_method_token": token,
            "processor_authorization_code": transaction.processor_authorization_code,
            "shipping_company": "Braintree P.S.",
            "shipping_country_name": "Mexico",
            "shipping_extended_address": "Apt 456",
            "shipping_first_name": "Thomas",
            "shipping_last_name": "Smithy",
            "shipping_locality": "Braintree",
            "shipping_postal_code": "54321",
            "shipping_region": "MA",
            "shipping_street_address": "456 Road",
            "user": "integration_user_public_id",
            "credit_card_unique_identifier": transaction.credit_card["unique_number_identifier"]
        }

        for criterion, value in search_criteria.items():
            text_node = getattr(TransactionSearch, criterion)

            collection = Transaction.search([
                TransactionSearch.id == transaction.id,
                text_node == value
            ])
            self.assertEquals(1, collection.maximum_size)
            self.assertEquals(transaction.id, collection.first.id)

            collection = Transaction.search([
                TransactionSearch.id == transaction.id,
                text_node == "invalid"
            ])
            self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_with_argument_list_rather_than_literal_list(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Tom Smith",
            },
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name == "Tom Smith"
        )

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

    def test_advanced_search_with_payment_instrument_type_is_credit_card(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Tom Smith",
            },
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == "CreditCardDetail" 
        )

        self.assertEquals(transaction.payment_instrument_type, PaymentInstrumentType.CreditCard)
        self.assertEquals(transaction.id, collection.first.id)
    
    def test_advanced_search_with_payment_instrument_type_is_paypal(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == "PayPalDetail" 
        )

        self.assertEquals(transaction.payment_instrument_type, PaymentInstrumentType.PayPalAccount)
        self.assertEquals(transaction.id, collection.first.id)
    
    def test_advanced_search_with_payment_instrument_type_is_apple_pay(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.ApplePayVisa
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == "ApplePayDetail" 
        )

        self.assertEquals(transaction.payment_instrument_type, PaymentInstrumentType.ApplePayCard)
        self.assertEquals(transaction.id, collection.first.id)
    
    def test_advanced_search_with_payment_instrument_type_is_europe(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "altpay_merchant"
            Configuration.public_key = "altpay_merchant_public_key"
            Configuration.private_key = "altpay_merchant_private_key"
            customer_id = Customer.create().customer.id
            token = TestHelper.generate_decoded_client_token({"customer_id": customer_id, "sepa_mandate_type": EuropeBankAccount.MandateType.Business})
            authorization_fingerprint = json.loads(token)["authorizationFingerprint"]
            config = Configuration.instantiate()
            client_api =  ClientApiHttp(config, {
                "authorization_fingerprint": authorization_fingerprint,
                "shared_customer_identifier": "fake_identifier",
                "shared_customer_identifier_type": "testing"
            })

            nonce = client_api.get_europe_bank_account_nonce({
                "locale": "de-DE",
                "bic": "DEUTDEFF",
                "iban": "DE89370400440532013000",
                "accountHolderName": "Baron Von Holder",
                "billingAddress": {"region": "Hesse", "country_name": "Germany"}
            })

            transaction = Transaction.sale({
                "merchant_account_id": "fake_sepa_ma",
                "amount": "10.00",
                "payment_method_nonce": nonce
            }).transaction

            collection = Transaction.search(
                TransactionSearch.id == transaction.id,
                TransactionSearch.payment_instrument_type == "EuropeBankAccountDetail" 
            )

            self.assertEquals(transaction.payment_instrument_type, PaymentInstrumentType.EuropeBankAccount)
            self.assertEquals(transaction.id, collection.first.id)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_advanced_search_text_node_contains(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Jane Shea"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name.contains("ane She")
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name.contains("invalid")
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_text_node_starts_with(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Jane Shea"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name.starts_with("Jane S")
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name.starts_with("invalid")
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_text_node_ends_with(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Jane Shea"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name.ends_with("e Shea")
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name.ends_with("invalid")
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_text_node_is_not(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": "Jane Shea"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name != "invalid"
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name != "Jane Shea"
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_multiple_value_node_created_using(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_using == Transaction.CreatedUsing.FullInformation
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_using.in_list([Transaction.CreatedUsing.FullInformation, Transaction.CreatedUsing.Token])
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_using == Transaction.CreatedUsing.Token
        ])

        self.assertEquals(0, collection.maximum_size)

    @raises_with_regexp(AttributeError, "Invalid argument\(s\) for created_using: noSuchCreatedUsing")
    def test_advanced_search_multiple_value_node_allowed_values_created_using(self):
        collection = Transaction.search([TransactionSearch.created_using == "noSuchCreatedUsing"])

    def test_advanced_search_multiple_value_node_credit_card_customer_location(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_customer_location == CreditCard.CustomerLocation.US
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_customer_location.in_list([CreditCard.CustomerLocation.US, CreditCard.CustomerLocation.International])
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_customer_location == CreditCard.CustomerLocation.International
        ])

        self.assertEquals(0, collection.maximum_size)

    @raises_with_regexp(AttributeError,
            "Invalid argument\(s\) for credit_card_customer_location: noSuchCreditCardCustomerLocation")
    def test_advanced_search_multiple_value_node_allowed_values_credit_card_customer_location(self):
        collection = Transaction.search([
            TransactionSearch.credit_card_customer_location == "noSuchCreditCardCustomerLocation"
        ])

    def test_advanced_search_multiple_value_node_merchant_account_id(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.merchant_account_id == transaction.merchant_account_id
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.merchant_account_id.in_list([transaction.merchant_account_id, "bogus_merchant_account_id"])
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.merchant_account_id == "bogus_merchant_account_id"
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_multiple_value_node_credit_card_card_type(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_card_type == transaction.credit_card_details.card_type
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_card_type.in_list([transaction.credit_card_details.card_type, CreditCard.CardType.AmEx])
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_card_type == CreditCard.CardType.AmEx
        ])

        self.assertEquals(0, collection.maximum_size)

    @raises_with_regexp(AttributeError,
            "Invalid argument\(s\) for credit_card_card_type: noSuchCreditCardCardType")
    def test_advanced_search_multiple_value_node_allowed_values_credit_card_card_type(self):
        collection = Transaction.search([
            TransactionSearch.credit_card_card_type == "noSuchCreditCardCardType"
        ])

    def test_advanced_search_multiple_value_node_status(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.status == Transaction.Status.Authorized
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.status.in_list([Transaction.Status.Authorized, Transaction.Status.Settled])
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.status == Transaction.Status.Settled
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_authorization_expired_status(self):
        collection = Transaction.search(
            TransactionSearch.status == Transaction.Status.AuthorizationExpired
        )

        self.assertTrue(collection.maximum_size > 0)
        self.assertEqual(Transaction.Status.AuthorizationExpired, collection.first.status)

    def test_advanced_search_allows_new_settlement_statuses(self):
        collection = Transaction.search([
            TransactionSearch.status.in_list(["settlement_confirmed", "settlement_declined"])
        ])
        print(collection)

    @raises_with_regexp(AttributeError, "Invalid argument\(s\) for status: noSuchStatus")
    def test_advanced_search_multiple_value_node_allowed_values_status(self):
        collection = Transaction.search([ TransactionSearch.status == "noSuchStatus" ])

    def test_advanced_search_multiple_value_node_source(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.source == Transaction.Source.Api
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.source.in_list([Transaction.Source.Api, Transaction.Source.ControlPanel])
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.source == Transaction.Source.ControlPanel
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_multiple_value_node_type(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.type == Transaction.Type.Sale
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.type.in_list([Transaction.Type.Sale, Transaction.Type.Credit])
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.type == Transaction.Type.Credit
        ])

        self.assertEquals(0, collection.maximum_size)

    @raises_with_regexp(AttributeError, "Invalid argument\(s\) for type: noSuchType")
    def test_advanced_search_multiple_value_node_allowed_values_type(self):
        collection = Transaction.search([
            TransactionSearch.type == "noSuchType"
        ])

    def test_advanced_search_multiple_value_node_type_with_refund(self):
        name = "Anabel Atkins%s" % randint(1,100000)
        sale = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            },
            'options': {
                'submit_for_settlement': True
            }
        }).transaction
        TestHelper.settle_transaction(sale.id)

        refund = Transaction.refund(sale.id).transaction

        credit = Transaction.credit({
            "amount": Decimal(TransactionAmounts.Authorize),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009",
                "cardholder_name": name
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.type == Transaction.Type.Credit
        ])

        self.assertEquals(2, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.type == Transaction.Type.Credit,
            TransactionSearch.refund == True
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(refund.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.type == Transaction.Type.Credit,
            TransactionSearch.refund == False
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(credit.id, collection.first.id)

    def test_advanced_search_range_node_amount(self):
        name = "Henrietta Livingston%s" % randint(1,100000)
        t_1000 = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        t_1500 = Transaction.sale({
            "amount": "1500.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        t_1800 = Transaction.sale({
            "amount": "1800.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "cardholder_name": name
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount >= "1700"
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(t_1800.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount <= "1250"
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(t_1000.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount.between("1100", "1600")
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(t_1500.id, collection.first.id)

    def test_advanced_search_range_node_created_at_less_than_or_equal_to(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             }
         }).transaction

        past = transaction.created_at - timedelta(minutes=10)
        now = transaction.created_at
        future = transaction.created_at + timedelta(minutes=10)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at <= past
        ])

        self.assertEquals(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at <= now
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at <= future
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

    def test_advanced_search_range_node_created_at_greater_than_or_equal_to(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             }
         }).transaction

        past = transaction.created_at - timedelta(minutes=10)
        now = transaction.created_at
        future = transaction.created_at + timedelta(minutes=10)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at >= past
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at >= now
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at >= future
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_created_at_between(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             }
         }).transaction

        past = transaction.created_at - timedelta(minutes=10)
        now = transaction.created_at
        future = transaction.created_at + timedelta(minutes=10)
        future2 = transaction.created_at + timedelta(minutes=20)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at.between(past, now)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at.between(now, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_created_at_is(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             }
         }).transaction

        past = transaction.created_at - timedelta(minutes=10)
        now = transaction.created_at
        future = transaction.created_at + timedelta(minutes=10)
        future2 = transaction.created_at + timedelta(minutes=20)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at == past
        ])

        self.assertEquals(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at == now
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at == future
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_created_with_dates(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             }
         }).transaction

        past = datetime.today() - timedelta(days=1)
        future = datetime.today() + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

    def test_advanced_search_range_node_disbursement_date_less_than_or_equal_to(self):
        transaction_id = "deposittransaction"
        disbursement_time = datetime(2013, 4, 10, 0, 0, 0)
        past = disbursement_time - timedelta(minutes=10)
        future = disbursement_time + timedelta(minutes=10)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date <= past
        ])

        self.assertEquals(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date <= disbursement_time
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date <= future
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

    def test_advanced_search_range_node_disbursement_date_greater_than_or_equal_to(self):
        transaction_id = "deposittransaction"
        disbursement_time = datetime(2013, 4, 10, 0, 0, 0)
        past = disbursement_time - timedelta(minutes=10)
        future = disbursement_time + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date >= past
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date >= disbursement_time
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date >= future
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_disbursement_date_between(self):
        transaction_id = "deposittransaction"
        disbursement_time = datetime(2013, 4, 10, 0, 0, 0)
        past = disbursement_time - timedelta(days=1)
        future = disbursement_time + timedelta(days=1)
        future2 = disbursement_time + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date.between(past, disbursement_time)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date.between(disbursement_time, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_disbursement_date_is(self):
        transaction_id = "deposittransaction"
        disbursement_time = datetime(2013, 4, 10, 0, 0, 0)
        past = disbursement_time - timedelta(days=10)
        now = disbursement_time
        future = disbursement_time + timedelta(days=10)
        future2 = disbursement_time + timedelta(days=20)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date == past
        ])

        self.assertEquals(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date == now
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date == future
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_disbursement_date_with_dates(self):
        transaction_id = "deposittransaction"
        disbursement_date = date(2013, 4, 10)
        past = disbursement_date - timedelta(days=1)
        future = disbursement_date + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

    def test_advanced_search_range_node_disputed_date_less_than_or_equal_to(self):
        transaction_id = "disputedtransaction"
        disputed_time = datetime(2014, 3, 1, 0, 0, 0)
        past = disputed_time - timedelta(minutes=10)
        future = disputed_time + timedelta(minutes=10)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date <= past
        ])

        self.assertEquals(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date <= disputed_time
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date <= future
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

    def test_advanced_search_range_node_disputed_date_greater_than_or_equal_to(self):
        transaction_id = "2disputetransaction"
        disputed_time = datetime(2014, 3, 1, 0, 0, 0)
        past = disputed_time - timedelta(minutes=10)
        future = disputed_time + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date >= past
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date >= disputed_time
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date >= future
        ])

        self.assertEquals(1, collection.maximum_size)

    def test_advanced_search_range_node_disputed_date_between(self):
        transaction_id = "disputedtransaction"
        disputed_time = datetime(2014, 3, 1, 0, 0, 0)
        past = disputed_time - timedelta(days=1)
        future = disputed_time + timedelta(days=1)
        future2 = disputed_time + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date.between(past, disputed_time)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date.between(disputed_time, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_disputed_date_is(self):
        transaction_id = "disputedtransaction"
        disputed_time = datetime(2014, 3, 1, 0, 0, 0)
        past = disputed_time - timedelta(days=10)
        now = disputed_time
        future = disputed_time + timedelta(days=10)
        future2 = disputed_time + timedelta(days=20)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date == past
        ])

        self.assertEquals(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date == now
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date == future
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_disputed_date_with_dates(self):
        transaction_id = "disputedtransaction"
        disputed_date = date(2014, 3, 1)
        past = disputed_date - timedelta(days=1)
        future = disputed_date + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.dispute_date.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction_id, collection.first.id)

    def test_advanced_search_range_node_authorization_expired_at(self):
        two_days_ago = datetime.today() - timedelta(days=2)
        yesterday = datetime.today() - timedelta(days=1)
        tomorrow = datetime.today() + timedelta(days=1)

        collection = Transaction.search(
            TransactionSearch.authorization_expired_at.between(two_days_ago, yesterday)
        )
        self.assertEquals(0, collection.maximum_size)

        collection = Transaction.search(
            TransactionSearch.authorization_expired_at.between(yesterday, tomorrow)
        )
        self.assertTrue(collection.maximum_size > 0)
        self.assertEquals(Transaction.Status.AuthorizationExpired, collection.first.status)


    def test_advanced_search_range_node_authorized_at(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             }
        }).transaction

        past = datetime.today() - timedelta(days=1)
        future = datetime.today() + timedelta(days=1)
        future2 = datetime.today() + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.authorized_at.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.authorized_at.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_failed_at(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Fail,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             }
        }).transaction

        past = datetime.today() - timedelta(days=1)
        future = datetime.today() + timedelta(days=1)
        future2 = datetime.today() + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.failed_at.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.failed_at.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_gateway_rejected_at(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "processing_rules_merchant_id"
            Configuration.public_key = "processing_rules_public_key"
            Configuration.private_key = "processing_rules_private_key"

            transaction  = Transaction.sale({
                 "amount": TransactionAmounts.Authorize,
                 "credit_card": {
                     "number": "4111111111111111",
                     "expiration_date": "05/2012",
                     "cvv": "200"
                 }
            }).transaction

            past = datetime.today() - timedelta(days=1)
            future = datetime.today() + timedelta(days=1)
            future2 = datetime.today() + timedelta(days=2)

            collection = Transaction.search([
                TransactionSearch.id == transaction.id,
                TransactionSearch.gateway_rejected_at.between(past, future)
            ])

            self.assertEquals(1, collection.maximum_size)
            self.assertEquals(transaction.id, collection.first.id)

            collection = Transaction.search([
                TransactionSearch.id == transaction.id,
                TransactionSearch.gateway_rejected_at.between(future, future2)
            ])

            self.assertEquals(0, collection.maximum_size)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_advanced_search_range_node_processor_declined_at(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Decline,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             }
        }).transaction

        past = datetime.today() - timedelta(days=1)
        future = datetime.today() + timedelta(days=1)
        future2 = datetime.today() + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.processor_declined_at.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.processor_declined_at.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_settled_at(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             },
             "options": {
                 "submit_for_settlement": True
             }
        }).transaction

        TestHelper.settle_transaction(transaction.id)
        transaction = Transaction.find(transaction.id)

        past = datetime.today() - timedelta(days=1)
        future = datetime.today() + timedelta(days=1)
        future2 = datetime.today() + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.settled_at.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.settled_at.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_submitted_for_settlement_at(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             },
             "options": {
                 "submit_for_settlement": True
             }
        }).transaction

        past = datetime.today() - timedelta(days=1)
        future = datetime.today() + timedelta(days=1)
        future2 = datetime.today() + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.submitted_for_settlement_at.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.submitted_for_settlement_at.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_voided_at(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             }
        }).transaction
        transaction = Transaction.void(transaction.id).transaction

        past = datetime.today() - timedelta(days=1)
        future = datetime.today() + timedelta(days=1)
        future2 = datetime.today() + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.voided_at.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.voided_at.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_range_node_can_search_on_multiple_statuses(self):
        transaction  = Transaction.sale({
             "amount": TransactionAmounts.Authorize,
             "credit_card": {
                 "number": "4111111111111111",
                 "expiration_date": "05/2012"
             },
             "options": {
                 "submit_for_settlement": True
             }
        }).transaction

        past = datetime.today() - timedelta(days=1)
        future = datetime.today() + timedelta(days=1)
        future2 = datetime.today() + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.authorized_at.between(past, future),
            TransactionSearch.submitted_for_settlement_at.between(past, future)
        ])

        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.authorized_at.between(future, future2),
            TransactionSearch.submitted_for_settlement_at.between(future, future2)
        ])

        self.assertEquals(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.authorized_at.between(past, future),
            TransactionSearch.voided_at.between(past, future)
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_advanced_search_returns_iteratable_results(self):
        collection = Transaction.search([
            TransactionSearch.credit_card_number.starts_with("411")
        ])

        self.assertTrue(collection.maximum_size > 100)

        transaction_ids = [transaction.id for transaction in collection.items]
        self.assertEquals(collection.maximum_size, len(TestHelper.unique(transaction_ids)))

    def test_advanced_search_can_search_on_paypal_fields(self):
        http = ClientApiHttp.create()
        status_code, nonce = http.get_paypal_nonce({
            "access_token": "PAYPAL-ACCESS-TOKEN",
            "options": {"validate": False}
        })
        self.assertEquals(status_code, 202)

        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": nonce
        }).transaction

        collection = Transaction.search([
            TransactionSearch.paypal_payer_email == transaction.paypal_details.payer_email,
            TransactionSearch.paypal_authorization_id == transaction.paypal_details.authorization_id,
            TransactionSearch.paypal_payment_id == transaction.paypal_details.payment_id,
        ])
        self.assertEquals(1, collection.maximum_size)
        self.assertEquals(transaction.id, collection.first.id)

    def test_advanced_search_can_search_on_sepa_iban(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "altpay_merchant"
            Configuration.public_key = "altpay_merchant_public_key"
            Configuration.private_key = "altpay_merchant_private_key"
            customer_id = Customer.create().customer.id
            token = TestHelper.generate_decoded_client_token({"customer_id": customer_id, "sepa_mandate_type": EuropeBankAccount.MandateType.Business})
            authorization_fingerprint = json.loads(token)["authorizationFingerprint"]
            config = Configuration.instantiate()
            client_api =  ClientApiHttp(config, {
                "authorization_fingerprint": authorization_fingerprint,
                "shared_customer_identifier": "fake_identifier",
                "shared_customer_identifier_type": "testing"
            })
            nonce = client_api.get_europe_bank_account_nonce({
                "locale": "de-DE",
                "bic": "DEUTDEFF",
                "iban": "DE89370400440532013000",
                "accountHolderName": "Baron Von Holder",
                "billingAddress": {"region": "Hesse", "country_name": "Germany"}
            })

            result = Transaction.sale({
                "merchant_account_id": "fake_sepa_ma",
                "amount": "10.00",
                "payment_method_nonce": nonce
            })

            collection = Transaction.search([
                TransactionSearch.europe_bank_account_iban == "DE89370400440532013000"
            ])
            self.assertTrue(collection.maximum_size >= 1)
            ids = [transaction.id for transaction in collection.items]
            self.assertIn(result.transaction.id, ids)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key


    @raises(DownForMaintenanceError)
    def test_search_handles_a_search_timeout(self):
        Transaction.search([
            TransactionSearch.amount.between("-1100", "1600")
        ])

