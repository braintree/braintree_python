import json
from tests.test_helper import *
from braintree.test.credit_card_numbers import CreditCardNumbers
from braintree.test.nonces import Nonces
from braintree.dispute import Dispute
from braintree.payment_instrument_type import PaymentInstrumentType

import braintree.test.venmo_sdk as venmo_sdk

class TestTransaction(unittest.TestCase):

    def test_sale_returns_risk_data(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "device_session_id": "abc123",
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertIsInstance(transaction.risk_data, RiskData)
        self.assertEqual(transaction.risk_data.id, None)
        self.assertEqual(transaction.risk_data.decision, "Not Evaluated")
        self.assertTrue(hasattr(transaction.risk_data, 'device_data_captured'))

    def test_sale_returns_a_successful_result_with_type_of_sale(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search(r"\A\w{6,}\Z", transaction.id))
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual(Decimal(TransactionAmounts.Authorize), transaction.amount)
        self.assertEqual("411111", transaction.credit_card_details.bin)
        self.assertEqual("1111", transaction.credit_card_details.last_4)
        self.assertEqual("05/2009", transaction.credit_card_details.expiration_date)
        self.assertEqual(None, transaction.voice_referral_number)

    def test_sale_allows_amount_as_a_decimal(self):
        result = Transaction.sale({
            "amount": Decimal(TransactionAmounts.Authorize),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search(r"\A\w{6,}\Z", transaction.id))
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual(Decimal(TransactionAmounts.Authorize), transaction.amount)
        self.assertEqual("411111", transaction.credit_card_details.bin)
        self.assertEqual("1111", transaction.credit_card_details.last_4)
        self.assertEqual("05/2009", transaction.credit_card_details.expiration_date)

    def test_sale_with_expiration_month_and_year_separately(self):
        result = Transaction.sale({
            "amount": Decimal(TransactionAmounts.Authorize),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "05",
                "expiration_year": "2012"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual("05", transaction.credit_card_details.expiration_month)
        self.assertEqual("2012", transaction.credit_card_details.expiration_year)

    def test_sale_works_with_all_attributes(self):
        result = Transaction.sale({
            "amount": "100.00",
            "order_id": "123",
            "channel": "MyShoppingCartProvider",
            "credit_card": {
                "cardholder_name": "The Cardholder",
                "number": "5105105105105100",
                "expiration_date": "05/2011",
                "cvv": "123"
            },
            "customer": {
                "first_name": "Dan",
                "last_name": "Smith",
                "company": "Braintree",
                "email": "dan@example.com",
                "phone": "419-555-1234",
                "fax": "419-555-1235",
                "website": "http://braintreepayments.com"
            },
            "billing": {
                "first_name": "Carl",
                "last_name": "Jones",
                "company": "Braintree",
                "street_address": "123 E Main St",
                "extended_address": "Suite 403",
                "locality": "Chicago",
                "region": "IL",
                "postal_code": "60622",
                "country_name": "United States of America",
                "country_code_alpha2": "US",
                "country_code_alpha3": "USA",
                "country_code_numeric": "840"
            },
            "shipping": {
                "first_name": "Andrew",
                "last_name": "Mason",
                "company": "Braintree",
                "street_address": "456 W Main St",
                "extended_address": "Apt 2F",
                "locality": "Bartlett",
                "region": "IL",
                "postal_code": "60103",
                "country_name": "Mexico",
                "country_code_alpha2": "MX",
                "country_code_alpha3": "MEX",
                "country_code_numeric": "484"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search(r"\A\w{6,}\Z", transaction.id))
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual(Transaction.Status.Authorized, transaction.status)
        self.assertEqual(Decimal("100.00"), transaction.amount)
        self.assertEqual("123", transaction.order_id)
        self.assertEqual("MyShoppingCartProvider", transaction.channel)
        self.assertEqual("1000", transaction.processor_response_code)
        self.assertEqual(datetime, type(transaction.created_at))
        self.assertEqual(datetime, type(transaction.updated_at))
        self.assertEqual("510510", transaction.credit_card_details.bin)
        self.assertEqual("5100", transaction.credit_card_details.last_4)
        self.assertEqual("510510******5100", transaction.credit_card_details.masked_number)
        self.assertEqual("MasterCard", transaction.credit_card_details.card_type)
        self.assertEqual("The Cardholder", transaction.credit_card_details.cardholder_name)
        self.assertEqual(None, transaction.avs_error_response_code)
        self.assertEqual("M", transaction.avs_postal_code_response_code)
        self.assertEqual("M", transaction.avs_street_address_response_code)
        self.assertEqual("Dan", transaction.customer_details.first_name)
        self.assertEqual("Smith", transaction.customer_details.last_name)
        self.assertEqual("Braintree", transaction.customer_details.company)
        self.assertEqual("dan@example.com", transaction.customer_details.email)
        self.assertEqual("419-555-1234", transaction.customer_details.phone)
        self.assertEqual("419-555-1235", transaction.customer_details.fax)
        self.assertEqual("http://braintreepayments.com", transaction.customer_details.website)
        self.assertEqual("Carl", transaction.billing_details.first_name)
        self.assertEqual("Jones", transaction.billing_details.last_name)
        self.assertEqual("Braintree", transaction.billing_details.company)
        self.assertEqual("123 E Main St", transaction.billing_details.street_address)
        self.assertEqual("Suite 403", transaction.billing_details.extended_address)
        self.assertEqual("Chicago", transaction.billing_details.locality)
        self.assertEqual("IL", transaction.billing_details.region)
        self.assertEqual("60622", transaction.billing_details.postal_code)
        self.assertEqual("United States of America", transaction.billing_details.country_name)
        self.assertEqual("US", transaction.billing_details.country_code_alpha2)
        self.assertEqual("USA", transaction.billing_details.country_code_alpha3)
        self.assertEqual("840", transaction.billing_details.country_code_numeric)
        self.assertEqual("Andrew", transaction.shipping_details.first_name)
        self.assertEqual("Mason", transaction.shipping_details.last_name)
        self.assertEqual("Braintree", transaction.shipping_details.company)
        self.assertEqual("456 W Main St", transaction.shipping_details.street_address)
        self.assertEqual("Apt 2F", transaction.shipping_details.extended_address)
        self.assertEqual("Bartlett", transaction.shipping_details.locality)
        self.assertEqual("IL", transaction.shipping_details.region)
        self.assertEqual("60103", transaction.shipping_details.postal_code)
        self.assertEqual("Mexico", transaction.shipping_details.country_name)
        self.assertEqual("MX", transaction.shipping_details.country_code_alpha2)
        self.assertEqual("MEX", transaction.shipping_details.country_code_alpha3)
        self.assertEqual("484", transaction.shipping_details.country_code_numeric)
        self.assertEqual(None, transaction.additional_processor_response)

    def test_sale_with_vault_customer_and_credit_card_data(self):
        customer = Customer.create({
            "first_name": "Pingu",
            "last_name": "Penguin",
        }).customer

        result = Transaction.sale({
            "amount": Decimal(TransactionAmounts.Authorize),
            "customer_id": customer.id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(transaction.credit_card_details.masked_number, "411111******1111")
        self.assertEqual(None, transaction.vault_credit_card)

    def test_sale_with_vault_customer_and_credit_card_data_and_store_in_vault(self):
        customer = Customer.create({
            "first_name": "Pingu",
            "last_name": "Penguin",
        }).customer

        result = Transaction.sale({
            "amount": Decimal(TransactionAmounts.Authorize),
            "customer_id": customer.id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "store_in_vault": True
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual("411111******1111", transaction.credit_card_details.masked_number)
        self.assertEqual("411111******1111", transaction.vault_credit_card.masked_number)

    def test_sale_with_venmo_merchant_data(self):
        result = Transaction.sale({
            "amount": Decimal(TransactionAmounts.Authorize),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "venmo_merchant_data": {
                    "venmo_merchant_public_id": "12345",
                    "originating_transaction_id": "abc123",
                    "originating_merchant_id": "xyz123",
                    "originating_merchant_kind": "braintree",
                }
            }
        })

        self.assertTrue(result.is_success)

    def test_sale_with_custom_fields(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "custom_fields": {
                "store_me": "some extra stuff"
            }

        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual("some extra stuff", transaction.custom_fields["store_me"])

    def test_sale_with_merchant_account_id(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.non_default_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(TestHelper.non_default_merchant_account_id, transaction.merchant_account_id)

    def test_sale_without_merchant_account_id_falls_back_to_default(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(TestHelper.default_merchant_account_id, transaction.merchant_account_id)

    def test_sale_with_shipping_address_id(self):
        result = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010"
            }
        })
        self.assertTrue(result.is_success)
        customer = result.customer

        result = Address.create({
            "customer_id": customer.id,
            "street_address": "123 Fake St."
        })
        self.assertTrue(result.is_success)
        address = result.address

        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "customer_id": customer.id,
            "shipping_address_id": address.id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual("123 Fake St.", transaction.shipping_details.street_address)
        self.assertEqual(address.id, transaction.shipping_details.id)

    def test_sale_with_risk_data_security_parameters(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "risk_data": {
                "customer_browser": "IE7",
                "customer_ip": "192.168.0.1"
            }
        })

        self.assertTrue(result.is_success)

    def test_sale_with_billing_address_id(self):
        result = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010"
            }
        })
        self.assertTrue(result.is_success)
        customer = result.customer

        result = Address.create({
            "customer_id": customer.id,
            "street_address": "123 Fake St."
        })
        self.assertTrue(result.is_success)
        address = result.address

        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "customer_id": customer.id,
            "billing_address_id": address.id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual("123 Fake St.", transaction.billing_details.street_address)
        self.assertEqual(address.id, transaction.billing_details.id)

    def test_sale_with_device_session_id_and_fraud_merchant_id(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010"
            },
            "device_session_id": "abc123",
            "fraud_merchant_id": "456"
        })

        self.assertTrue(result.is_success)


    def test_sale_with_level_2(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "purchase_order_number": "12345",
            "tax_amount": Decimal("10.00"),
            "tax_exempt": True,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual("12345", transaction.purchase_order_number)
        self.assertEqual(Decimal("10.00"), transaction.tax_amount)
        self.assertEqual(True, transaction.tax_exempt)

    def test_create_with_invalid_tax_amount(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "tax_amount": "asdf",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        tax_amount_errors = result.errors.for_object("transaction").on("tax_amount")
        self.assertEqual(1, len(tax_amount_errors))
        self.assertEqual(ErrorCodes.Transaction.TaxAmountFormatIsInvalid, tax_amount_errors[0].code)

    def test_create_with_too_long_purchase_order_number(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "purchase_order_number": "aaaaaaaaaaaaaaaaaa",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        purchase_order_number_errors = result.errors.for_object("transaction").on("purchase_order_number")
        self.assertEqual(1, len(purchase_order_number_errors))
        self.assertEqual(ErrorCodes.Transaction.PurchaseOrderNumberIsTooLong, purchase_order_number_errors[0].code)

    def test_create_with_invalid_purchase_order_number(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "purchase_order_number": "\xc3\x9f\xc3\xa5\xe2\x88\x82",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        purchase_order_number_errors = result.errors.for_object("transaction").on("purchase_order_number")
        self.assertEqual(1, len(purchase_order_number_errors))
        self.assertEqual(ErrorCodes.Transaction.PurchaseOrderNumberIsInvalid, purchase_order_number_errors[0].code)

    def test_sale_with_level_3(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "purchase_order_number": "12345",
            "discount_amount": Decimal("1.00"),
            "shipping_amount": Decimal("2.00"),
            "ships_from_postal_code": "12345",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(Decimal("1.00"), transaction.discount_amount)
        self.assertEqual(Decimal("2.00"), transaction.shipping_amount)
        self.assertEqual("12345", transaction.ships_from_postal_code)

    def test_create_with_discount_amount_invalid(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "discount_amount": "asdf",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("transaction").on("discount_amount")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.Transaction.DiscountAmountFormatIsInvalid, errors[0].code)

    def test_create_with_discount_amount_negative(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "discount_amount": Decimal("-100"),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("transaction").on("discount_amount")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.Transaction.DiscountAmountCannotBeNegative, errors[0].code)

    def test_create_with_discount_amount_too_large(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "discount_amount": Decimal("999999999"),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("transaction").on("discount_amount")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.Transaction.DiscountAmountIsTooLarge, errors[0].code)

    def test_create_with_shipping_amount_invalid(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "shipping_amount": "asdf",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("transaction").on("shipping_amount")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.Transaction.ShippingAmountFormatIsInvalid, errors[0].code)

    def test_create_with_shipping_amount_negative(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "shipping_amount": Decimal("-100"),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("transaction").on("shipping_amount")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.Transaction.ShippingAmountCannotBeNegative, errors[0].code)

    def test_create_with_shipping_amount_too_large(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "shipping_amount": Decimal("999999999"),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("transaction").on("shipping_amount")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.Transaction.ShippingAmountIsTooLarge, errors[0].code)

    def test_create_with_ships_from_postal_code_is_too_long(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "ships_from_postal_code": "0000000000",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("transaction").on("ships_from_postal_code")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.Transaction.ShipsFromPostalCodeIsTooLong, errors[0].code)

    def test_create_with_ships_from_postal_code_invalid_characters(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "ships_from_postal_code": "1$345",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)

        errors = result.errors.for_object("transaction").on("ships_from_postal_code")
        self.assertEqual(1, len(errors))
        self.assertEqual(ErrorCodes.Transaction.ShipsFromPostalCodeInvalidCharacters, errors[0].code)

    def test_sale_with_processor_declined(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Decline,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertFalse(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.Status.ProcessorDeclined, transaction.status)
        self.assertEqual("2000 : Do Not Honor", transaction.additional_processor_response)

    def test_sale_with_gateway_rejected_with_incomplete_application(self):
        gateway = BraintreeGateway(
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret",
            environment=Environment.Development
        )

        result = gateway.merchant.create({
            "email": "name@email.com",
            "country_code_alpha3": "USA",
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

    def test_sale_with_gateway_rejected_with_avs(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "processing_rules_merchant_id"
            Configuration.public_key = "processing_rules_public_key"
            Configuration.private_key = "processing_rules_private_key"

            result = Transaction.sale({
                "amount": TransactionAmounts.Authorize,
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
            self.assertEqual(Transaction.GatewayRejectionReason.Avs, transaction.gateway_rejection_reason)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_sale_with_gateway_rejected_with_avs_and_cvv(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "processing_rules_merchant_id"
            Configuration.public_key = "processing_rules_public_key"
            Configuration.private_key = "processing_rules_private_key"

            result = Transaction.sale({
                "amount": TransactionAmounts.Authorize,
                "billing": {
                    "postal_code": "20000"
                },
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "05/2009",
                    "cvv": "200"
                }
            })

            self.assertFalse(result.is_success)
            transaction = result.transaction
            self.assertEqual(Transaction.GatewayRejectionReason.AvsAndCvv, transaction.gateway_rejection_reason)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_sale_with_gateway_rejected_with_cvv(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "processing_rules_merchant_id"
            Configuration.public_key = "processing_rules_public_key"
            Configuration.private_key = "processing_rules_private_key"

            result = Transaction.sale({
                "amount": TransactionAmounts.Authorize,
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "05/2009",
                    "cvv": "200"
                }
            })

            self.assertFalse(result.is_success)
            transaction = result.transaction
            self.assertEqual(Transaction.GatewayRejectionReason.Cvv, transaction.gateway_rejection_reason)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_sale_with_gateway_rejected_with_fraud(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4000111111111511",
                "expiration_date": "05/2017",
                "cvv": "333"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(Transaction.GatewayRejectionReason.Fraud, result.transaction.gateway_rejection_reason)

    def test_sale_with_service_fee(self):
        result = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.non_default_sub_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "service_fee_amount": "1.00"
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(transaction.service_fee_amount, "1.00")

    def test_sale_on_master_merchant_accoount_is_invalid_with_service_fee(self):
        result = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.non_default_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "service_fee_amount": "1.00"
        })
        self.assertFalse(result.is_success)

        amount_errors = result.errors.for_object("transaction").on("service_fee_amount")
        self.assertEqual(1, len(amount_errors))
        self.assertEqual(ErrorCodes.Transaction.ServiceFeeAmountNotAllowedOnMasterMerchantAccount, amount_errors[0].code)

    def test_sale_on_submerchant_is_invalid_without_with_service_fee(self):
        result = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.non_default_sub_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.SubMerchantAccountRequiresServiceFeeAmount,
            result.errors.for_object("transaction").on("merchant_account_id")[0].code
        )

    def test_sale_with_hold_in_escrow_option(self):
        result = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.non_default_sub_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "hold_in_escrow": True
            },
            "service_fee_amount": "1.00"
        })
        self.assertTrue(result.is_success)
        self.assertEqual(
            Transaction.EscrowStatus.HoldPending,
            result.transaction.escrow_status
        )

    def test_sale_with_hold_in_escrow_option_fails_for_master_merchant_account(self):
        result = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.non_default_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "hold_in_escrow": True
            }
        })
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.CannotHoldInEscrow,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_hold_in_escrow_after_sale(self):
        result = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.non_default_sub_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "service_fee_amount": "1.00"
        })
        self.assertTrue(result.is_success)
        result = Transaction.hold_in_escrow(result.transaction.id)
        self.assertTrue(result.is_success)
        self.assertEqual(
            Transaction.EscrowStatus.HoldPending,
            result.transaction.escrow_status
        )

    def test_hold_in_escrow_after_sale_fails_for_master_merchant_account(self):
        result = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.non_default_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertTrue(result.is_success)
        result = Transaction.hold_in_escrow(result.transaction.id)
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.CannotHoldInEscrow,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_release_from_escrow_from_escrow(self):
        transaction = self.__create_escrowed_transaction()
        result = Transaction.release_from_escrow(transaction.id)
        self.assertTrue(result.is_success)
        self.assertEqual(
            Transaction.EscrowStatus.ReleasePending,
            result.transaction.escrow_status
        )


    def test_release_from_escrow_from_escrow_fails_when_transaction_not_in_escrow(self):
        result = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.non_default_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertTrue(result.is_success)
        result = Transaction.release_from_escrow(result.transaction.id)
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.CannotReleaseFromEscrow,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_cancel_release_from_escrow(self):
        transaction = self.__create_escrowed_transaction()
        submit_result = Transaction.release_from_escrow(transaction.id)
        result = Transaction.cancel_release(submit_result.transaction.id)
        self.assertTrue(result.is_success)
        self.assertEqual(
                Transaction.EscrowStatus.Held,
                result.transaction.escrow_status
        )

    def test_cancel_release_from_escrow_fails_if_transaction_is_not_pending_release(self):
        transaction = self.__create_escrowed_transaction()
        result = Transaction.cancel_release(transaction.id)
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.CannotCancelRelease,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_sale_with_venmo_sdk_session(self):
        result = Transaction.sale({
            "amount": "10.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "venmo_sdk_session": venmo_sdk.Session
            }
        })

        self.assertTrue(result.is_success)
        self.assertFalse(result.transaction.credit_card_details.venmo_sdk)

    def test_sale_with_venmo_sdk_payment_method_code(self):
        result = Transaction.sale({
            "amount": "10.00",
            "venmo_sdk_payment_method_code": venmo_sdk.VisaPaymentMethodCode
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual("411111", transaction.credit_card_details.bin)

    def test_sale_with_payment_method_nonce(self):
        config = Configuration.instantiate()
        parsed_client_token = TestHelper.generate_decoded_client_token()
        authorization_fingerprint = json.loads(parsed_client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })
        _, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            },
            "share": True
        })
        nonce = json.loads(response)["creditCards"][0]["nonce"]


        result = Transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": nonce
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual("411111", transaction.credit_card_details.bin)

    def test_sale_with_fake_apple_pay_nonce(self):
        result = Transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": Nonces.ApplePayAmEx
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.amount, 10.00)
        self.assertEqual(result.transaction.payment_instrument_type, PaymentInstrumentType.ApplePayCard)
        apple_pay_details = result.transaction.apple_pay_details
        self.assertNotEqual(None, apple_pay_details)
        self.assertEqual(ApplePayCard.CardType.AmEx, apple_pay_details.card_type)
        self.assertEqual("AmEx 41002", apple_pay_details.payment_instrument_name)
        self.assertTrue(int(apple_pay_details.expiration_month) > 0)
        self.assertTrue(int(apple_pay_details.expiration_year) > 0)
        self.assertNotEqual(None, apple_pay_details.cardholder_name)

    def test_sale_with_fake_android_pay_proxy_card_nonce(self):
        result = Transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": Nonces.AndroidPayCardDiscover
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.amount, 10.00)
        self.assertEqual(result.transaction.payment_instrument_type, PaymentInstrumentType.AndroidPayCard)
        android_pay_card_details = result.transaction.android_pay_card_details
        self.assertNotEqual(None, android_pay_card_details)
        self.assertEqual(CreditCard.CardType.Discover, android_pay_card_details.card_type)
        self.assertTrue(int(android_pay_card_details.expiration_month) > 0)
        self.assertTrue(int(android_pay_card_details.expiration_year) > 0)

    def test_sale_with_fake_android_pay_network_token_nonce(self):
        result = Transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": Nonces.AndroidPayCardMasterCard
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.amount, 10.00)
        self.assertEqual(result.transaction.payment_instrument_type, PaymentInstrumentType.AndroidPayCard)
        android_pay_card_details = result.transaction.android_pay_card_details
        self.assertNotEqual(None, android_pay_card_details)
        self.assertEqual(CreditCard.CardType.MasterCard, android_pay_card_details.card_type)
        self.assertTrue(int(android_pay_card_details.expiration_month) > 0)
        self.assertTrue(int(android_pay_card_details.expiration_year) > 0)

    def test_sale_with_fake_amex_express_checkout_card_nonce(self):
        result = Transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": Nonces.AmexExpressCheckoutCard,
            "merchant_account_id": TestHelper.fake_amex_direct_merchant_account_id,
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.amount, 10.00)
        self.assertEqual(result.transaction.payment_instrument_type, PaymentInstrumentType.AmexExpressCheckoutCard)
        amex_express_checkout_card_details = result.transaction.amex_express_checkout_card_details
        self.assertNotEqual(None, amex_express_checkout_card_details)
        self.assertEqual(CreditCard.CardType.AmEx, amex_express_checkout_card_details.card_type)
        self.assertTrue(int(amex_express_checkout_card_details.expiration_month) > 0)
        self.assertTrue(int(amex_express_checkout_card_details.expiration_year) > 0)

    def test_sale_with_fake_venmo_account_nonce(self):
        result = Transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": Nonces.VenmoAccount,
            "merchant_account_id": TestHelper.fake_venmo_account_merchant_account_id,
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.amount, 10.00)
        self.assertEqual(result.transaction.payment_instrument_type, PaymentInstrumentType.VenmoAccount)

        venmo_account_details = result.transaction.venmo_account_details
        self.assertIsNotNone(venmo_account_details)
        self.assertEqual(venmo_account_details.username, "venmojoe")
        self.assertEqual(venmo_account_details.venmo_user_id, "Venmo-Joe-1")

    def test_sale_with_fake_venmo_account_nonce_and_profile_id(self):
        result = Transaction.sale({
            "amount": "10.00",
            "payment_method_nonce": Nonces.VenmoAccount,
            "merchant_account_id": TestHelper.fake_venmo_account_merchant_account_id,
            "options": {
                "venmo": {
                    "profile_id": "integration_venmo_merchant_public_id",
                    },
                },
            })

        self.assertTrue(result.is_success)

    def test_sale_with_advanced_fraud_checking_skipped(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009"
            },
            "options": {
                "skip_advanced_fraud_checking": True
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertIsInstance(transaction.risk_data, RiskData)
        self.assertEqual(transaction.risk_data.id, None)

    def test_sale_with_skip_cvv_option_set(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009"
            },
            "options": {
                "skip_cvv": True
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(transaction.cvv_response_code, "B")

    def test_sale_with_skip_avs_option_set(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009"
            },
            "options": {
                "skip_avs": True
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(transaction.avs_error_response_code, None)
        self.assertEqual(transaction.avs_street_address_response_code, "B")

    def test_sale_with_line_items_zero(self):
        result = Transaction.sale({
            "amount": "45.15",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            }
        })

        self.assertTrue(result.is_success)

        transaction = result.transaction

        line_items = transaction.line_items
        self.assertEqual(0, len(line_items))

    def test_sale_with_line_items_single_only_required_fields(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "total_amount": "45.15",
            }]
        })

        self.assertTrue(result.is_success)

        transaction = result.transaction

        line_items = transaction.line_items
        self.assertEqual(1, len(line_items))

        lineItem = line_items[0]
        self.assertEqual("1.0232", lineItem.quantity)
        self.assertEqual("Name #1", lineItem.name)
        self.assertEqual(TransactionLineItem.Kind.Debit, lineItem.kind)
        self.assertEqual("45.1232", lineItem.unit_amount)
        self.assertEqual("45.15", lineItem.total_amount)

    def test_sale_with_line_items_single(self):
        result = Transaction.sale({
            "amount": "45.15",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "description": "Description #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_tax_amount": "1.23",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "tax_amount": "4.50",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
                "url": "https://example.com/products/23434",
            }]
        })

        self.assertTrue(result.is_success)

        transaction = result.transaction

        line_items = transaction.line_items
        self.assertEqual(1, len(line_items))

        lineItem = line_items[0]
        self.assertEqual("1.0232", lineItem.quantity)
        self.assertEqual("Name #1", lineItem.name)
        self.assertEqual("Description #1", lineItem.description)
        self.assertEqual(TransactionLineItem.Kind.Debit, lineItem.kind)
        self.assertEqual("45.1232", lineItem.unit_amount)
        self.assertEqual("1.23", lineItem.unit_tax_amount)
        self.assertEqual("gallon", lineItem.unit_of_measure)
        self.assertEqual("1.02", lineItem.discount_amount)
        self.assertEqual("4.50", lineItem.tax_amount)
        self.assertEqual("45.15", lineItem.total_amount)
        self.assertEqual("23434", lineItem.product_code)
        self.assertEqual("9SAASSD8724", lineItem.commodity_code)
        self.assertEqual("https://example.com/products/23434", lineItem.url)

    def test_sale_with_line_items_multiple(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "description": "Description #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "tax_amount": "4.50",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "2.02",
                "name": "Name #2",
                "description": "Description #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "5",
                "unit_of_measure": "gallon",
                "tax_amount": "4.50",
                "total_amount": "45.15",
            }]
        })

        self.assertTrue(result.is_success)

        transaction = result.transaction

        line_items = transaction.line_items
        self.assertEqual(2, len(line_items))

        line_item_1 = None
        for line_item in line_items:
            if line_item.name == "Name #1":
                line_item_1 = line_item
                break
        if line_item_1 is None:
            self.fail("TransactionLineItem with name \"Name #1\" not returned.")
        self.assertEqual("1.0232", line_item_1.quantity)
        self.assertEqual("Name #1", line_item_1.name)
        self.assertEqual("Description #1", line_item_1.description)
        self.assertEqual(TransactionLineItem.Kind.Debit, line_item_1.kind)
        self.assertEqual("45.1232", line_item_1.unit_amount)
        self.assertEqual("gallon", line_item_1.unit_of_measure)
        self.assertEqual("1.02", line_item_1.discount_amount)
        self.assertEqual("45.15", line_item_1.total_amount)
        self.assertEqual("23434", line_item_1.product_code)
        self.assertEqual("9SAASSD8724", line_item_1.commodity_code)

        line_item_2 = None
        for line_item in line_items:
            if line_item.name == "Name #2":
                line_item_2 = line_item
                break
        if line_item_2 is None:
            self.fail("TransactionLineItem with name \"Name #2\" not returned.")
        self.assertEqual("2.02", line_item_2.quantity)
        self.assertEqual("Name #2", line_item_2.name)
        self.assertEqual("Description #2", line_item_2.description)
        self.assertEqual(TransactionLineItem.Kind.Credit, line_item_2.kind)
        self.assertEqual("5", line_item_2.unit_amount)
        self.assertEqual("gallon", line_item_2.unit_of_measure)
        self.assertEqual("45.15", line_item_2.total_amount)
        self.assertEqual(None, line_item_2.discount_amount)
        self.assertEqual(None, line_item_2.product_code)
        self.assertEqual(None, line_item_2.commodity_code)

    def test_sale_with_line_items_with_zero_amount_fields(self):
        result = Transaction.sale({
            "amount": "45.15",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "total_amount": "45.15",
                "discount_amount": "0",
                "unit_tax_amount": "0",
                "tax_amount": "0",
            }]
        })

        self.assertTrue(result.is_success)

        transaction = result.transaction

        line_items = transaction.line_items

        lineItem = line_items[0]
        self.assertEqual("0.00", lineItem.unit_tax_amount)
        self.assertEqual("0.00", lineItem.discount_amount)
        self.assertEqual("0.00", lineItem.tax_amount)

    def test_sale_with_line_items_validation_error_commodity_code_is_too_long(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "0123456789123",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.CommodityCodeIsTooLong,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("commodity_code")[0].code
        )

    def test_sale_with_line_items_validation_error_description_is_too_long(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "description": "This is a line item description which is far too long. Like, way too long to be practical. We don't like how long this line item description is.",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.DescriptionIsTooLong,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("description")[0].code
        )

    def test_sale_with_line_items_validation_error_discount_amount_is_too_large(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "2147483648",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.DiscountAmountIsTooLarge,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("discount_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_discount_amount_cannot_be_negative(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "-1.23",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.DiscountAmountCannotBeNegative,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("discount_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_tax_amount_is_too_large(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "tax_amount": "2147483648",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.TaxAmountIsTooLarge,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_0").on("tax_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_tax_amount_cannot_be_negative(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "tax_amount": "-1.23",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.TaxAmountCannotBeNegative,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_0").on("tax_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_tax_amount_format_is_invalid(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "tax_amount": "4.555",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.TaxAmountFormatIsInvalid,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_0").on("tax_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_kind_is_required(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.KindIsRequired,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("kind")[0].code
        )

    def test_sale_with_line_items_validation_error_name_is_required(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.NameIsRequired,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("name")[0].code
        )

    def test_sale_with_line_items_validation_error_name_is_too_long(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "123456789012345678901234567890123456",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.NameIsTooLong,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("name")[0].code
        )

    def test_sale_with_line_items_validation_error_product_code_is_too_long(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "123456789012345678901234567890123456",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.ProductCodeIsTooLong,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("product_code")[0].code
        )

    def test_sale_with_line_items_validation_error_quantity_is_required(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.QuantityIsRequired,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("quantity")[0].code
        )

    def test_sale_with_line_items_validation_error_quantity_is_too_large(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "2147483648",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.QuantityIsTooLarge,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("quantity")[0].code
        )

    def test_sale_with_line_items_validation_error_total_amount_is_required(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.TotalAmountIsRequired,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("total_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_total_amount_is_too_large(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "2147483648",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.TotalAmountIsTooLarge,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("total_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_total_amount_must_be_greater_than_zero(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "-2",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.TotalAmountMustBeGreaterThanZero,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("total_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_unit_amount_is_required(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.UnitAmountIsRequired,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("unit_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_unit_amount_is_too_large(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "2147483648",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.UnitAmountIsTooLarge,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("unit_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_unit_amount_must_be_greater_than_zero(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "-2",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.UnitAmountMustBeGreaterThanZero,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("unit_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_unit_of_measure_is_too_large(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.0232",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.0232",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.1232",
                "unit_of_measure": "1234567890123",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.UnitOfMeasureIsTooLarge,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("unit_of_measure")[0].code
        )

    def test_sale_with_line_items_validation_error_unit_tax_amount_format_is_invalid(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.2322",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.2322",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.0122",
                "unit_tax_amount": "2.012",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.UnitTaxAmountFormatIsInvalid,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("unit_tax_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_unit_tax_amount_is_too_large(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.2322",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_tax_amount": "1.23",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.2322",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.0122",
                "unit_tax_amount": "2147483648",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.UnitTaxAmountIsTooLarge,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("unit_tax_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_unit_tax_amount_cannot_be_negative(self):
        result = Transaction.sale({
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [{
                "quantity": "1.2322",
                "name": "Name #1",
                "kind": TransactionLineItem.Kind.Debit,
                "unit_amount": "45.1232",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            },
            {
                "quantity": "1.2322",
                "name": "Name #2",
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "45.0122",
                "unit_tax_amount": "-1.23",
                "unit_of_measure": "gallon",
                "discount_amount": "1.02",
                "total_amount": "45.15",
                "product_code": "23434",
                "commodity_code": "9SAASSD8724",
            }]
        })

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.LineItem.UnitTaxAmountCannotBeNegative,
            result.errors.for_object("transaction").for_object("line_items").for_object("index_1").on("unit_tax_amount")[0].code
        )

    def test_sale_with_line_items_validation_error_too_many_live_items(self):
        sale_params = {
            "amount": "35.05",
            "credit_card": {
                "number": CreditCardNumbers.Visa,
                "expiration_date": "05/2009",
            },
            "line_items": [],
        }

        for i in range(250):
            sale_params["line_items"].append({
                "quantity": "2.02",
                "name": "Line item #" + str(i),
                "kind": TransactionLineItem.Kind.Credit,
                "unit_amount": "5",
                "unit_of_measure": "gallon",
                "total_amount": "10.1",
            })

        result = Transaction.sale(sale_params)

        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.TooManyLineItems,
            result.errors.for_object("transaction").on("line_items")[0].code
        )

    def test_validation_error_on_invalid_custom_fields(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "custom_fields": {
                "invalid_key": "some extra stuff"
            }

        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.CustomFieldIsInvalid,
            result.errors.for_object("transaction").on("custom_fields")[0].code
        )

    def test_card_type_indicators(self):
        result = Transaction.sale({
            "amount": Decimal(TransactionAmounts.Authorize),
            "credit_card": {
                "number": CreditCardNumbers.CardTypeIndicators.Unknown,
                "expiration_month": "05",
                "expiration_year": "2012"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(CreditCard.Prepaid.Unknown, transaction.credit_card_details.prepaid)
        self.assertEqual(CreditCard.Debit.Unknown, transaction.credit_card_details.debit)
        self.assertEqual(CreditCard.Commercial.Unknown, transaction.credit_card_details.commercial)
        self.assertEqual(CreditCard.Healthcare.Unknown, transaction.credit_card_details.healthcare)
        self.assertEqual(CreditCard.Payroll.Unknown, transaction.credit_card_details.payroll)
        self.assertEqual(CreditCard.DurbinRegulated.Unknown, transaction.credit_card_details.durbin_regulated)
        self.assertEqual(CreditCard.CardTypeIndicator.Unknown, transaction.credit_card_details.issuing_bank)
        self.assertEqual(CreditCard.CardTypeIndicator.Unknown, transaction.credit_card_details.country_of_issuance)
        self.assertEqual(CreditCard.ProductId.Unknown, transaction.credit_card_details.product_id)

    def test_create_can_set_recurring_flag(self):
        result = Transaction.sale({
            "amount": "100",
            "customer": {
                "first_name": "Adam",
                "last_name": "Williams"
            },
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "recurring": True
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(True, transaction.recurring)

    def test_create_can_set_transaction_source_flag_recurring(self):
        result = Transaction.sale({
            "amount": "100",
            "customer": {
                "first_name": "Adam",
                "last_name": "Williams"
            },
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "transaction_source": "recurring"
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(True, transaction.recurring)

    def test_create_can_set_transaction_source_flag_moto(self):
        result = Transaction.sale({
            "amount": "100",
            "customer": {
                "first_name": "Adam",
                "last_name": "Williams"
            },
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "transaction_source": "moto"
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(False, transaction.recurring)

    def test_create_can_store_customer_and_credit_card_in_the_vault(self):
        result = Transaction.sale({
            "amount": "100",
            "customer": {
                "first_name": "Adam",
                "last_name": "Williams"
            },
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "store_in_vault": True
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search(r"\A\d{6,}\Z", transaction.customer_details.id))
        self.assertEqual(transaction.customer_details.id, transaction.vault_customer.id)
        self.assertNotEqual(None, re.search(r"\A\w{4,}\Z", transaction.credit_card_details.token))
        self.assertEqual(transaction.credit_card_details.token, transaction.vault_credit_card.token)

    def test_create_can_store_customer_and_credit_card_in_the_vault_on_success(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "customer": {
                "first_name": "Adam",
                "last_name": "Williams"
            },
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "store_in_vault_on_success": True
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search(r"\A\d{6,}\Z", transaction.customer_details.id))
        self.assertEqual(transaction.customer_details.id, transaction.vault_customer.id)
        self.assertNotEqual(None, re.search(r"\A\w{4,}\Z", transaction.credit_card_details.token))
        self.assertEqual(transaction.credit_card_details.token, transaction.vault_credit_card.token)

    def test_create_does_not_store_customer_and_credit_card_in_the_vault_on_failure(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Decline,
            "customer": {
                "first_name": "Adam",
                "last_name": "Williams"
            },
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "store_in_vault_on_success": True
            }
        })

        self.assertFalse(result.is_success)
        transaction = result.transaction
        self.assertEqual(None, transaction.customer_details.id)
        self.assertEqual(None, transaction.credit_card_details.token)
        self.assertEqual(None, transaction.vault_customer)
        self.assertEqual(None, transaction.vault_credit_card)

    def test_create_associated_a_billing_address_with_credit_card_in_vault(self):
        result = Transaction.sale({
            "amount": "100",
            "customer": {
                "first_name": "Adam",
                "last_name": "Williams"
            },
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2012"
            },
            "billing": {
                "first_name": "Carl",
                "last_name": "Jones",
                "company": "Braintree",
                "street_address": "123 E Main St",
                "extended_address": "Suite 403",
                "locality": "Chicago",
                "region": "IL",
                "postal_code": "60622",
                "country_name": "United States of America"
            },
            "options": {
                "store_in_vault": True,
                "add_billing_address_to_payment_method": True,
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search(r"\A\d{6,}\Z", transaction.customer_details.id))
        self.assertEqual(transaction.customer_details.id, transaction.vault_customer.id)
        credit_card = CreditCard.find(transaction.vault_credit_card.token)
        self.assertEqual(credit_card.billing_address.id, transaction.billing_details.id)
        self.assertEqual(credit_card.billing_address.id, transaction.vault_billing_address.id)
        self.assertEqual("Carl", credit_card.billing_address.first_name)
        self.assertEqual("Jones", credit_card.billing_address.last_name)
        self.assertEqual("Braintree", credit_card.billing_address.company)
        self.assertEqual("123 E Main St", credit_card.billing_address.street_address)
        self.assertEqual("Suite 403", credit_card.billing_address.extended_address)
        self.assertEqual("Chicago", credit_card.billing_address.locality)
        self.assertEqual("IL", credit_card.billing_address.region)
        self.assertEqual("60622", credit_card.billing_address.postal_code)
        self.assertEqual("United States of America", credit_card.billing_address.country_name)

    def test_create_and_store_the_shipping_address_in_the_vault(self):
        result = Transaction.sale({
            "amount": "100",
            "customer": {
                "first_name": "Adam",
                "last_name": "Williams"
            },
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2012"
            },
            "shipping": {
                "first_name": "Carl",
                "last_name": "Jones",
                "company": "Braintree",
                "street_address": "123 E Main St",
                "extended_address": "Suite 403",
                "locality": "Chicago",
                "region": "IL",
                "postal_code": "60622",
                "country_name": "United States of America"
            },
            "options": {
                "store_in_vault": True,
                "store_shipping_address_in_vault": True,
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search(r"\A\d{6,}\Z", transaction.customer_details.id))
        self.assertEqual(transaction.customer_details.id, transaction.vault_customer.id)
        shipping_address = transaction.vault_customer.addresses[0]
        self.assertEqual("Carl", shipping_address.first_name)
        self.assertEqual("Jones", shipping_address.last_name)
        self.assertEqual("Braintree", shipping_address.company)
        self.assertEqual("123 E Main St", shipping_address.street_address)
        self.assertEqual("Suite 403", shipping_address.extended_address)
        self.assertEqual("Chicago", shipping_address.locality)
        self.assertEqual("IL", shipping_address.region)
        self.assertEqual("60622", shipping_address.postal_code)
        self.assertEqual("United States of America", shipping_address.country_name)

    def test_create_submits_for_settlement_if_given_submit_for_settlement_option(self):
        result = Transaction.sale({
            "amount": "100",
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2012"
            },
            "options": {
                "submit_for_settlement": True
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(Transaction.Status.SubmittedForSettlement, result.transaction.status)

    def test_create_does_not_submit_for_settlement_if_submit_for_settlement_is_false(self):
        result = Transaction.sale({
            "amount": "100",
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2012"
            },
            "options": {
                "submit_for_settlement": False
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(Transaction.Status.Authorized, result.transaction.status)

    def test_create_can_specify_the_customer_id_and_payment_method_token(self):
        customer_id = "customer_" + str(random.randint(1, 1000000))
        payment_method_token = "credit_card_" + str(random.randint(1, 1000000))

        result = Transaction.sale({
            "amount": "100",
            "customer": {
              "id": customer_id,
              "first_name": "Adam",
              "last_name": "Williams"
            },
            "credit_card": {
              "token": payment_method_token,
              "number": "5105105105105100",
              "expiration_date": "05/2012"
            },
            "options": {
              "store_in_vault": True
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(customer_id, transaction.customer_details.id)
        self.assertEqual(customer_id, transaction.vault_customer.id)
        self.assertEqual(payment_method_token, transaction.credit_card_details.token)
        self.assertEqual(payment_method_token, transaction.vault_credit_card.token)

    def test_create_using_customer_id(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
            }
        })
        self.assertTrue(result.is_success)
        customer = result.customer
        credit_card = customer.credit_cards[0]

        result = Transaction.sale({
            "amount": "100",
            "customer_id": customer.id
        })
        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(customer.id, transaction.customer_details.id)
        self.assertEqual(customer.id, transaction.vault_customer.id)
        self.assertEqual(credit_card.token, transaction.credit_card_details.token)
        self.assertEqual(credit_card.token, transaction.vault_credit_card.token)

    def test_create_using_payment_method_token(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
            }
        })
        self.assertTrue(result.is_success)
        customer = result.customer
        credit_card = customer.credit_cards[0]

        result = Transaction.sale({
            "amount": "100",
            "payment_method_token": credit_card.token
        })
        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(customer.id, transaction.customer_details.id)
        self.assertEqual(customer.id, transaction.vault_customer.id)
        self.assertEqual(credit_card.token, transaction.credit_card_details.token)
        self.assertEqual(credit_card.token, transaction.vault_credit_card.token)

    def test_create_using_payment_method_token_with_cvv(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
            }
        })
        self.assertTrue(result.is_success)
        customer = result.customer
        credit_card = customer.credit_cards[0]

        result = Transaction.sale({
            "amount": "100",
            "payment_method_token": credit_card.token,
            "credit_card": {
                "cvv": "301"
            }
        })
        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(customer.id, transaction.customer_details.id)
        self.assertEqual(customer.id, transaction.vault_customer.id)
        self.assertEqual(credit_card.token, transaction.credit_card_details.token)
        self.assertEqual(credit_card.token, transaction.vault_credit_card.token)
        self.assertEqual("S", transaction.cvv_response_code)

    def test_create_with_failing_validations(self):
        params = {
            "transaction": {
                "amount": None,
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "05/2009"
                }
            }
        }
        result = Transaction.sale(params["transaction"])
        params["transaction"]["credit_card"].pop("number")
        self.assertFalse(result.is_success)
        self.assertEqual(params, result.params)
        self.assertEqual(
            ErrorCodes.Transaction.AmountIsRequired,
            result.errors.for_object("transaction").on("amount")[0].code
        )

    def test_credit_with_a_successful_result(self):
        result = Transaction.credit({
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

    def test_credit_with_unsuccessful_result(self):
        result = Transaction.credit({
            "amount": None,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        params = {
            "transaction": {
                "type": Transaction.Type.Credit,
                "amount": None,
                "credit_card": {
                    "expiration_date": "05/2009"
                }
            }
        }

        self.assertFalse(result.is_success)
        self.assertEqual(params, result.params)
        self.assertEqual(
            ErrorCodes.Transaction.AmountIsRequired,
            result.errors.for_object("transaction").on("amount")[0].code
        )

    def test_credit_card_payment_instrument_type_is_credit_card(self):
        result = Transaction.credit({
            "amount": Decimal(TransactionAmounts.Authorize),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(
            PaymentInstrumentType.CreditCard,
            transaction.payment_instrument_type
        )

    def test_service_fee_not_allowed_with_credits(self):
        result = Transaction.credit({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "service_fee_amount": "1.00"
        })

        self.assertFalse(result.is_success)
        self.assertTrue(
            ErrorCodes.Transaction.ServiceFeeIsNotAllowedOnCredits in [error.code for error in result.errors.for_object("transaction").on("base")]
        )

    def test_credit_with_merchant_account_id(self):
        result = Transaction.credit({
            "amount": TransactionAmounts.Authorize,
            "merchant_account_id": TestHelper.non_default_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(TestHelper.non_default_merchant_account_id, transaction.merchant_account_id)

    def test_credit_without_merchant_account_id_falls_back_to_default(self):
        result = Transaction.credit({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(TestHelper.default_merchant_account_id, transaction.merchant_account_id)

    def test_find_returns_a_found_transaction(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Fail,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction
        TestHelper.settle_transaction(transaction.id)
        found_transaction = Transaction.find(transaction.id)
        self.assertEqual(transaction.id, found_transaction.id)

    @raises_with_regexp(NotFoundError, "transaction with id 'notreal' not found")
    def test_find_for_bad_transaction_raises_not_found_error(self):
        Transaction.find("notreal")

    def test_void_with_successful_result(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        result = Transaction.void(transaction.id)
        self.assertTrue(result.is_success)
        self.assertEqual(transaction.id, result.transaction.id)
        self.assertEqual(Transaction.Status.Voided, result.transaction.status)

    def test_void_with_unsuccessful_result(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Decline,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        result = Transaction.void(transaction.id)
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.CannotBeVoided,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_create_with_successful_result(self):
        result = Transaction.create({
            "type": Transaction.Type.Sale,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.Type.Sale, transaction.type)

    def test_create_with_error_result(self):
        result = Transaction.create({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "billing": {
                "country_code_alpha2": "ZZ",
                "country_code_alpha3": "ZZZ",
                "country_code_numeric": "000",
                "country_name": "zzzzzz"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(ErrorCodes.Transaction.TypeIsRequired, result.errors.for_object("transaction").on("type")[0].code)
        self.assertEqual(
            ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted,
            result.errors.for_object("transaction").for_object("billing").on("country_code_alpha2")[0].code
        )
        self.assertEqual(
            ErrorCodes.Address.CountryCodeAlpha3IsNotAccepted,
            result.errors.for_object("transaction").for_object("billing").on("country_code_alpha3")[0].code
        )
        self.assertEqual(
            ErrorCodes.Address.CountryCodeNumericIsNotAccepted,
            result.errors.for_object("transaction").for_object("billing").on("country_code_numeric")[0].code
        )
        self.assertEqual(
            ErrorCodes.Address.CountryNameIsNotAccepted,
            result.errors.for_object("transaction").for_object("billing").on("country_name")[0].code
        )

    def test_sale_from_transparent_redirect_with_successful_result(self):
        tr_data = {
            "transaction": {
                "amount": TransactionAmounts.Authorize,
            }
        }
        post_params = {
            "tr_data": Transaction.tr_data_for_sale(tr_data, "http://example.com/path"),
            "transaction[credit_card][number]": "4111111111111111",
            "transaction[credit_card][expiration_date]": "05/2010",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Transaction.transparent_redirect_create_url())
        result = Transaction.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)

        transaction = result.transaction
        self.assertEqual(Decimal(TransactionAmounts.Authorize), transaction.amount)
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual("411111", transaction.credit_card_details.bin)
        self.assertEqual("1111", transaction.credit_card_details.last_4)
        self.assertEqual("05/2010", transaction.credit_card_details.expiration_date)

    def test_sale_from_transparent_redirect_with_error_result(self):
        tr_data = {
            "transaction": {
                "amount": TransactionAmounts.Authorize,
            }
        }
        post_params = {
            "tr_data": Transaction.tr_data_for_sale(tr_data, "http://example.com/path"),
            "transaction[credit_card][number]": "booya",
            "transaction[credit_card][expiration_date]": "05/2010",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Transaction.transparent_redirect_create_url())
        result = Transaction.confirm_transparent_redirect(query_string)
        self.assertFalse(result.is_success)
        self.assertTrue(len(result.errors.for_object("transaction").for_object("credit_card").on("number")) > 0)

    def test_sale_from_transparent_redirect_with_403_and_message(self):
        tr_data = {
            "transaction": {
                "amount": TransactionAmounts.Authorize
            }
        }
        post_params = {
            "tr_data": Transaction.tr_data_for_sale(tr_data, "http://example.com/path"),
            "transaction[credit_card][number]": "booya",
            "transaction[credit_card][expiration_date]": "05/2010",
            "transaction[bad]": "value"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Transaction.transparent_redirect_create_url())
        try:
            Transaction.confirm_transparent_redirect(query_string)
            self.fail()
        except AuthorizationError as e:
            self.assertEqual("Invalid params: transaction[bad]", str(e))

    def test_credit_from_transparent_redirect_with_successful_result(self):
        tr_data = {
            "transaction": {
                "amount": TransactionAmounts.Authorize,
            }
        }
        post_params = {
            "tr_data": Transaction.tr_data_for_credit(tr_data, "http://example.com/path"),
            "transaction[credit_card][number]": "4111111111111111",
            "transaction[credit_card][expiration_date]": "05/2010",
            "transaction[billing][country_code_alpha2]": "US",
            "transaction[billing][country_code_alpha3]": "USA",
            "transaction[billing][country_code_numeric]": "840",
            "transaction[billing][country_name]": "United States of America"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Transaction.transparent_redirect_create_url())
        result = Transaction.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)

        transaction = result.transaction
        self.assertEqual(Decimal(TransactionAmounts.Authorize), transaction.amount)
        self.assertEqual(Transaction.Type.Credit, transaction.type)
        self.assertEqual("411111", transaction.credit_card_details.bin)
        self.assertEqual("1111", transaction.credit_card_details.last_4)
        self.assertEqual("05/2010", transaction.credit_card_details.expiration_date)

        self.assertEqual("US", transaction.billing_details.country_code_alpha2)
        self.assertEqual("USA", transaction.billing_details.country_code_alpha3)
        self.assertEqual("840", transaction.billing_details.country_code_numeric)
        self.assertEqual("United States of America", transaction.billing_details.country_name)

    def test_credit_from_transparent_redirect_with_error_result(self):
        tr_data = {
            "transaction": {
                "amount": TransactionAmounts.Authorize,
            }
        }
        post_params = {
            "tr_data": Transaction.tr_data_for_credit(tr_data, "http://example.com/path"),
            "transaction[credit_card][number]": "booya",
            "transaction[credit_card][expiration_date]": "05/2010",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Transaction.transparent_redirect_create_url())
        result = Transaction.confirm_transparent_redirect(query_string)
        self.assertFalse(result.is_success)
        self.assertTrue(len(result.errors.for_object("transaction").for_object("credit_card").on("number")) > 0)

    def test_submit_for_settlement_without_amount(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        submitted_transaction = Transaction.submit_for_settlement(transaction.id).transaction

        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)
        self.assertEqual(Decimal(TransactionAmounts.Authorize), submitted_transaction.amount)

    def test_submit_for_settlement_with_amount(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        submitted_transaction = Transaction.submit_for_settlement(transaction.id, Decimal("900")).transaction

        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)
        self.assertEqual(Decimal("900.00"), submitted_transaction.amount)

    def test_submit_for_settlement_with_order_id(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        params = {"order_id": "ABC123"}

        submitted_transaction = Transaction.submit_for_settlement(transaction.id, Decimal("900"), params).transaction

        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)
        self.assertEqual("ABC123", submitted_transaction.order_id)

    def test_submit_for_settlement_with_descriptor(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        params = {
            "descriptor": {
                "name": "123*123456789012345678",
                "phone": "3334445555",
                "url": "ebay.com"
            }
        }

        submitted_transaction = Transaction.submit_for_settlement(transaction.id, Decimal("900"), params).transaction

        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)
        self.assertEqual("123*123456789012345678", submitted_transaction.descriptor.name)
        self.assertEqual("3334445555", submitted_transaction.descriptor.phone)
        self.assertEqual("ebay.com", submitted_transaction.descriptor.url)

    @raises_with_regexp(KeyError, "'Invalid keys: invalid_param'")
    def test_submit_for_settlement_with_invalid_params(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        params = {
            "descriptor": {
                "name": "123*123456789012345678",
                "phone": "3334445555",
                "url": "ebay.com"
            },
            "invalid_param": "foo",
        }

        Transaction.submit_for_settlement(transaction.id, Decimal("900"), params)

    def test_submit_for_settlement_with_validation_error(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        result = Transaction.submit_for_settlement(transaction.id, Decimal("1200"))
        self.assertFalse(result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.SettlementAmountIsTooLarge,
            result.errors.for_object("transaction").on("amount")[0].code
        )

    def test_submit_for_settlement_with_validation_error_on_service_fee(self):
        transaction = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.non_default_sub_merchant_account_id,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "service_fee_amount": "5.00"
        }).transaction

        result = Transaction.submit_for_settlement(transaction.id, "1.00")

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.SettlementAmountIsLessThanServiceFeeAmount,
            result.errors.for_object("transaction").on("amount")[0].code
        )

    def test_update_details_with_valid_params(self):
        transaction = Transaction.sale({
            "amount": "10.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            }
        }).transaction

        params = {
            "amount" : "9.00",
            "order_id": "123",
            "descriptor": {
                "name": "456*123456789012345678",
                "phone": "3334445555",
                "url": "ebay.com"
            }
        }

        result = Transaction.update_details(transaction.id, params)
        self.assertTrue(result.is_success)
        self.assertEqual(Decimal("9.00"), result.transaction.amount)
        self.assertEqual(Transaction.Status.SubmittedForSettlement, result.transaction.status)
        self.assertEqual("123", result.transaction.order_id)
        self.assertEqual("456*123456789012345678", result.transaction.descriptor.name)
        self.assertEqual("3334445555", result.transaction.descriptor.phone)
        self.assertEqual("ebay.com", result.transaction.descriptor.url)

    @raises_with_regexp(KeyError, "'Invalid keys: invalid_key'")
    def test_update_details_with_invalid_params(self):
        transaction = Transaction.sale({
            "amount": "10.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            },
        }).transaction

        params = {
            "amount" : "9.00",
            "invalid_key": "invalid_value",
            "order_id": "123",
            "descriptor": {
                "name": "456*123456789012345678",
                "phone": "3334445555",
                "url": "ebay.com"
            }
        }

        Transaction.update_details(transaction.id, params)

    def test_update_details_with_invalid_order_id(self):
        transaction = Transaction.sale({
            "amount": "10.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            },
        }).transaction

        params = {
            "amount" : "9.00",
            "order_id": "A" * 256,
            "descriptor": {
                "name": "456*123456789012345678",
                "phone": "3334445555",
                "url": "ebay.com"
            }
        }

        result = Transaction.update_details(transaction.id, params)
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.OrderIdIsTooLong,
            result.errors.for_object("transaction").on("order_id")[0].code
        )

    def test_update_details_with_invalid_descriptor(self):
        transaction = Transaction.sale({
            "amount": "10.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            },
        }).transaction

        params = {
            "amount" : "9.00",
            "order_id": "123",
            "descriptor": {
                "name": "invalid name",
                "phone": "invalid phone",
                "url": "12345678901234567890"
            }
        }

        result = Transaction.update_details(transaction.id, params)
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Descriptor.NameFormatIsInvalid,
            result.errors.for_object("transaction").for_object("descriptor").on("name")[0].code
        )
        self.assertEqual(
            ErrorCodes.Descriptor.PhoneFormatIsInvalid,
            result.errors.for_object("transaction").for_object("descriptor").on("phone")[0].code
        )
        self.assertEqual(
            ErrorCodes.Descriptor.UrlFormatIsInvalid,
            result.errors.for_object("transaction").for_object("descriptor").on("url")[0].code
        )

    def test_update_details_with_invalid_amount(self):
        transaction = Transaction.sale({
            "amount": "10.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            },
        }).transaction

        params = {
            "amount" : "999.00",
            "order_id": "123",
        }

        result = Transaction.update_details(transaction.id, params)
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.SettlementAmountIsTooLarge,
            result.errors.for_object("transaction").on("amount")[0].code
        )

    def test_update_details_with_invalid_status(self):
        transaction = Transaction.sale({
            "amount": "10.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
        }).transaction

        params = {
            "amount" : "9.00",
            "order_id": "123",
        }

        result = Transaction.update_details(transaction.id, params)
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.CannotUpdateTransactionDetailsNotSubmittedForSettlement,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_update_details_with_invalid_processor(self):
        transaction = Transaction.sale({
            "amount": "10.00",
            "merchant_account_id": TestHelper.fake_amex_direct_merchant_account_id,
            "credit_card": {
                "number": CreditCardNumbers.AmexPayWithPoints.Success,
                "expiration_date": "05/2020"
            },
            "options": {
                "submit_for_settlement": True
            },
        }).transaction

        params = {
            "amount" : "9.00",
            "order_id": "123",
        }

        result = Transaction.update_details(transaction.id, params)
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.ProcessorDoesNotSupportUpdatingTransactionDetails,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_status_history(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        submitted_transaction = Transaction.submit_for_settlement(transaction.id).transaction

        self.assertEqual(2, len(submitted_transaction.status_history))
        self.assertEqual(Transaction.Status.Authorized, submitted_transaction.status_history[0].status)
        self.assertEqual(Decimal(TransactionAmounts.Authorize), submitted_transaction.status_history[0].amount)
        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status_history[1].status)
        self.assertEqual(Decimal(TransactionAmounts.Authorize), submitted_transaction.status_history[1].amount)

    def test_successful_refund(self):
        transaction = self.__create_transaction_to_refund()

        result = Transaction.refund(transaction.id)

        self.assertTrue(result.is_success)
        refund = result.transaction

        self.assertEqual(Transaction.Type.Credit, refund.type)
        self.assertEqual(Decimal(TransactionAmounts.Authorize), refund.amount)
        self.assertEqual(transaction.id, refund.refunded_transaction_id)

        self.assertEqual(refund.id, Transaction.find(transaction.id).refund_id)

    def test_successful_partial_refund(self):
        transaction = self.__create_transaction_to_refund()

        result = Transaction.refund(transaction.id, Decimal("500.00"))

        self.assertTrue(result.is_success)
        self.assertEqual(Transaction.Type.Credit, result.transaction.type)
        self.assertEqual(Decimal("500.00"), result.transaction.amount)

    def test_multiple_successful_partial_refunds(self):
        transaction = self.__create_transaction_to_refund()

        refund1 = Transaction.refund(transaction.id, Decimal("500.00")).transaction
        self.assertEqual(Transaction.Type.Credit, refund1.type)
        self.assertEqual(Decimal("500.00"), refund1.amount)

        refund2 = Transaction.refund(transaction.id, Decimal("500.00")).transaction
        self.assertEqual(Transaction.Type.Credit, refund2.type)
        self.assertEqual(Decimal("500.00"), refund2.amount)

        transaction = Transaction.find(transaction.id)

        self.assertEqual(2, len(transaction.refund_ids))
        self.assertTrue(TestHelper.in_list(transaction.refund_ids, refund1.id))
        self.assertTrue(TestHelper.in_list(transaction.refund_ids, refund2.id))

    def test_refund_already_refunded_transation_fails(self):
        transaction = self.__create_transaction_to_refund()

        Transaction.refund(transaction.id)
        result = Transaction.refund(transaction.id)

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.HasAlreadyBeenRefunded,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_refund_with_options_params(self):
        transaction = self.__create_transaction_to_refund()
        options = {
            "amount": Decimal("1.00"),
            "order_id": "abcd"
        }
        result = Transaction.refund(transaction.id, options)

        self.assertTrue(result.is_success)
        self.assertEqual(
            "abcd",
            result.transaction.order_id
        )
        self.assertEqual(
            Decimal("1.00"),
            result.transaction.amount
        )

    def test_refund_returns_an_error_if_unsettled(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            }
        }).transaction

        result = Transaction.refund(transaction.id)

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.CannotRefundUnlessSettled,
            result.errors.for_object("transaction").on("base")[0].code
        )

    @staticmethod
    def __create_transaction_to_refund():
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            }
        }).transaction

        TestHelper.settle_transaction(transaction.id)
        return transaction

    @staticmethod
    def __create_paypal_transaction():
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "options": {
                "submit_for_settlement": True
            }
        }).transaction

        return transaction

    @staticmethod
    def __create_escrowed_transaction():
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            },
            "service_fee_amount": "10.00",
            "merchant_account_id": TestHelper.non_default_sub_merchant_account_id,
            "options": {
                "hold_in_escrow": True
            }
        }).transaction

        TestHelper.escrow_transaction(transaction.id)
        return transaction

    def test_snapshot_plan_id_add_ons_and_discounts_from_subscription(self):
        credit_card = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
            }
        }).customer.credit_cards[0]

        result = Subscription.create({
            "payment_method_token": credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "add_ons": {
                "add": [
                    {
                        "amount": Decimal("11.00"),
                        "inherited_from_id": "increase_10",
                        "quantity": 2,
                        "number_of_billing_cycles": 5
                    },
                    {
                        "amount": Decimal("21.00"),
                        "inherited_from_id": "increase_20",
                        "quantity": 3,
                        "number_of_billing_cycles": 6
                    }
                ]
            },
            "discounts": {
                "add": [
                    {
                        "amount": Decimal("7.50"),
                        "inherited_from_id": "discount_7",
                        "quantity": 2,
                        "never_expires": True
                    }
                ]
            }
        })

        transaction = result.subscription.transactions[0]

        self.assertEqual(TestHelper.trialless_plan["id"], transaction.plan_id)

        self.assertEqual(2, len(transaction.add_ons))
        add_ons = sorted(transaction.add_ons, key=lambda add_on: add_on.id)

        self.assertEqual("increase_10", add_ons[0].id)
        self.assertEqual(Decimal("11.00"), add_ons[0].amount)
        self.assertEqual(2, add_ons[0].quantity)
        self.assertEqual(5, add_ons[0].number_of_billing_cycles)
        self.assertFalse(add_ons[0].never_expires)

        self.assertEqual("increase_20", add_ons[1].id)
        self.assertEqual(Decimal("21.00"), add_ons[1].amount)
        self.assertEqual(3, add_ons[1].quantity)
        self.assertEqual(6, add_ons[1].number_of_billing_cycles)
        self.assertFalse(add_ons[1].never_expires)

        self.assertEqual(1, len(transaction.discounts))
        discounts = transaction.discounts

        self.assertEqual("discount_7", discounts[0].id)
        self.assertEqual(Decimal("7.50"), discounts[0].amount)
        self.assertEqual(2, discounts[0].quantity)
        self.assertEqual(None, discounts[0].number_of_billing_cycles)
        self.assertTrue(discounts[0].never_expires)


    def test_transactions_accept_lodging_industry_data(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "industry": {
                "industry_type": Transaction.IndustryType.Lodging,
                "data": {
                    "folio_number": "aaa",
                    "check_in_date": "2014-07-07",
                    "check_out_date": "2014-08-08",
                    "room_rate": "239.00",
                }
            }
        })

        self.assertTrue(result.is_success)

    def test_transactions_return_validation_errors_on_lodging_industry_data(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "industry": {
                "industry_type": Transaction.IndustryType.Lodging,
                "data": {
                    "folio_number": "aaa",
                    "check_in_date": "2014-07-07",
                    "check_out_date": "2014-06-06",
                    "room_rate": "asdfsdf",
                }
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.Industry.Lodging.CheckOutDateMustFollowCheckInDate,
            result.errors.for_object("transaction").for_object("industry").on("check_out_date")[0].code
        )

    def test_transactions_accept_travel_cruise_industry_data(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "industry": {
                "industry_type": Transaction.IndustryType.TravelAndCruise,
                "data": {
                    "travel_package": "flight",
                    "departure_date": "2014-07-07",
                    "lodging_check_in_date": "2014-07-07",
                    "lodging_check_out_date": "2014-09-07",
                    "lodging_name": "Royal Caribbean"
                }
            }
        })

        self.assertTrue(result.is_success)

    def test_transactions_return_validation_errors_on_travel_cruise_industry_data(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "industry": {
                "industry_type": Transaction.IndustryType.TravelAndCruise,
                "data": {
                    "travel_package": "roadtrip",
                    "departure_date": "2014-07-07",
                    "lodging_check_in_date": "2014-07-07",
                    "lodging_check_out_date": "2014-09-07",
                    "lodging_name": "Royal Caribbean"
                }
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.Industry.TravelCruise.TravelPackageIsInvalid,
            result.errors.for_object("transaction").for_object("industry").on("travel_package")[0].code
        )

    def test_descriptors_accepts_name_phone_and_url(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "descriptor": {
                "name": "123*123456789012345678",
                "phone": "3334445555",
                "url": "ebay.com"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual("123*123456789012345678", transaction.descriptor.name)
        self.assertEqual("3334445555", transaction.descriptor.phone)
        self.assertEqual("ebay.com", transaction.descriptor.url)

    def test_descriptors_has_validation_errors_if_format_is_invalid(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "descriptor": {
                "name": "badcompanyname12*badproduct12",
                "phone": "%bad4445555",
                "url": "12345678901234"
            }
        })
        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Descriptor.NameFormatIsInvalid,
            result.errors.for_object("transaction").for_object("descriptor").on("name")[0].code
        )
        self.assertEqual(
            ErrorCodes.Descriptor.PhoneFormatIsInvalid,
            result.errors.for_object("transaction").for_object("descriptor").on("phone")[0].code
        )
        self.assertEqual(
            ErrorCodes.Descriptor.UrlFormatIsInvalid,
            result.errors.for_object("transaction").for_object("descriptor").on("url")[0].code
        )

    def test_clone_transaction(self):
        result = Transaction.sale({
            "amount": "100.00",
            "order_id": "123",
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2011",
            },
            "customer": {
                "first_name": "Dan",
            },
            "billing": {
                "first_name": "Carl",
            },
            "shipping": {
                "first_name": "Andrew",
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        clone_result = Transaction.clone_transaction(
                transaction.id,
                {
                    "amount": "123.45",
                    "channel": "MyShoppingCartProvider",
                    "options": {"submit_for_settlement": "false"}
                })
        self.assertTrue(clone_result.is_success)
        clone_transaction = clone_result.transaction

        self.assertNotEqual(transaction.id, clone_transaction.id)

        self.assertEqual(Transaction.Type.Sale, clone_transaction.type)
        self.assertEqual(Transaction.Status.Authorized, clone_transaction.status)
        self.assertEqual(Decimal("123.45"), clone_transaction.amount)
        self.assertEqual("MyShoppingCartProvider", clone_transaction.channel)
        self.assertEqual("123", clone_transaction.order_id)
        self.assertEqual("510510******5100", clone_transaction.credit_card_details.masked_number)
        self.assertEqual("Dan", clone_transaction.customer_details.first_name)
        self.assertEqual("Carl", clone_transaction.billing_details.first_name)
        self.assertEqual("Andrew", clone_transaction.shipping_details.first_name)

    def test_clone_transaction_submits_for_settlement(self):
        result = Transaction.sale({
            "amount": "100.00",
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2011",
            }
        })
        self.assertTrue(result.is_success)
        transaction = result.transaction

        clone_result = Transaction.clone_transaction(transaction.id, {"amount": "123.45", "options": {"submit_for_settlement": "true"}})
        self.assertTrue(clone_result.is_success)
        clone_transaction = clone_result.transaction

        self.assertEqual(Transaction.Type.Sale, clone_transaction.type)
        self.assertEqual(Transaction.Status.SubmittedForSettlement, clone_transaction.status)

    def test_clone_transaction_with_validations(self):
        result = Transaction.credit({
            "amount": "100.00",
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2011",
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        clone_result = Transaction.clone_transaction(transaction.id, {"amount": "123.45"})
        self.assertFalse(clone_result.is_success)

        self.assertEqual(
            ErrorCodes.Transaction.CannotCloneCredit,
            clone_result.errors.for_object("transaction").on("base")[0].code
        )

    def test_find_exposes_disbursement_details(self):
        transaction = Transaction.find("deposittransaction")
        disbursement_details = transaction.disbursement_details

        self.assertEqual(date(2013, 4, 10), disbursement_details.disbursement_date)
        self.assertEqual("USD", disbursement_details.settlement_currency_iso_code)
        self.assertEqual(Decimal("1"), disbursement_details.settlement_currency_exchange_rate)
        self.assertEqual(False, disbursement_details.funds_held)
        self.assertEqual(True, disbursement_details.success)
        self.assertEqual(Decimal("100.00"), disbursement_details.settlement_amount)

    def test_sale_with_three_d_secure_option(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.three_d_secure_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "three_d_secure": {
                    "required": True
                }
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(Transaction.Status.GatewayRejected, result.transaction.status)
        self.assertEqual(Transaction.GatewayRejectionReason.ThreeDSecure, result.transaction.gateway_rejection_reason)

    def test_sale_with_three_d_secure_token(self):
        three_d_secure_token = TestHelper.create_3ds_verification(TestHelper.three_d_secure_merchant_account_id, {
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2009",
        })

        result = Transaction.sale({
            "merchant_account_id": TestHelper.three_d_secure_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "three_d_secure_token": three_d_secure_token
        })

        self.assertTrue(result.is_success)

    def test_sale_without_three_d_secure_token(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.three_d_secure_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)

    def test_sale_returns_error_with_none_three_d_secure_token(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.three_d_secure_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "three_d_secure_token": None
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.ThreeDSecureTokenIsInvalid,
            result.errors.for_object("transaction").on("three_d_secure_token")[0].code
        )

    def test_sale_returns_error_with_mismatched_3ds_verification_data(self):
        three_d_secure_token = TestHelper.create_3ds_verification(TestHelper.three_d_secure_merchant_account_id, {
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2009",
        })

        result = Transaction.sale({
            "merchant_account_id": TestHelper.three_d_secure_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "5105105105105100",
                "expiration_date": "05/2009"
            },
            "three_d_secure_token": three_d_secure_token
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.ThreeDSecureTransactionDataDoesntMatchVerify,
            result.errors.for_object("transaction").on("three_d_secure_token")[0].code
        )

    def test_transaction_with_three_d_secure_pass_thru(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.three_d_secure_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "three_d_secure_pass_thru": {
                "eci_flag": "02",
                "cavv": "some-cavv",
                "xid": "some-xid"
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual(Transaction.Status.Authorized, result.transaction.status)

    def test_transaction_with_three_d_secure_pass_thru_with_invalid_processor_settings(self):
        result = Transaction.sale({
            "merchant_account_id": "adyen_ma",
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "three_d_secure_pass_thru": {
                "eci_flag": "02",
                "cavv": "some-cavv",
                "xid": "some-xid"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.ThreeDSecureMerchantAccountDoesNotSupportCardType,
            result.errors.for_object("transaction").on("merchant_account_id")[0].code
        )

    def test_transaction_with_three_d_secure_pass_thru_with_missing_eci_flag(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.three_d_secure_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "three_d_secure_pass_thru": {
                "eci_flag": "",
                "cavv": "some-cavv",
                "xid": "some-xid"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.ThreeDSecureEciFlagIsRequired,
            result.errors.for_object("transaction").for_object("three_d_secure_pass_thru").on("eci_flag")[0].code
        )


    def test_transaction_with_three_d_secure_pass_thru_with_missing_cavv_and_xid(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.three_d_secure_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "three_d_secure_pass_thru": {
                "eci_flag": "05",
                "cavv": "",
                "xid": ""
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.ThreeDSecureCavvIsRequired,
            result.errors.for_object("transaction").for_object("three_d_secure_pass_thru").on("cavv")[0].code
        )

    def test_transaction_with_three_d_secure_pass_thru_with_invalid_eci_flag(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.three_d_secure_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "three_d_secure_pass_thru": {
                "eci_flag": "bad_eci_flag",
                "cavv": "some-cavv",
                "xid": "some-xid"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.ThreeDSecureEciFlagIsInvalid,
            result.errors.for_object("transaction").for_object("three_d_secure_pass_thru").on("eci_flag")[0].code
        )


    def test_sale_with_amex_rewards_succeeds(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.fake_amex_direct_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.AmexPayWithPoints.Success,
                "expiration_date": "05/2020"
            },
            "options" : {
                "submit_for_settlement" : True,
                "amex_rewards" : {
                    "request_id" : "ABC123",
                    "points" : "100",
                    "currency_amount" : "1.00",
                    "currency_iso_code" : "USD"
                }
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual(Transaction.Status.SubmittedForSettlement, transaction.status)

    def test_sale_with_amex_rewards_succeeds_even_if_card_is_ineligible(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.fake_amex_direct_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.AmexPayWithPoints.IneligibleCard,
                "expiration_date": "05/2009"
            },
            "options" : {
                "submit_for_settlement" : True,
                "amex_rewards" : {
                    "request_id" : "ABC123",
                    "points" : "100",
                    "currency_amount" : "1.00",
                    "currency_iso_code" : "USD"
                }
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual(Transaction.Status.SubmittedForSettlement, transaction.status)

    def test_sale_with_amex_rewards_succeeds_even_if_card_balance_is_insufficient(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.fake_amex_direct_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.AmexPayWithPoints.InsufficientPoints,
                "expiration_date": "05/2009"
            },
            "options" : {
                "submit_for_settlement" : True,
                "amex_rewards" : {
                    "request_id" : "ABC123",
                    "points" : "100",
                    "currency_amount" : "1.00",
                    "currency_iso_code" : "USD"
                }
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual(Transaction.Status.SubmittedForSettlement, transaction.status)

    def test_submit_for_settlement_with_amex_rewards_succeeds(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.fake_amex_direct_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.AmexPayWithPoints.Success,
                "expiration_date": "05/2009"
            },
            "options" : {
                "amex_rewards" : {
                    "request_id" : "ABC123",
                    "points" : "100",
                    "currency_amount" : "1.00",
                    "currency_iso_code" : "USD"
                }
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual(Transaction.Status.Authorized, transaction.status)

        submitted_transaction = Transaction.submit_for_settlement(transaction.id).transaction
        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)

    def test_submit_for_settlement_with_amex_rewards_succeeds_even_if_card_is_ineligible(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.fake_amex_direct_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.AmexPayWithPoints.IneligibleCard,
                "expiration_date": "05/2009"
            },
            "options" : {
                "amex_rewards" : {
                    "request_id" : "ABC123",
                    "points" : "100",
                    "currency_amount" : "1.00",
                    "currency_iso_code" : "USD"
                }
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual(Transaction.Status.Authorized, transaction.status)

        submitted_transaction = Transaction.submit_for_settlement(transaction.id).transaction
        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)

    def test_submit_for_settlement_with_amex_rewards_succeeds_even_if_card_balance_is_insufficient(self):
        result = Transaction.sale({
            "merchant_account_id": TestHelper.fake_amex_direct_merchant_account_id,
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": CreditCardNumbers.AmexPayWithPoints.InsufficientPoints,
                "expiration_date": "05/2009"
            },
            "options" : {
                "amex_rewards" : {
                    "request_id" : "ABC123",
                    "points" : "100",
                    "currency_amount" : "1.00",
                    "currency_iso_code" : "USD"
                }
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(Transaction.Type.Sale, transaction.type)
        self.assertEqual(Transaction.Status.Authorized, transaction.status)

        submitted_transaction = Transaction.submit_for_settlement(transaction.id).transaction
        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)

    def test_find_exposes_authorization_adjustments(self):
        transaction = Transaction.find("authadjustmenttransaction")
        authorization_adjustment = transaction.authorization_adjustments[0]

        self.assertEqual(datetime, type(authorization_adjustment.timestamp))
        self.assertEqual(Decimal("-20.00"), authorization_adjustment.amount)
        self.assertEqual(True, authorization_adjustment.success)

    def test_find_exposes_disputes(self):
        transaction = Transaction.find("disputedtransaction")
        dispute = transaction.disputes[0]

        self.assertEqual(date(2014, 3, 1), dispute.received_date)
        self.assertEqual(date(2014, 3, 21), dispute.reply_by_date)
        self.assertEqual("USD", dispute.currency_iso_code)
        self.assertEqual(Decimal("250.00"), dispute.amount)
        self.assertEqual(Dispute.Status.Won, dispute.status)
        self.assertEqual(Dispute.Reason.Fraud, dispute.reason)
        self.assertEqual("disputedtransaction", dispute.transaction_details.id)
        self.assertEqual(Decimal("1000.00"), dispute.transaction_details.amount)
        self.assertEqual(Dispute.Kind.Chargeback, dispute.kind)
        self.assertEqual(date(2014, 3, 1), dispute.date_opened)
        self.assertEqual(date(2014, 3, 7), dispute.date_won)

    def test_find_exposes_three_d_secure_info(self):
        transaction = Transaction.find("threedsecuredtransaction")
        three_d_secure_info = transaction.three_d_secure_info

        self.assertEqual("Y", three_d_secure_info.enrolled)
        self.assertEqual("authenticate_successful", three_d_secure_info.status)
        self.assertEqual(True, three_d_secure_info.liability_shifted)
        self.assertEqual(True, three_d_secure_info.liability_shift_possible)

    def test_find_exposes_none_for_null_three_d_secure_info(self):
        transaction = Transaction.find("settledtransaction")
        three_d_secure_info = transaction.three_d_secure_info

        self.assertEqual(None, three_d_secure_info)

    def test_find_exposes_retrievals(self):
        transaction = Transaction.find("retrievaltransaction")
        dispute = transaction.disputes[0]

        self.assertEqual("USD", dispute.currency_iso_code)
        self.assertEqual(Decimal("1000.00"), dispute.amount)
        self.assertEqual(Dispute.Status.Open, dispute.status)
        self.assertEqual(Dispute.Reason.Retrieval, dispute.reason)
        self.assertEqual("retrievaltransaction", dispute.transaction_details.id)
        self.assertEqual(Decimal("1000.00"), dispute.transaction_details.amount)

    def test_creating_paypal_transaction_with_one_time_use_nonce(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        self.assertEqual(transaction.paypal_details.payer_email, "payer@example.com")
        self.assertNotEqual(None, re.search(r'PAY-\w+', transaction.paypal_details.payment_id))
        self.assertNotEqual(None, re.search(r'AUTH-\w+', transaction.paypal_details.authorization_id))
        self.assertNotEqual(None, transaction.paypal_details.image_url)
        self.assertNotEqual(None, transaction.paypal_details.debug_id)

    def test_creating_paypal_transaction_with_payee_email(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "paypal_account": {
                "payee_email": "payee@example.com"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        self.assertEqual(transaction.paypal_details.payer_email, "payer@example.com")
        self.assertNotEqual(None, re.search(r'PAY-\w+', transaction.paypal_details.payment_id))
        self.assertNotEqual(None, re.search(r'AUTH-\w+', transaction.paypal_details.authorization_id))
        self.assertNotEqual(None, transaction.paypal_details.image_url)
        self.assertNotEqual(None, transaction.paypal_details.debug_id)
        self.assertEqual(transaction.paypal_details.payee_email, "payee@example.com")

    def test_creating_paypal_transaction_with_payee_email_in_options_params(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "paypal_account": {},
            "options": {
                "payee_email": "payee@example.com"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        self.assertEqual(transaction.paypal_details.payer_email, "payer@example.com")
        self.assertNotEqual(None, re.search(r'PAY-\w+', transaction.paypal_details.payment_id))
        self.assertNotEqual(None, re.search(r'AUTH-\w+', transaction.paypal_details.authorization_id))
        self.assertNotEqual(None, transaction.paypal_details.image_url)
        self.assertNotEqual(None, transaction.paypal_details.debug_id)
        self.assertEqual(transaction.paypal_details.payee_email, "payee@example.com")

    def test_creating_paypal_transaction_with_payee_email_in_options_paypal_params(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "paypal_account": {},
            "options": {
                "paypal": {
                    "payee_email": "foo@paypal.com"
                }
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        self.assertEqual(transaction.paypal_details.payer_email, "payer@example.com")
        self.assertNotEqual(None, re.search(r'PAY-\w+', transaction.paypal_details.payment_id))
        self.assertNotEqual(None, re.search(r'AUTH-\w+', transaction.paypal_details.authorization_id))
        self.assertNotEqual(None, transaction.paypal_details.image_url)
        self.assertNotEqual(None, transaction.paypal_details.debug_id)
        self.assertEqual(transaction.paypal_details.payee_email, "foo@paypal.com")

    def test_creating_paypal_transaction_with_custom_field_in_options_paypal_params(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "paypal_account": {},
            "options": {
                "paypal": {
                    "custom_field": "custom field stuff"
                }
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        self.assertEqual(transaction.paypal_details.payer_email, "payer@example.com")
        self.assertNotEqual(None, re.search(r'PAY-\w+', transaction.paypal_details.payment_id))
        self.assertNotEqual(None, re.search(r'AUTH-\w+', transaction.paypal_details.authorization_id))
        self.assertNotEqual(None, transaction.paypal_details.image_url)
        self.assertNotEqual(None, transaction.paypal_details.debug_id)
        self.assertEqual(transaction.paypal_details.custom_field, "custom field stuff")

    def test_creating_paypal_transaction_with_supplementary_data_in_options_paypal_params(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "paypal_account": {},
            "options": {
                "paypal": {
                    "supplementary_data": {
                        "key1": "value1",
                        "key2": "value2"
                    }
                }
            }
        })

        # note - supplementary data is not returned in response
        self.assertTrue(result.is_success)

    def test_creating_paypal_transaction_with_description_in_options_paypal_params(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "paypal_account": {},
            "options": {
                "paypal": {
                    "description": "Product description"
                }
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        self.assertEqual(transaction.paypal_details.payer_email, "payer@example.com")
        self.assertNotEqual(None, re.search(r'PAY-\w+', transaction.paypal_details.payment_id))
        self.assertNotEqual(None, re.search(r'AUTH-\w+', transaction.paypal_details.authorization_id))
        self.assertNotEqual(None, transaction.paypal_details.image_url)
        self.assertNotEqual(None, transaction.paypal_details.debug_id)
        self.assertEqual(transaction.paypal_details.description, "Product description")

    def test_paypal_transaction_payment_instrument_type(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
        })

        self.assertTrue(result.is_success)

        transaction = result.transaction
        self.assertEqual(PaymentInstrumentType.PayPalAccount, transaction.payment_instrument_type)

    def test_creating_paypal_transaction_with_one_time_use_nonce_and_store_in_vault(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "options": {"store_in_vault": True}
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        self.assertEqual(transaction.paypal_details.payer_email, "payer@example.com")
        self.assertEqual(transaction.paypal_details.token, None)
        self.assertNotEqual(None, transaction.paypal_details.debug_id)

    def test_creating_paypal_transaction_with_future_payment_nonce(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalFuturePayment
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        self.assertEqual(transaction.paypal_details.payer_email, "payer@example.com")
        self.assertNotEqual(None, re.search(r'PAY-\w+', transaction.paypal_details.payment_id))
        self.assertNotEqual(None, re.search(r'AUTH-\w+', transaction.paypal_details.authorization_id))
        self.assertNotEqual(None, transaction.paypal_details.debug_id)

    def test_validation_failure_on_invalid_paypal_nonce(self):
        http = ClientApiHttp.create()

        status_code, nonce = http.get_paypal_nonce({
            "consent-code": "consent-code",
            "access-token": "access-token",
            "options": {"validate": False}
        })
        self.assertEqual(202, status_code)

        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": nonce
        })

        self.assertFalse(result.is_success)
        error_code = result.errors.for_object("transaction").for_object("paypal_account").on("base")[0].code
        self.assertEqual(error_code, ErrorCodes.PayPalAccount.CannotHaveBothAccessTokenAndConsentCode)

    def test_validation_failure_on_non_existent_nonce(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": "doesnt-exist"
        })

        self.assertFalse(result.is_success)
        error_code = result.errors.for_object("transaction").on("payment_method_nonce")[0].code
        self.assertEqual(error_code, ErrorCodes.Transaction.PaymentMethodNonceUnknown)

    def test_creating_paypal_transaction_with_vaulted_token(self):
        customer_id = Customer.create().customer.id

        result = PaymentMethod.create({
            "customer_id": customer_id,
            "payment_method_nonce": Nonces.PayPalFuturePayment
        })

        self.assertTrue(result.is_success)

        transaction_result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_token": result.payment_method.token
        })

        self.assertTrue(transaction_result.is_success)
        transaction = transaction_result.transaction

        self.assertEqual(transaction.paypal_details.payer_email, "payer@example.com")
        self.assertNotEqual(None, transaction.paypal_details.debug_id)

    def test_creating_paypal_transaction_with_one_time_nonce_and_store_in_vault_fails_gracefully(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "options": {"store_in_vault": True}
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEqual(None, transaction.paypal_details.token)

    def test_creating_paypal_transaction_with_future_payment_nonce_and_store_in_vault(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalFuturePayment,
            "options": {"store_in_vault": True}
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        self.assertNotEqual(None, transaction.paypal_details.token)
        paypal_account = PaymentMethod.find(transaction.paypal_details.token)
        self.assertEqual(paypal_account.email, transaction.paypal_details.payer_email)

    def test_creating_paypal_transaction_and_submitting_for_settlement(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "options": {"submit_for_settlement": True}
        })

        self.assertTrue(result.is_success)
        self.assertEqual(result.transaction.status, Transaction.Status.Settling)

    def test_voiding_a_paypal_transaction(self):
        sale_result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
        })
        self.assertTrue(sale_result.is_success)
        sale_transaction = sale_result.transaction

        void_result = Transaction.void(sale_transaction.id)
        self.assertTrue(void_result.is_success)

        void_transaction = void_result.transaction
        self.assertEqual(void_transaction.id, sale_transaction.id)
        self.assertEqual(void_transaction.status, Transaction.Status.Voided)

    def test_paypal_transaction_successful_refund(self):
        transaction = self.__create_paypal_transaction()

        result = Transaction.refund(transaction.id)

        self.assertTrue(result.is_success)
        refund = result.transaction

        self.assertEqual(Transaction.Type.Credit, refund.type)
        self.assertEqual(Decimal(TransactionAmounts.Authorize), refund.amount)
        self.assertEqual(transaction.id, refund.refunded_transaction_id)

        self.assertEqual(refund.id, Transaction.find(transaction.id).refund_id)

    def test_paypal_transaction_successful_partial_refund(self):
        transaction = self.__create_paypal_transaction()

        result = Transaction.refund(transaction.id, Decimal("500.00"))

        self.assertTrue(result.is_success)
        self.assertEqual(Transaction.Type.Credit, result.transaction.type)
        self.assertEqual(Decimal("500.00"), result.transaction.amount)

    def test_paypal_transaction_multiple_successful_partial_refunds(self):
        transaction = self.__create_paypal_transaction()

        refund1 = Transaction.refund(transaction.id, Decimal("500.00")).transaction
        self.assertEqual(Transaction.Type.Credit, refund1.type)
        self.assertEqual(Decimal("500.00"), refund1.amount)

        refund2 = Transaction.refund(transaction.id, Decimal("500.00")).transaction
        self.assertEqual(Transaction.Type.Credit, refund2.type)
        self.assertEqual(Decimal("500.00"), refund2.amount)

        transaction = Transaction.find(transaction.id)

        self.assertEqual(2, len(transaction.refund_ids))
        self.assertTrue(TestHelper.in_list(transaction.refund_ids, refund1.id))
        self.assertTrue(TestHelper.in_list(transaction.refund_ids, refund2.id))

    def test_paypal_transaction_returns_required_fields(self):
        transaction = self.__create_paypal_transaction()

        self.assertNotEqual(None, transaction.paypal_details.debug_id)
        self.assertNotEqual(None, transaction.paypal_details.payer_email)
        self.assertNotEqual(None, transaction.paypal_details.authorization_id)
        self.assertNotEqual(None, transaction.paypal_details.payer_id)
        self.assertNotEqual(None, transaction.paypal_details.payer_first_name)
        self.assertNotEqual(None, transaction.paypal_details.payer_last_name)
        self.assertNotEqual(None, transaction.paypal_details.payer_status)
        self.assertNotEqual(None, transaction.paypal_details.seller_protection_status)
        self.assertNotEqual(None, transaction.paypal_details.capture_id)
        #self.assertNotEqual(None, transaction.paypal_details.refund_id)
        self.assertNotEqual(None, transaction.paypal_details.transaction_fee_amount)
        self.assertNotEqual(None, transaction.paypal_details.transaction_fee_currency_iso_code)

    def test_paypal_transaction_refund_already_refunded_transation_fails(self):
        transaction = self.__create_paypal_transaction()

        Transaction.refund(transaction.id)
        result = Transaction.refund(transaction.id)

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.HasAlreadyBeenRefunded,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_paypal_transaction_refund_returns_an_error_if_unsettled(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            }
        }).transaction

        result = Transaction.refund(transaction.id)

        self.assertFalse(result.is_success)
        self.assertEqual(
            ErrorCodes.Transaction.CannotRefundUnlessSettled,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def test_transaction_settlement_errors(self):
        sale_result = Transaction.sale({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
            },
            "amount": "100.00",
        })
        transaction = sale_result.transaction

        settle_result = TestHelper.settle_transaction(transaction.id)
        self.assertFalse(settle_result.is_success)

        error_codes = [
            error.code for error in settle_result.errors.for_object("transaction").on("base")
        ]
        self.assertTrue(ErrorCodes.Transaction.CannotSimulateTransactionSettlement in error_codes)

    def test_transaction_returns_settlement_declined_response(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "options": {"submit_for_settlement": True}
        })
        self.assertTrue(result.is_success)
        TestHelper.settlement_decline_transaction(result.transaction.id)

        transaction = Transaction.find(result.transaction.id)

        self.assertTrue("4001", transaction.processor_settlement_response_code)
        self.assertTrue("Settlement Declined", transaction.processor_settlement_response_text)
        self.assertTrue(Transaction.Status.SettlementDeclined, transaction.status)

    def test_transaction_returns_settlement_pending_response(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "options": {"submit_for_settlement": True}
        })
        self.assertTrue(result.is_success)
        TestHelper.settlement_pending_transaction(result.transaction.id)

        transaction = Transaction.find(result.transaction.id)

        self.assertTrue("4002", transaction.processor_settlement_response_code)
        self.assertTrue("Settlement Pending", transaction.processor_settlement_response_text)
        self.assertTrue(Transaction.Status.SettlementPending, transaction.status)

    def test_transaction_submit_for_partial_settlement(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertTrue(result.is_success)
        authorized_transaction = result.transaction

        partial_settlement_result = Transaction.submit_for_partial_settlement(authorized_transaction.id, Decimal("500.00"))
        partial_settlement_transaction = partial_settlement_result.transaction
        self.assertTrue(partial_settlement_result.is_success)
        self.assertEqual(partial_settlement_transaction.amount, Decimal("500.00"))
        self.assertEqual(Transaction.Type.Sale, partial_settlement_transaction.type)
        self.assertEqual(Transaction.Status.SubmittedForSettlement, partial_settlement_transaction.status)
        self.assertEqual(authorized_transaction.id, partial_settlement_transaction.authorized_transaction_id)

        partial_settlement_result_2 = Transaction.submit_for_partial_settlement(authorized_transaction.id, Decimal("500.00"))
        partial_settlement_transaction_2 = partial_settlement_result_2.transaction
        self.assertTrue(partial_settlement_result_2.is_success)
        self.assertEqual(partial_settlement_transaction_2.amount, Decimal("500.00"))
        self.assertEqual(Transaction.Type.Sale, partial_settlement_transaction_2.type)
        self.assertEqual(Transaction.Status.SubmittedForSettlement, partial_settlement_transaction_2.status)
        self.assertEqual(authorized_transaction.id, partial_settlement_transaction_2.authorized_transaction_id)

        refreshed_authorized_transaction = Transaction.find(authorized_transaction.id)
        self.assertEqual(2, len(refreshed_authorized_transaction.partial_settlement_transaction_ids))

    def test_transaction_submit_for_partial_settlement_unsuccessful(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })
        self.assertTrue(result.is_success)
        authorized_transaction = result.transaction

        partial_settlement_result = Transaction.submit_for_partial_settlement(authorized_transaction.id, Decimal("500.00"))
        partial_settlement_transaction = partial_settlement_result.transaction

        partial_settlement_result_2 = Transaction.submit_for_partial_settlement(partial_settlement_transaction.id, Decimal("250.00"))
        self.assertFalse(partial_settlement_result_2.is_success)
        error_code = partial_settlement_result_2.errors.for_object("transaction").on("base")[0].code
        self.assertEqual(ErrorCodes.Transaction.CannotSubmitForPartialSettlement, error_code)

    def test_submit_for_partial_settlement_with_order_id(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        params = {"order_id": "ABC123"}

        submitted_transaction = Transaction.submit_for_partial_settlement(transaction.id, Decimal("900"), params).transaction

        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)
        self.assertEqual("ABC123", submitted_transaction.order_id)

    def test_submit_for_partial_settlement_with_descriptor(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        params = {
            "descriptor": {
                "name": "123*123456789012345678",
                "phone": "3334445555",
                "url": "ebay.com"
            }
        }

        submitted_transaction = Transaction.submit_for_partial_settlement(transaction.id, Decimal("900"), params).transaction

        self.assertEqual(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)
        self.assertEqual("123*123456789012345678", submitted_transaction.descriptor.name)
        self.assertEqual("3334445555", submitted_transaction.descriptor.phone)
        self.assertEqual("ebay.com", submitted_transaction.descriptor.url)

    @raises_with_regexp(KeyError, "'Invalid keys: invalid_param'")
    def test_submit_for_partial_settlement_with_invalid_params(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        params = {
            "descriptor": {
                "name": "123*123456789012345678",
                "phone": "3334445555",
                "url": "ebay.com"
            },
            "invalid_param": "foo",
        }

        Transaction.submit_for_partial_settlement(transaction.id, Decimal("900"), params)

    def test_facilitated_transaction(self):
        granting_gateway, credit_card = TestHelper.create_payment_method_grant_fixtures()
        grant_result = granting_gateway.payment_method.grant(credit_card.token, False)
        nonce = grant_result.payment_method_nonce.nonce

        result = Transaction.sale({
            "payment_method_nonce": nonce,
            "amount": TransactionAmounts.Authorize,
        })
        self.assertNotEqual(result.transaction.facilitated_details, None)
        self.assertEqual(result.transaction.facilitated_details.merchant_id, "integration_merchant_id")
        self.assertEqual(result.transaction.facilitated_details.merchant_name, "14ladders")
        self.assertEqual(result.transaction.facilitated_details.payment_method_nonce, nonce)
        self.assertTrue(result.transaction.facilitator_details is not None)
        self.assertEqual(result.transaction.facilitator_details.oauth_application_client_id, "client_id$development$integration_client_id")
        self.assertEqual(result.transaction.facilitator_details.oauth_application_name, "PseudoShop")
        self.assertTrue(result.transaction.billing["postal_code"] is None)

    def test_include_billing_postal_code(self):
        granting_gateway, credit_card = TestHelper.create_payment_method_grant_fixtures()
        grant_result = granting_gateway.payment_method.grant(credit_card.token, { "allow_vaulting": False, "include_billing_postal_code": True })

        result = Transaction.sale({
            "payment_method_nonce": grant_result.payment_method_nonce.nonce,
            "amount": TransactionAmounts.Authorize,
        })

        self.assertTrue(result.transaction.billing["postal_code"], "95131")

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

    def test_sale_transacts_ideal_payment(self):
        valid_id = TestHelper.generate_valid_ideal_payment_id()
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "order_id": "ABC123",
            "merchant_account_id": "ideal_merchant_account",
            "payment_method_nonce": valid_id,
            "options": {
                "submit_for_settlement": True,
            },
        })

        self.assertTrue(result.is_success)

        self.assertRegexpMatches(result.transaction.id, r'^\w{6,}$')
        self.assertEqual(result.transaction.type, "sale")
        self.assertEqual(result.transaction.payment_instrument_type, PaymentInstrumentType.IdealPayment)
        self.assertEqual(result.transaction.amount, Decimal(TransactionAmounts.Authorize))
        self.assertEqual(result.transaction.status, Transaction.Status.Settled)
        self.assertRegexpMatches(result.transaction.ideal_payment_details.ideal_payment_id, r"^idealpayment_\w{6,}")
        self.assertRegexpMatches(result.transaction.ideal_payment_details.ideal_transaction_id, r"^\d{16,}$")
        self.assertEqual(result.transaction.ideal_payment_details.image_url[:8], 'https://')
        self.assertNotEqual(result.transaction.ideal_payment_details.masked_iban, None)
        self.assertNotEqual(result.transaction.ideal_payment_details.bic, None)

    def test_failed_sale_non_complete_ideal_payment(self):
        non_complete_id = TestHelper.generate_valid_ideal_payment_id("3.00")
        result = Transaction.sale({
            "amount": "3.00",
            "order_id": "ABC123",
            "merchant_account_id": "ideal_merchant_account",
            "payment_method_nonce": non_complete_id,
            "options": {
                "submit_for_settlement": True,
            },
        })
        error_codes = [
            error.code for error in result.errors.for_object("transaction").on("payment_method_nonce")
        ]

        self.assertFalse(result.is_success)
        self.assertTrue(ErrorCodes.Transaction.IdealPaymentNotComplete in error_codes)
