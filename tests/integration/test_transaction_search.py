from unittest.mock import patch
from tests.test_helper import *

class TestTransactionSearch(unittest.TestCase):
    def test_advanced_search_no_results(self):
        collection = Transaction.search([
            TransactionSearch.billing_first_name == "no_such_person"
        ])
        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_searches_all_text_fields_at_once(self):
        first_name = "Tim%s" % random.randint(1, 100000)
        token = "creditcard%s" % random.randint(1, 100000)
        customer_id = "customer%s" % random.randint(1, 100000)

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_search_each_text_field(self):
        first_name = "Tim%s" % random.randint(1, 100000)
        token = "creditcard%s" % random.randint(1, 100000)
        customer_id = "customer%s" % random.randint(1, 100000)

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
            self.assertEqual(1, collection.maximum_size)
            self.assertEqual(transaction.id, collection.first.id)

            collection = Transaction.search([
                TransactionSearch.id == transaction.id,
                text_node == "invalid"
            ])
            self.assertEqual(0, collection.maximum_size)

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

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

        self.assertEqual(transaction.payment_instrument_type, PaymentInstrumentType.CreditCard)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_with_payment_instrument_type_is_paypal(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == "PayPalDetail"
        )

        self.assertEqual(transaction.payment_instrument_type, PaymentInstrumentType.PayPalAccount)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_with_payment_instrument_type_is_local_payment(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "options": {
                "submit_for_settlement": True,
            },
            "payment_method_nonce": Nonces.LocalPayment
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == "LocalPaymentDetail"
        )

        self.assertEqual(transaction.payment_instrument_type, PaymentInstrumentType.LocalPayment)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_with_payment_instrument_type_is_sepa_debit_account(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "options": {
                "submit_for_settlement": True,
            },
            "payment_method_nonce": Nonces.SepaDirectDebit
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == "SEPADebitAccount"
        )

        self.assertEqual(transaction.payment_instrument_type, PaymentInstrumentType.SepaDirectDebitAccount)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_with_sepa_debit_paypal_v2_order_id(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "options": {
                "submit_for_settlement": True,
            },
            "payment_method_nonce": Nonces.SepaDirectDebit
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.sepa_debit_paypal_v2_order_id == transaction.sepa_direct_debit_account_details.paypal_v2_order_id
        )

        self.assertEqual(transaction.payment_instrument_type, PaymentInstrumentType.SepaDirectDebitAccount)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_with_payment_instrument_type_is_meta_checkout(self):
        card_tx = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "options": {
                "submit_for_settlement": True,
            },
            "payment_method_nonce": Nonces.MetaCheckoutCard
        }).transaction

        token_tx = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "options": {
                "submit_for_settlement": True,
            },
            "payment_method_nonce": Nonces.MetaCheckoutToken
        }).transaction

        collection = Transaction.search(
            TransactionSearch.payment_instrument_type == "MetaCheckout"
        )

        self.assertTrue(collection.maximum_size >= 2)

        tx_id_map = list(map(lambda x: x.id, collection))
        self.assertTrue(card_tx.id in tx_id_map)
        self.assertTrue(token_tx.id in tx_id_map)

    def test_advanced_search_with_payment_instrument_type_is_apple_pay(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.ApplePayVisa
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == "ApplePayDetail"
        )

        self.assertEqual(transaction.payment_instrument_type, PaymentInstrumentType.ApplePayCard)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_with_debit_network(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.pinless_debit_merchant_account_id,
            #"currency_iso_code": "USD",
            "payment_method_nonce": Nonces.TransactablePinlessDebitVisa,
            "options": {
                "submit_for_settlement": True
            }
        }).transaction

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_card_type == transaction.credit_card_details.card_type
        )

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search(
            TransactionSearch.id == transaction.id,
            TransactionSearch.debit_network.in_list(Constants.get_all_enum_values(CreditCard.DebitNetwork))
        )

        self.assertEqual(1, collection.maximum_size)

    def test_advanced_search_multiple_value_node_allowed_values_debit_network(self):
        with self.assertRaisesRegex(AttributeError,
                "Invalid argument\(s\) for debit_network: noSuchDebitNetwork"):
            Transaction.search([
                TransactionSearch.debit_network == "noSuchDebitNetwork"
            ])

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name.contains("invalid")
        ])

        self.assertEqual(0, collection.maximum_size)

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name.starts_with("invalid")
        ])

        self.assertEqual(0, collection.maximum_size)

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name.ends_with("invalid")
        ])

        self.assertEqual(0, collection.maximum_size)

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_cardholder_name != "Jane Shea"
        ])

        self.assertEqual(0, collection.maximum_size)

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_using.in_list([Transaction.CreatedUsing.FullInformation, Transaction.CreatedUsing.Token])
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_using == Transaction.CreatedUsing.Token
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_multiple_value_node_allowed_values_created_using(self):
        with self.assertRaisesRegex(AttributeError, "Invalid argument\(s\) for created_using: noSuchCreatedUsing"):
            Transaction.search([TransactionSearch.created_using == "noSuchCreatedUsing"])

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_customer_location.in_list([CreditCard.CustomerLocation.US, CreditCard.CustomerLocation.International])
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_customer_location == CreditCard.CustomerLocation.International
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_multiple_value_node_allowed_values_credit_card_customer_location(self):
        with self.assertRaisesRegex(AttributeError,
            "Invalid argument\(s\) for credit_card_customer_location: noSuchCreditCardCustomerLocation"):
            Transaction.search([
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.merchant_account_id.in_list([transaction.merchant_account_id, "bogus_merchant_account_id"])
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.merchant_account_id == "bogus_merchant_account_id"
        ])

        self.assertEqual(0, collection.maximum_size)

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_card_type.in_list([transaction.credit_card_details.card_type, CreditCard.CardType.AmEx])
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_card_type == CreditCard.CardType.AmEx
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_elo(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.adyen_merchant_account_id,
            "credit_card": {
                "number": CreditCardNumbers.Elo,
                "expiration_date": "10/2020",
                "cvv": "737",
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_card_type == transaction.credit_card_details.card_type
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)
        self.assertEqual(transaction.credit_card_details.card_type, collection.first.credit_card_details.card_type)

    def test_advanced_search_hiper(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.hiper_brl_merchant_account_id,
            "credit_card": {
                "number": CreditCardNumbers.Hiper,
                "expiration_date": "10/2020",
                "cvv": "737",
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_card_type == transaction.credit_card_details.card_type
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)
        self.assertEqual(transaction.credit_card_details.card_type, collection.first.credit_card_details.card_type)

    def test_advanced_search_hipercard(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.hiper_brl_merchant_account_id,
            "credit_card": {
                "number": CreditCardNumbers.Hipercard,
                "expiration_date": "10/2020",
                "cvv": "737",
            }
        }).transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.credit_card_card_type == transaction.credit_card_details.card_type
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)
        self.assertEqual(transaction.credit_card_details.card_type, collection.first.credit_card_details.card_type)

    def test_advanced_search_multiple_value_node_allowed_values_credit_card_card_type(self):
        with self.assertRaisesRegex(AttributeError,
                "Invalid argument\(s\) for credit_card_card_type: noSuchCreditCardCardType"):
            Transaction.search([
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.status.in_list([Transaction.Status.Authorized, Transaction.Status.Settled])
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.status == Transaction.Status.Settled
        ])

        self.assertEqual(0, collection.maximum_size)

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

    def test_advanced_search_settlement_confirmed_transaction(self):
        transaction_id = "settlement_confirmed_txn"

        collection = Transaction.search([
            TransactionSearch.id == transaction_id
        ])

        self.assertEqual(1, collection.maximum_size)

    def test_advanced_search_multiple_value_node_allowed_values_status(self):
        with self.assertRaisesRegex(AttributeError, "Invalid argument\(s\) for status: noSuchStatus"):
            Transaction.search([TransactionSearch.status == "noSuchStatus"])

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.source.in_list([Transaction.Source.Api, Transaction.Source.ControlPanel])
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.source == Transaction.Source.ControlPanel
        ])

        self.assertEqual(0, collection.maximum_size)

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.type.in_list([Transaction.Type.Sale, Transaction.Type.Credit])
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.type == Transaction.Type.Credit
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_multiple_value_node_allowed_values_type(self):
        with self.assertRaisesRegex(AttributeError, "Invalid argument\(s\) for type: noSuchType"):
            Transaction.search([
                TransactionSearch.type == "noSuchType"
            ])

    def test_advanced_search_multiple_value_node_type_with_refund(self):
        name = "Anabel Atkins%s" % random.randint(1, 100000)
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

        self.assertEqual(2, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.type == Transaction.Type.Credit,
            TransactionSearch.refund == True
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(refund.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.type == Transaction.Type.Credit,
            TransactionSearch.refund == False
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(credit.id, collection.first.id)

    def test_advanced_search_range_node_amount(self):
        name = "Henrietta Livingston%s" % random.randint(1, 100000)
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(t_1800.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount <= "1250"
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(t_1000.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.credit_card_cardholder_name == name,
            TransactionSearch.amount.between("1100", "1600")
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(t_1500.id, collection.first.id)

    def test_advanced_search_range_node_created_at_less_than_or_equal_to(self):
        transaction = Transaction.sale({
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

        self.assertEqual(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at <= now
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at <= future
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_range_node_created_at_greater_than_or_equal_to(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at >= now
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at >= future
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_created_at_between(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at.between(now, future)
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at.between(past, future)
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_created_at_is(self):
        transaction = Transaction.sale({
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
            TransactionSearch.created_at == past
        ])

        self.assertEqual(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at == now
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.created_at == future
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_created_with_dates(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_range_node_disbursement_date_less_than_or_equal_to(self):
        transaction_id = "deposittransaction"
        disbursement_time = datetime(2013, 4, 10, 0, 0, 0)
        past = disbursement_time - timedelta(minutes=10)
        future = disbursement_time + timedelta(minutes=10)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date <= past
        ])

        self.assertEqual(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction_id, collection.first.id)

    def test_advanced_search_range_node_disbursement_date_greater_than_or_equal_to(self):
        transaction_id = "deposittransaction"
        disbursement_time = datetime(2013, 4, 10, 0, 0, 0)
        past = disbursement_time - timedelta(minutes=10)
        future = disbursement_time + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date >= past
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date >= disbursement_time
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date >= future
        ])

        self.assertEqual(0, collection.maximum_size)

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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date.between(disbursement_time, future)
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date.between(past, future)
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_disbursement_date_is(self):
        transaction_id = "deposittransaction"
        disbursement_time = datetime(2013, 4, 10, 0, 0, 0)
        past = disbursement_time - timedelta(days=10)
        now = disbursement_time
        future = disbursement_time + timedelta(days=10)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date == past
        ])

        self.assertEqual(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date == now
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date == future
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_disbursement_date_with_dates(self):
        transaction_id = "deposittransaction"
        disbursement_date = date(2013, 4, 10)
        past = disbursement_date - timedelta(days=1)
        future = disbursement_date + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.disbursement_date.between(past, future)
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction_id, collection.first.id)

    def test_advanced_search_range_node_disputed_date_less_than_or_equal_to(self):
        disputed_transaction_id = TestHelper.create_disputed_transaction().id
        disputed_time = datetime.now()
        past = disputed_time - timedelta(days=1)
        future = disputed_time + timedelta(minutes=10)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date <= past
        ])

        self.assertEqual(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date <= disputed_time
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(disputed_transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date <= future
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(disputed_transaction_id, collection.first.id)

    def test_advanced_search_range_node_disputed_date_greater_than_or_equal_to(self):
        disputed_transaction_id = TestHelper.create_disputed_transaction().id
        disputed_time = datetime.now()
        past = disputed_time - timedelta(minutes=10)
        future = disputed_time + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date >= past
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(disputed_transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date >= disputed_time
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(disputed_transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date >= future
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_disputed_date_between(self):
        disputed_transaction_id = TestHelper.create_disputed_transaction().id
        disputed_time = datetime.now()
        past = disputed_time - timedelta(days=1)
        future = disputed_time + timedelta(days=1)
        future2 = disputed_time + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date.between(past, disputed_time)
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(disputed_transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date.between(disputed_time, future)
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(disputed_transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date.between(past, future)
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(disputed_transaction_id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_disputed_date_is(self):
        disputed_transaction_id = TestHelper.create_disputed_transaction().id
        disputed_date = datetime.today()
        past = disputed_date - timedelta(days=10)
        future = disputed_date + timedelta(days=10)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date == past
        ])

        self.assertEqual(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date == future
        ])

        self.assertEqual(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date == disputed_date
        ])

        self.assertEqual(1, collection.maximum_size)

    def test_advanced_search_range_node_disputed_date_with_dates(self):
        disputed_transaction_id = TestHelper.create_disputed_transaction().id
        disputed_date = datetime.today()
        past = disputed_date - timedelta(days=1)
        future = disputed_date + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.id == disputed_transaction_id,
            TransactionSearch.dispute_date.between(past, future)
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(disputed_transaction_id, collection.first.id)

    def test_advanced_search_range_node_authorization_expired_at(self):
        two_days_ago = datetime.today() - timedelta(days=2)
        yesterday = datetime.today() - timedelta(days=1)
        tomorrow = datetime.today() + timedelta(days=1)

        collection = Transaction.search(
            TransactionSearch.authorization_expired_at.between(two_days_ago, yesterday)
        )
        self.assertEqual(0, collection.maximum_size)

        collection = Transaction.search(
            TransactionSearch.authorization_expired_at.between(yesterday, tomorrow)
        )
        self.assertTrue(collection.maximum_size > 0)
        self.assertEqual(Transaction.Status.AuthorizationExpired, collection.first.status)


    def test_advanced_search_range_node_authorized_at(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.authorized_at.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_failed_at(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.failed_at.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_gateway_rejected_at(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "processing_rules_merchant_id"
            Configuration.public_key = "processing_rules_public_key"
            Configuration.private_key = "processing_rules_private_key"

            transaction = Transaction.sale({
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

            self.assertEqual(1, collection.maximum_size)
            self.assertEqual(transaction.id, collection.first.id)

            collection = Transaction.search([
                TransactionSearch.id == transaction.id,
                TransactionSearch.gateway_rejected_at.between(future, future2)
            ])

            self.assertEqual(0, collection.maximum_size)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_advanced_search_range_node_processor_declined_at(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.processor_declined_at.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_settled_at(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.settled_at.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_submitted_for_settlement_at(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.submitted_for_settlement_at.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_voided_at(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.voided_at.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_range_node_can_search_on_multiple_statuses(self):
        transaction = Transaction.sale({
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

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.authorized_at.between(future, future2),
            TransactionSearch.submitted_for_settlement_at.between(future, future2)
        ])

        self.assertEqual(0, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.authorized_at.between(past, future),
            TransactionSearch.voided_at.between(past, future)
        ])

        self.assertEqual(0, collection.maximum_size)

    @unittest.skip("skip until CI is more stable")
    def test_advanced_search_returns_iteratable_results(self):
        collection = Transaction.search([
            TransactionSearch.credit_card_number.starts_with("411")
        ])

        self.assertTrue(collection.maximum_size > 100)

        transaction_ids = [transaction.id for transaction in collection.items]
        self.assertEqual(collection.maximum_size, len(TestHelper.unique(transaction_ids)))

    def test_advanced_search_can_search_on_paypal_fields(self):
        http = ClientApiHttp.create()
        status_code, nonce = http.get_paypal_nonce({
            "access_token": "PAYPAL-ACCESS-TOKEN",
            "options": {"validate": False}
        })
        self.assertEqual(202, status_code)

        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": nonce
        }).transaction

        collection = Transaction.search([
            TransactionSearch.paypal_payer_email == transaction.paypal_details.payer_email,
            TransactionSearch.paypal_authorization_id == transaction.paypal_details.authorization_id,
            TransactionSearch.paypal_payment_id == transaction.paypal_details.payment_id,
        ])
        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

    def test_advanced_search_can_search_on_store_id_1(self):
        transaction_id = "contact_visa_transaction"

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.store_id == "store-id"
        ])

        self.assertEqual(1, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.store_id == "invalid-store-id"
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_advanced_search_can_search_on_store_ids(self):
        transaction_id = "contact_visa_transaction"

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.store_ids.in_list(["store-id"])
        ])

        self.assertEqual(1, collection.maximum_size)

        collection = Transaction.search([
            TransactionSearch.id == transaction_id,
            TransactionSearch.store_ids.in_list(["invalid-store-id"])
        ])

        self.assertEqual(0, collection.maximum_size)

    def test_search_handles_a_search_timeout(self):
        with self.assertRaises(RequestTimeoutError):
            Transaction.search([
                TransactionSearch.amount.between("-1100", "1600")
            ])

    def test_search_returns_records_from_valid_daterange(self):
        yesterday = datetime.now() - timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=1)

        collection = Transaction.search([
            TransactionSearch.ach_return_responses_created_at.between(yesterday, tomorrow)
        ])
        self.assertEqual(2, collection.maximum_size)

    def test_search_returns_records_from_invalid_daterange(self):
        day_after_tomorrow = datetime.now() + timedelta(days=1)
        tomorrow = datetime.now() + timedelta(days=2)

        collection = Transaction.search([
            TransactionSearch.ach_return_responses_created_at.between(tomorrow, day_after_tomorrow)
        ])
        self.assertEqual(0, collection.maximum_size)

    def test_search_returns_records_for_one_reasoncode(self):
        collection = Transaction.search([
            TransactionSearch.reason_code.in_list(['R01'])
        ])
        self.assertEqual(1, collection.maximum_size)

    def test_search_returns_records_for_multiple_reasoncode(self):
        collection = Transaction.search([
            TransactionSearch.reason_code.in_list(['R01', 'R02'])
        ])
        self.assertEqual(2, collection.maximum_size)

    def test_search_returns_multiple_records_for_any_reason_code(self):
        collection = Transaction.search([
            TransactionSearch.reason_code == Transaction.ReasonCode.ANY_REASON_CODE
        ])
        self.assertEqual(2, collection.maximum_size)

    def test_search_retried_transaction(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.default_merchant_account_id,
            "amount": TransactionAmounts.Decline,
            "payment_method_token": "network_tokenized_credit_card",
            })
        transaction = result.transaction
        retry_transaction_id = transaction.retry_ids[0]

        collection = Transaction.search(
            TransactionSearch.id == retry_transaction_id,
            TransactionSearch.amount == TransactionAmounts.Decline,
        )
        self.assertEqual(1, collection.maximum_size)
        self.assertIsNotNone(collection.first.retried_transaction_id)
        self.assertEqual(retry_transaction_id, collection.first.id)
