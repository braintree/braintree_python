from tests.test_helper import *

class TestTransaction(unittest.TestCase):
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
        self.assertNotEqual(None, re.search("\A\w{6}\Z", transaction.id))
        self.assertEquals(Transaction.Type.Sale, transaction.type)
        self.assertEquals(Decimal(TransactionAmounts.Authorize), transaction.amount)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2009", transaction.credit_card_details.expiration_date)

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
        self.assertNotEqual(None, re.search("\A\w{6}\Z", transaction.id))
        self.assertEquals(Transaction.Type.Sale, transaction.type)
        self.assertEquals(Decimal(TransactionAmounts.Authorize), transaction.amount)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2009", transaction.credit_card_details.expiration_date)

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
        self.assertEquals(Transaction.Type.Sale, transaction.type)
        self.assertEquals("05", transaction.credit_card_details.expiration_month)
        self.assertEquals("2012", transaction.credit_card_details.expiration_year)

    def test_sale_works_with_all_attributes(self):
        result = Transaction.sale({
            "amount": "100.00",
            "order_id": "123",
            "credit_card": {
                "cardholder_name": "The Cardholder",
                "number": "5105105105105100",
                "expiration_date": "05/2011",
                "cvv": "123"
            },
            "customer": {
                "first_name": "Dan",
                "last_name": "Smith",
                "company": "Braintree Payment Solutions",
                "email": "dan@example.com",
                "phone": "419-555-1234",
                "fax": "419-555-1235",
                "website": "http://braintreepaymentsolutions.com"
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
        self.assertNotEquals(None, re.search("\A\w{6}\Z", transaction.id))
        self.assertEquals(Transaction.Type.Sale, transaction.type)
        self.assertEquals(Transaction.Status.Authorized, transaction.status)
        self.assertEquals(Decimal("100.00"), transaction.amount)
        self.assertEquals("123", transaction.order_id)
        self.assertEquals("1000", transaction.processor_response_code)
        self.assertEquals(datetime, type(transaction.created_at))
        self.assertEquals(datetime, type(transaction.updated_at))
        self.assertEquals("510510", transaction.credit_card_details.bin)
        self.assertEquals("5100", transaction.credit_card_details.last_4)
        self.assertEquals("510510******5100", transaction.credit_card_details.masked_number)
        self.assertEquals("MasterCard", transaction.credit_card_details.card_type)
        self.assertEquals("The Cardholder", transaction.credit_card_details.cardholder_name)
        self.assertEquals(None, transaction.avs_error_response_code)
        self.assertEquals("M", transaction.avs_postal_code_response_code)
        self.assertEquals("M", transaction.avs_street_address_response_code)
        self.assertEquals("Dan", transaction.customer_details.first_name)
        self.assertEquals("Smith", transaction.customer_details.last_name)
        self.assertEquals("Braintree Payment Solutions", transaction.customer_details.company)
        self.assertEquals("dan@example.com", transaction.customer_details.email)
        self.assertEquals("419-555-1234", transaction.customer_details.phone)
        self.assertEquals("419-555-1235", transaction.customer_details.fax)
        self.assertEquals("http://braintreepaymentsolutions.com", transaction.customer_details.website)
        self.assertEquals("Carl", transaction.billing_details.first_name)
        self.assertEquals("Jones", transaction.billing_details.last_name)
        self.assertEquals("Braintree", transaction.billing_details.company)
        self.assertEquals("123 E Main St", transaction.billing_details.street_address)
        self.assertEquals("Suite 403", transaction.billing_details.extended_address)
        self.assertEquals("Chicago", transaction.billing_details.locality)
        self.assertEquals("IL", transaction.billing_details.region)
        self.assertEquals("60622", transaction.billing_details.postal_code)
        self.assertEquals("United States of America", transaction.billing_details.country_name)
        self.assertEquals("US", transaction.billing_details.country_code_alpha2)
        self.assertEquals("USA", transaction.billing_details.country_code_alpha3)
        self.assertEquals("840", transaction.billing_details.country_code_numeric)
        self.assertEquals("Andrew", transaction.shipping_details.first_name)
        self.assertEquals("Mason", transaction.shipping_details.last_name)
        self.assertEquals("Braintree", transaction.shipping_details.company)
        self.assertEquals("456 W Main St", transaction.shipping_details.street_address)
        self.assertEquals("Apt 2F", transaction.shipping_details.extended_address)
        self.assertEquals("Bartlett", transaction.shipping_details.locality)
        self.assertEquals("IL", transaction.shipping_details.region)
        self.assertEquals("60103", transaction.shipping_details.postal_code)
        self.assertEquals("Mexico", transaction.shipping_details.country_name)
        self.assertEquals("MX", transaction.shipping_details.country_code_alpha2)
        self.assertEquals("MEX", transaction.shipping_details.country_code_alpha3)
        self.assertEquals("484", transaction.shipping_details.country_code_numeric)

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
        self.assertEquals(transaction.credit_card_details.masked_number, "411111******1111")
        self.assertEquals(None, transaction.vault_credit_card)

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
        self.assertEquals("411111******1111", transaction.credit_card_details.masked_number)
        self.assertEquals("411111******1111", transaction.vault_credit_card.masked_number)

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
        self.assertEquals("some extra stuff", transaction.custom_fields["store_me"])

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
        self.assertEquals(TestHelper.non_default_merchant_account_id, transaction.merchant_account_id)

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
        self.assertEquals(TestHelper.default_merchant_account_id, transaction.merchant_account_id)

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
        self.assertEquals("123 Fake St.", transaction.shipping_details.street_address)
        self.assertEquals(address.id, transaction.shipping_details.id)


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
        self.assertEquals("12345", transaction.purchase_order_number)
        self.assertEquals(Decimal("10.00"), transaction.tax_amount)
        self.assertEquals(True, transaction.tax_exempt)

    def test_create_with_failing_level_2_validations(self):
        result = Transaction.sale({
            "amount": Decimal("100"),
            "tax_amount": "asdf",
            "purchase_order_number": "aaaaaaaaaaaaaaaaaa",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.Transaction.TaxAmountFormatIsInvalid,
            result.errors.for_object("transaction").on("tax_amount")[0].code
        )
        self.assertEquals(
            ErrorCodes.Transaction.PurchaseOrderNumberIsTooLong,
            result.errors.for_object("transaction").on("purchase_order_number")[0].code
        )

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
        self.assertEquals(Transaction.Status.ProcessorDeclined, transaction.status)

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
            self.assertEquals(Transaction.GatewayRejectionReason.Avs, transaction.gateway_rejection_reason)
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
            self.assertEquals(Transaction.GatewayRejectionReason.AvsAndCvv, transaction.gateway_rejection_reason)
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
            self.assertEquals(Transaction.GatewayRejectionReason.Cvv, transaction.gateway_rejection_reason)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

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
        self.assertEquals(
            ErrorCodes.Transaction.CustomFieldIsInvalid,
            result.errors.for_object("transaction").on("custom_fields")[0].code
        )

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
        self.assertNotEqual(None, re.search("\A\d{6,7}\Z", transaction.customer_details.id))
        self.assertEquals(transaction.customer_details.id, transaction.vault_customer.id)
        self.assertNotEqual(None, re.search("\A\w{4,5}\Z", transaction.credit_card_details.token))
        self.assertEquals(transaction.credit_card_details.token, transaction.vault_credit_card.token)

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
        self.assertNotEqual(None, re.search("\A\d{6,7}\Z", transaction.customer_details.id))
        self.assertEquals(transaction.customer_details.id, transaction.vault_customer.id)
        self.assertNotEqual(None, re.search("\A\w{4,5}\Z", transaction.credit_card_details.token))
        self.assertEquals(transaction.credit_card_details.token, transaction.vault_credit_card.token)

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
        self.assertNotEquals(None, re.search("\A\d{6,7}\Z", transaction.customer_details.id))
        self.assertEquals(transaction.customer_details.id, transaction.vault_customer.id)
        credit_card = CreditCard.find(transaction.vault_credit_card.token)
        self.assertEquals(credit_card.billing_address.id, transaction.billing_details.id)
        self.assertEquals(credit_card.billing_address.id, transaction.vault_billing_address.id)
        self.assertEquals("Carl", credit_card.billing_address.first_name)
        self.assertEquals("Jones", credit_card.billing_address.last_name)
        self.assertEquals("Braintree", credit_card.billing_address.company)
        self.assertEquals("123 E Main St", credit_card.billing_address.street_address)
        self.assertEquals("Suite 403", credit_card.billing_address.extended_address)
        self.assertEquals("Chicago", credit_card.billing_address.locality)
        self.assertEquals("IL", credit_card.billing_address.region)
        self.assertEquals("60622", credit_card.billing_address.postal_code)
        self.assertEquals("United States of America", credit_card.billing_address.country_name)

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
        self.assertNotEquals(None, re.search("\A\d{6,7}\Z", transaction.customer_details.id))
        self.assertEquals(transaction.customer_details.id, transaction.vault_customer.id)
        shipping_address = transaction.vault_customer.addresses[0]
        self.assertEquals("Carl", shipping_address.first_name)
        self.assertEquals("Jones", shipping_address.last_name)
        self.assertEquals("Braintree", shipping_address.company)
        self.assertEquals("123 E Main St", shipping_address.street_address)
        self.assertEquals("Suite 403", shipping_address.extended_address)
        self.assertEquals("Chicago", shipping_address.locality)
        self.assertEquals("IL", shipping_address.region)
        self.assertEquals("60622", shipping_address.postal_code)
        self.assertEquals("United States of America", shipping_address.country_name)

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
        self.assertEquals(Transaction.Status.SubmittedForSettlement, result.transaction.status)

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
        self.assertEquals(Transaction.Status.Authorized, result.transaction.status)

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
        self.assertEquals(customer_id, transaction.customer_details.id)
        self.assertEquals(customer_id, transaction.vault_customer.id)
        self.assertEquals(payment_method_token, transaction.credit_card_details.token)
        self.assertEquals(payment_method_token, transaction.vault_credit_card.token)

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
        self.assertEquals(customer.id, transaction.customer_details.id)
        self.assertEquals(customer.id, transaction.vault_customer.id)
        self.assertEquals(credit_card.token, transaction.credit_card_details.token)
        self.assertEquals(credit_card.token, transaction.vault_credit_card.token)

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
        self.assertEquals(customer.id, transaction.customer_details.id)
        self.assertEquals(customer.id, transaction.vault_customer.id)
        self.assertEquals(credit_card.token, transaction.credit_card_details.token)
        self.assertEquals(credit_card.token, transaction.vault_credit_card.token)

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
        self.assertEquals(customer.id, transaction.customer_details.id)
        self.assertEquals(customer.id, transaction.vault_customer.id)
        self.assertEquals(credit_card.token, transaction.credit_card_details.token)
        self.assertEquals(credit_card.token, transaction.vault_credit_card.token)
        self.assertEquals("S", transaction.cvv_response_code)

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
        self.assertEquals(params, result.params)
        self.assertEquals(
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
        self.assertNotEquals(None, re.search("\A\w{6}\Z", transaction.id))
        self.assertEquals(Transaction.Type.Credit, transaction.type)
        self.assertEquals(Decimal(TransactionAmounts.Authorize), transaction.amount)
        cc_details = transaction.credit_card_details
        self.assertEquals("411111", cc_details.bin)
        self.assertEquals("1111", cc_details.last_4)
        self.assertEquals("05/2009", cc_details.expiration_date)

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
        self.assertEquals(params, result.params)
        self.assertEquals(
            ErrorCodes.Transaction.AmountIsRequired,
            result.errors.for_object("transaction").on("amount")[0].code
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
        self.assertEquals(TestHelper.non_default_merchant_account_id, transaction.merchant_account_id)

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
        self.assertEquals(TestHelper.default_merchant_account_id, transaction.merchant_account_id)

    def test_find_returns_a_found_transaction(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction
        found_transaction = Transaction.find(transaction.id)
        self.assertEquals(transaction.id, found_transaction.id)

    def test_find_for_bad_transaction_raises_not_found_error(self):
        try:
            Transaction.find("notreal")
            self.assertTrue(False)
        except NotFoundError, e:
            self.assertEquals("transaction with id notreal not found", str(e))

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
        self.assertEquals(transaction.id, result.transaction.id)
        self.assertEquals(Transaction.Status.Voided, result.transaction.status)

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
        self.assertEquals(
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
        self.assertEquals(Transaction.Type.Sale, transaction.type)

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
        self.assertEquals(ErrorCodes.Transaction.TypeIsRequired, result.errors.for_object("transaction").on("type")[0].code)
        self.assertEquals(
            ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted,
            result.errors.for_object("transaction").for_object("billing").on("country_code_alpha2")[0].code
        )
        self.assertEquals(
            ErrorCodes.Address.CountryCodeAlpha3IsNotAccepted,
            result.errors.for_object("transaction").for_object("billing").on("country_code_alpha3")[0].code
        )
        self.assertEquals(
            ErrorCodes.Address.CountryCodeNumericIsNotAccepted,
            result.errors.for_object("transaction").for_object("billing").on("country_code_numeric")[0].code
        )
        self.assertEquals(
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
        self.assertEquals(Decimal(TransactionAmounts.Authorize), transaction.amount)
        self.assertEquals(Transaction.Type.Sale, transaction.type)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2010", transaction.credit_card_details.expiration_date)

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
            result = Transaction.confirm_transparent_redirect(query_string)
            self.fail()
        except AuthorizationError, e:
            self.assertEquals("Invalid params: transaction[bad]", e.message)

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
        self.assertEquals(Decimal(TransactionAmounts.Authorize), transaction.amount)
        self.assertEquals(Transaction.Type.Credit, transaction.type)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2010", transaction.credit_card_details.expiration_date)

        self.assertEquals("US", transaction.billing_details.country_code_alpha2)
        self.assertEquals("USA", transaction.billing_details.country_code_alpha3)
        self.assertEquals("840", transaction.billing_details.country_code_numeric)
        self.assertEquals("United States of America", transaction.billing_details.country_name)

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

        self.assertEquals(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)
        self.assertEquals(Decimal(TransactionAmounts.Authorize), submitted_transaction.amount)

    def test_submit_for_settlement_with_amount(self):
        transaction = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        submitted_transaction = Transaction.submit_for_settlement(transaction.id, Decimal("900")).transaction

        self.assertEquals(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)
        self.assertEquals(Decimal("900.00"), submitted_transaction.amount)

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

        self.assertEquals(
            ErrorCodes.Transaction.SettlementAmountIsTooLarge,
            result.errors.for_object("transaction").on("amount")[0].code
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

        self.assertEquals(2, len(submitted_transaction.status_history))
        self.assertEquals(Transaction.Status.Authorized, submitted_transaction.status_history[0].status)
        self.assertEquals(Decimal(TransactionAmounts.Authorize), submitted_transaction.status_history[0].amount)
        self.assertEquals(Transaction.Status.SubmittedForSettlement, submitted_transaction.status_history[1].status)
        self.assertEquals(Decimal(TransactionAmounts.Authorize), submitted_transaction.status_history[1].amount)

    def test_successful_refund(self):
        transaction = self.__create_transaction_to_refund()

        result = Transaction.refund(transaction.id)

        self.assertTrue(result.is_success)
        refund = result.transaction

        self.assertEquals(Transaction.Type.Credit, refund.type)
        self.assertEquals(Decimal(TransactionAmounts.Authorize), refund.amount)
        self.assertEquals(transaction.id, refund.refunded_transaction_id)

        self.assertEquals(refund.id, Transaction.find(transaction.id).refund_id)

    def test_successful_partial_refund(self):
        transaction = self.__create_transaction_to_refund()

        result = Transaction.refund(transaction.id, Decimal("500.00"))

        self.assertTrue(result.is_success)
        self.assertEquals(Transaction.Type.Credit, result.transaction.type)
        self.assertEquals(Decimal("500.00"), result.transaction.amount)

    def test_multiple_successful_partial_refunds(self):
        transaction = self.__create_transaction_to_refund()

        refund1 = Transaction.refund(transaction.id, Decimal("500.00")).transaction
        self.assertEquals(Transaction.Type.Credit, refund1.type)
        self.assertEquals(Decimal("500.00"), refund1.amount)

        refund2 = Transaction.refund(transaction.id, Decimal("500.00")).transaction
        self.assertEquals(Transaction.Type.Credit, refund2.type)
        self.assertEquals(Decimal("500.00"), refund2.amount)

        transaction = Transaction.find(transaction.id)

        self.assertEquals(2, len(transaction.refund_ids))
        self.assertTrue(TestHelper.in_list(transaction.refund_ids, refund1.id))
        self.assertTrue(TestHelper.in_list(transaction.refund_ids, refund2.id))

    def test_refund_already_refunded_transation_fails(self):
        transaction = self.__create_transaction_to_refund()

        Transaction.refund(transaction.id)
        result = Transaction.refund(transaction.id)

        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.Transaction.HasAlreadyBeenRefunded,
            result.errors.for_object("transaction").on("base")[0].code
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
        self.assertEquals(
            ErrorCodes.Transaction.CannotRefundUnlessSettled,
            result.errors.for_object("transaction").on("base")[0].code
        )

    def __create_transaction_to_refund(self):
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

    def test_snapshot_add_ons_and_discounts_from_subscription(self):
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

        self.assertEquals(2, len(transaction.add_ons))
        add_ons = sorted(transaction.add_ons, key=lambda add_on: add_on.id)

        self.assertEquals("increase_10", add_ons[0].id)
        self.assertEquals(Decimal("11.00"), add_ons[0].amount)
        self.assertEquals(2, add_ons[0].quantity)
        self.assertEquals(5, add_ons[0].number_of_billing_cycles)
        self.assertFalse(add_ons[0].never_expires)

        self.assertEquals("increase_20", add_ons[1].id)
        self.assertEquals(Decimal("21.00"), add_ons[1].amount)
        self.assertEquals(3, add_ons[1].quantity)
        self.assertEquals(6, add_ons[1].number_of_billing_cycles)
        self.assertFalse(add_ons[1].never_expires)

        self.assertEquals(1, len(transaction.discounts))
        discounts = transaction.discounts

        self.assertEquals("discount_7", discounts[0].id)
        self.assertEquals(Decimal("7.50"), discounts[0].amount)
        self.assertEquals(2, discounts[0].quantity)
        self.assertEquals(None, discounts[0].number_of_billing_cycles)
        self.assertTrue(discounts[0].never_expires)

    def test_descriptors_accepts_name_and_phone(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "descriptor": {
                "name": "123*123456789012345678",
                "phone": "3334445555"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertEquals("123*123456789012345678", transaction.descriptor.name)
        self.assertEquals("3334445555", transaction.descriptor.phone)

    def test_descriptors_has_validation_errors_if_format_is_invalid(self):
        result = Transaction.sale({
            "amount": TransactionAmounts.Authorize,
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "descriptor": {
                "name": "badcompanyname12*badproduct12",
                "phone": "%bad4445555"
            }
        })
        self.assertFalse(result.is_success)
        transaction = result.transaction
        self.assertEquals(
            ErrorCodes.Descriptor.NameFormatIsInvalid,
            result.errors.for_object("transaction").for_object("descriptor").on("name")[0].code
        )
        self.assertEquals(
            ErrorCodes.Descriptor.PhoneFormatIsInvalid,
            result.errors.for_object("transaction").for_object("descriptor").on("phone")[0].code
        )
