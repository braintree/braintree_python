from tests.test_helper import *

class TestTransaction(unittest.TestCase):
    def test_sale_returns_a_successful_result_with_type_of_sale(self):
        result = Transaction.sale({
            "amount": "1000.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search("\A\w{6}\Z", transaction.id))
        self.assertEquals(Transaction.Type.Sale, transaction.type)
        self.assertEquals(Decimal("1000.00"), transaction.amount)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2009", transaction.credit_card_details.expiration_date)

    def test_sale_allows_amount_as_a_decimal(self):
        result = Transaction.sale({
            "amount": Decimal("1000.00"),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEqual(None, re.search("\A\w{6}\Z", transaction.id))
        self.assertEquals(Transaction.Type.Sale, transaction.type)
        self.assertEquals(Decimal("1000.00"), transaction.amount)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2009", transaction.credit_card_details.expiration_date)

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
                "country_name": "United States of America"
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
                "country_name": "United States of America"
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
        self.assertEquals("Andrew", transaction.shipping_details.first_name)
        self.assertEquals("Mason", transaction.shipping_details.last_name)
        self.assertEquals("Braintree", transaction.shipping_details.company)
        self.assertEquals("456 W Main St", transaction.shipping_details.street_address)
        self.assertEquals("Apt 2F", transaction.shipping_details.extended_address)
        self.assertEquals("Bartlett", transaction.shipping_details.locality)
        self.assertEquals("IL", transaction.shipping_details.region)
        self.assertEquals("60103", transaction.shipping_details.postal_code)
        self.assertEquals("United States of America", transaction.shipping_details.country_name)

    def test_sale_with_custom_fields(self):
        result = Transaction.sale({
            "amount": "1000.00",
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

    def test_validation_error_on_invalid_custom_fields(self):
        result = Transaction.sale({
            "amount": "1000.00",
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

    def test_create_can_stuff_customer_and_credit_card_in_the_vault(self):
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
            "amount": Decimal("1000.00"),
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction
        self.assertNotEquals(None, re.search("\A\w{6}\Z", transaction.id))
        self.assertEquals(Transaction.Type.Credit, transaction.type)
        self.assertEquals(Decimal("1000.00"), transaction.amount)
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

    def test_find_returns_a_found_transaction(self):
        transaction = Transaction.sale({
            "amount": "1000.00",
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
            "amount": "1000.00",
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
            "amount": "2000.00",
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
            "amount": "1000.00",
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
            "amount": "1000.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.Transaction.TypeIsRequired, result.errors.for_object("transaction").on("type")[0].code)

    def test_sale_from_transparent_redirect_with_successful_result(self):
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

        query_string = TestHelper.simulate_tr_form_post(post_params, Transaction.transparent_redirect_create_url())
        result = Transaction.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)

        transaction = result.transaction
        self.assertEquals(Decimal("1000.00"), transaction.amount)
        self.assertEquals(Transaction.Type.Sale, transaction.type)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2010", transaction.credit_card_details.expiration_date)

    def test_sale_from_transparent_redirect_with_error_result(self):
        tr_data = {
            "transaction": {
                "amount": "1000.00",
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
        self.assertEquals(ErrorCodes.CreditCard.NumberHasInvalidLength, result.errors.for_object("transaction").for_object("credit_card").on("number")[0].code)

    def test_credit_from_transparent_redirect_with_successful_result(self):
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

        query_string = TestHelper.simulate_tr_form_post(post_params, Transaction.transparent_redirect_create_url())
        result = Transaction.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)

        transaction = result.transaction
        self.assertEquals(Decimal("1000.00"), transaction.amount)
        self.assertEquals(Transaction.Type.Credit, transaction.type)
        self.assertEquals("411111", transaction.credit_card_details.bin)
        self.assertEquals("1111", transaction.credit_card_details.last_4)
        self.assertEquals("05/2010", transaction.credit_card_details.expiration_date)

    def test_credit_from_transparent_redirect_with_error_result(self):
        tr_data = {
            "transaction": {
                "amount": "1000.00",
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
        self.assertEquals(ErrorCodes.CreditCard.NumberHasInvalidLength, result.errors.for_object("transaction").for_object("credit_card").on("number")[0].code)

    def test_submit_for_settlement_without_amount(self):
        transaction = Transaction.sale({
            "amount": "1000.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            }
        }).transaction

        submitted_transaction = Transaction.submit_for_settlement(transaction.id).transaction

        self.assertEquals(Transaction.Status.SubmittedForSettlement, submitted_transaction.status)
        self.assertEquals(Decimal("1000.00"), submitted_transaction.amount)

    def test_submit_for_settlement_with_amount(self):
        transaction = Transaction.sale({
            "amount": "1000.00",
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
            "amount": "1000.00",
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

    def test_search_returns_some_results(self):
        collection = Transaction.search("411111")

        self.assertEquals(1, collection.current_page_number)
        self.assertTrue(collection.page_size > 0)
        self.assertTrue(collection.total_items > 0)
        self.assertEquals("411111", collection[0].credit_card_details.bin)

    def test_search_can_traverse_pages(self):
        first_page = Transaction.search("411111")
        self.assertEquals(1, first_page.current_page_number)

        next_page = first_page.next_page()
        self.assertEquals(2, next_page.current_page_number)
        self.assertEquals("411111", next_page[0].credit_card_details.bin)

        self.assertNotEquals(first_page[0].id, next_page[0].id)

    def test_search_on_last_page(self):
        last_page_number = Transaction.search("411111").total_pages

        collection = Transaction.search("411111", last_page_number)
        self.assertTrue(collection.is_last_page)
        self.assertEquals(None, collection.next_page())

    def test_search_with_no_results(self):
        collection = Transaction.search("no_such_transactions_exists")
        self.assertEquals(0, collection.total_items)
        self.assertEquals(0, collection.current_page_size)
        self.assertEquals(1, collection.current_page_number)

    def test_all_statuses(self):
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("authorizing"), Transaction.Status.Authorizing)
        )
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("authorized"), Transaction.Status.Authorized)
        )
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("gateway_rejected"), Transaction.Status.GatewayRejected)
        )
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("failed"), Transaction.Status.Failed)
        )
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("processor_declined"), Transaction.Status.ProcessorDeclined)
        )
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("settled"), Transaction.Status.Settled)
        )
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("settlement_failed"), Transaction.Status.SettlementFailed)
        )
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("submitted_for_settlement"), Transaction.Status.SubmittedForSettlement)
        )
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("unknown"), Transaction.Status.Unknown)
        )
        self.assertTrue(
            TestHelper.includes_status_on_any_page(Transaction.search("voided"), Transaction.Status.Voided)
        )

    def test_successful_refund(self):
        transaction = self.__create_transaction_to_refund()

        result = Transaction.refund(transaction.id)

        self.assertTrue(result.is_success)
        self.assertEquals(Transaction.Type.Credit, result.transaction.type)
        self.assertEquals(Decimal("1000.00"), result.transaction.amount)

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
            "amount": "1000.00",
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
            "amount": "1000.00",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2009"
            },
            "options": {
                "submit_for_settlement": True
            }
        }).transaction

        Http().put("/transactions/" + transaction.id + "/settle")
        return transaction
