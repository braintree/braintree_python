from tests.test_helper import *

class TestCreditCard(unittest.TestCase):
    def test_create_adds_credit_card_to_existing_customer(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertTrue(re.search("\A\w{4,5}\Z", credit_card.token) != None)
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2009", credit_card.expiration_year)
        self.assertEquals("05/2009", credit_card.expiration_date)
        self.assertEquals("John Doe", credit_card.cardholder_name)

    def test_create_and_make_default(self):
        customer = Customer.create().customer
        card1 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        self.assertTrue(card1.default)

        card2 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe",
            "options":
                {"make_default": True}
        }).credit_card

        card1 = CreditCard.find(card1.token)
        self.assertFalse(card1.default)
        self.assertTrue(card2.default)


    def test_create_with_expiration_month_and_year(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_month": "05",
            "expiration_year": "2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertEquals("05/2009", credit_card.expiration_date)

    def test_create_can_specify_the_desired_token(self):
        token = str(random.randint(1, 1000000))
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "token": token
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertEquals(token, credit_card.token)

    def test_create_with_billing_address(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "billing_address": {
                "street_address": "123 Abc Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60622",
                "country_code_alpha2": "MX",
                "country_code_alpha3": "MEX",
                "country_code_numeric": "484",
                "country_name": "Mexico"
            }
        })

        self.assertTrue(result.is_success)
        address = result.credit_card.billing_address
        self.assertEquals("123 Abc Way", address.street_address)
        self.assertEquals("Chicago", address.locality)
        self.assertEquals("Illinois", address.region)
        self.assertEquals("60622", address.postal_code)
        self.assertEquals("MX", address.country_code_alpha2)
        self.assertEquals("MEX", address.country_code_alpha3)
        self.assertEquals("484", address.country_code_numeric)
        self.assertEquals("Mexico", address.country_name)

    def test_create_with_billing_address_id(self):
        customer = Customer.create().customer
        address = Address.create({
            "customer_id": customer.id,
            "street_address": "123 Abc Way"
        }).address

        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "billing_address_id": address.id
        })

        self.assertTrue(result.is_success)
        billing_address = result.credit_card.billing_address
        self.assertEquals(address.id, billing_address.id)
        self.assertEquals("123 Abc Way", billing_address.street_address)

    def test_create_without_billing_address_still_has_billing_address_method(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
        })
        self.assertTrue(result.is_success)
        self.assertEquals(None, result.credit_card.billing_address)

    def test_create_with_card_verification(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2009",
            "options": {"verify_card": True}
        })

        self.assertFalse(result.is_success)
        verification = result.credit_card_verification
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, verification.status)
        self.assertEquals("2000", verification.processor_response_code)
        self.assertEquals("Do Not Honor", verification.processor_response_text)
        self.assertEquals("I", verification.cvv_response_code)
        self.assertEquals(None, verification.avs_error_response_code)
        self.assertEquals("I", verification.avs_postal_code_response_code)
        self.assertEquals("I", verification.avs_street_address_response_code)
        self.assertEquals(TestHelper.default_merchant_account_id, verification.merchant_account_id)

    def test_create_with_card_verification_and_non_default_merchant_account(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2009",
            "options": {
                "verification_merchant_account_id": TestHelper.non_default_merchant_account_id,
                "verify_card": True
            }
        })

        self.assertFalse(result.is_success)
        verification = result.credit_card_verification
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, verification.status)
        self.assertEquals(None, verification.gateway_rejection_reason)
        self.assertEquals(TestHelper.non_default_merchant_account_id, verification.merchant_account_id)

    def test_verify_gateway_rejected_responds_to_processor_response_code(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "processing_rules_merchant_id"
            Configuration.public_key = "processing_rules_public_key"
            Configuration.private_key = "processing_rules_private_key"

            customer = Customer.create().customer
            result = CreditCard.create({
                "customer_id": customer.id,
                "number": "4111111111111111",
                "expiration_date": "05/2009",
                "billing_address": {
                    "postal_code": "20000"
                },
                "options": {
                    "verify_card": True
                }
            })


            self.assertFalse(result.is_success)
            self.assertEquals('1000', result.credit_card_verification.processor_response_code)
            self.assertEquals('Approved', result.credit_card_verification.processor_response_text)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_expose_gateway_rejection_reason_on_verification(self):
        old_merchant_id = Configuration.merchant_id
        old_public_key = Configuration.public_key
        old_private_key = Configuration.private_key

        try:
            Configuration.merchant_id = "processing_rules_merchant_id"
            Configuration.public_key = "processing_rules_public_key"
            Configuration.private_key = "processing_rules_private_key"

            customer = Customer.create().customer
            result = CreditCard.create({
                "customer_id": customer.id,
                "number": "4111111111111111",
                "expiration_date": "05/2009",
                "cvv": "200",
                "options": {
                    "verify_card": True
                }
            })

            self.assertFalse(result.is_success)
            verification = result.credit_card_verification
            self.assertEquals(Transaction.GatewayRejectionReason.Cvv, verification.gateway_rejection_reason)
        finally:
            Configuration.merchant_id = old_merchant_id
            Configuration.public_key = old_public_key
            Configuration.private_key = old_private_key

    def test_create_with_card_verification_set_to_false(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4000111111111115",
            "expiration_date": "05/2009",
            "options": {"verify_card": False}
        })

        self.assertTrue(result.is_success)

    def test_create_with_invalid_invalid_options(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "invalid_date",
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.CreditCard.ExpirationDateIsInvalid, result.errors.for_object("credit_card").on("expiration_date")[0].code)
        self.assertEquals("Expiration date is invalid.", result.message)

    def test_create_with_invalid_country_codes(self):
        customer = Customer.create().customer
        result = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2012",
            "billing_address": {
                "country_code_alpha2": "ZZ",
                "country_code_alpha3": "ZZZ",
                "country_code_numeric": "000",
                "country_name": "zzzzzzz"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted,
            result.errors.for_object("credit_card").for_object("billing_address").on("country_code_alpha2")[0].code
        )
        self.assertEquals(
            ErrorCodes.Address.CountryCodeAlpha3IsNotAccepted,
            result.errors.for_object("credit_card").for_object("billing_address").on("country_code_alpha3")[0].code
        )
        self.assertEquals(
            ErrorCodes.Address.CountryCodeNumericIsNotAccepted,
            result.errors.for_object("credit_card").for_object("billing_address").on("country_code_numeric")[0].code
        )
        self.assertEquals(
            ErrorCodes.Address.CountryNameIsNotAccepted,
            result.errors.for_object("credit_card").for_object("billing_address").on("country_name")[0].code
        )

    def test_update_with_valid_options(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "number": "5105105105105100",
            "expiration_date": "06/2010",
            "cvv": "123",
            "cardholder_name": "Jane Jones"
        })

        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertTrue(re.search("\A\w{4,5}\Z", credit_card.token) != None)
        self.assertEquals("510510", credit_card.bin)
        self.assertEquals("5100", credit_card.last_4)
        self.assertEquals("06", credit_card.expiration_month)
        self.assertEquals("2010", credit_card.expiration_year)
        self.assertEquals("06/2010", credit_card.expiration_date)
        self.assertEquals("Jane Jones", credit_card.cardholder_name)

    def test_update_billing_address_creates_new_by_default(self):
        customer = Customer.create().customer
        initial_credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "billing_address": {
                "street_address": "123 Nigeria Ave",
            }
        }).credit_card

        updated_credit_card = CreditCard.update(initial_credit_card.token, {
            "billing_address": {
                "region": "IL",
                "country_code_alpha2": "NG",
                "country_code_alpha3": "NGA",
                "country_code_numeric": "566",
                "country_name": "Nigeria"
            }
        }).credit_card

        self.assertEquals("IL", updated_credit_card.billing_address.region)
        self.assertEquals("NG", updated_credit_card.billing_address.country_code_alpha2)
        self.assertEquals("NGA", updated_credit_card.billing_address.country_code_alpha3)
        self.assertEquals("566", updated_credit_card.billing_address.country_code_numeric)
        self.assertEquals("Nigeria", updated_credit_card.billing_address.country_name)
        self.assertEquals(None, updated_credit_card.billing_address.street_address)
        self.assertNotEquals(initial_credit_card.billing_address.id, updated_credit_card.billing_address.id)

    def test_update_billing_address_when_update_existing_is_True(self):
        customer = Customer.create().customer
        initial_credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "billing_address": {
                "street_address": "123 Nigeria Ave",
            }
        }).credit_card

        updated_credit_card = CreditCard.update(initial_credit_card.token, {
            "billing_address": {
                "region": "IL",
                "options": {
                    "update_existing": True
                }
            }
        }).credit_card

        self.assertEquals("IL", updated_credit_card.billing_address.region)
        self.assertEquals("123 Nigeria Ave", updated_credit_card.billing_address.street_address)
        self.assertEquals(initial_credit_card.billing_address.id, updated_credit_card.billing_address.id)

    def test_update_and_make_default(self):
        customer = Customer.create().customer
        card1 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card
        card2 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        self.assertTrue(card1.default)
        self.assertFalse(card2.default)

        result = CreditCard.update(card2.token, {
            "options": {
                "make_default": True
            }
        })
        self.assertFalse(CreditCard.find(card1.token).default)
        self.assertTrue(CreditCard.find(card2.token).default)


    def test_update_verifies_card_if_option_is_provided(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "number": "4000111111111115",
            "expiration_date": "06/2010",
            "cvv": "123",
            "cardholder_name": "Jane Jones",
            "options": {"verify_card": True}
        })

        self.assertFalse(result.is_success)
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, result.credit_card_verification.status)

    def test_update_verifies_card_with_non_default_merchant_account(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "number": "4000111111111115",
            "expiration_date": "06/2010",
            "cvv": "123",
            "cardholder_name": "Jane Jones",
            "options": {
                "verification_merchant_account_id": TestHelper.non_default_merchant_account_id,
                "verify_card": True
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, result.credit_card_verification.status)

    def test_update_billing_address(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "billing_address": {
                "street_address": "321 Xyz Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60621"
            }
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "billing_address": {
                "street_address": "123 Abc Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60622"
            }
        })

        self.assertTrue(result.is_success)
        address = result.credit_card.billing_address
        self.assertEquals("123 Abc Way", address.street_address)
        self.assertEquals("Chicago", address.locality)
        self.assertEquals("Illinois", address.region)
        self.assertEquals("60622", address.postal_code)

    def test_update_returns_error_if_invalid(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009"
        }).credit_card

        result = CreditCard.update(credit_card.token, {
            "expiration_date": "invalid_date"
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.CreditCard.ExpirationDateIsInvalid, result.errors.for_object("credit_card").on("expiration_date")[0].code)

    def test_delete_with_valid_token(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009"
        }).credit_card

        result = CreditCard.delete(credit_card.token)
        self.assertTrue(result.is_success)

    @raises(NotFoundError)
    def test_delete_raises_error_when_deleting_twice(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009"
        }).credit_card

        CreditCard.delete(credit_card.token)
        CreditCard.delete(credit_card.token)

    @raises(NotFoundError)
    def test_delete_with_invalid_token(self):
        result = CreditCard.delete("notreal")

    def test_find_with_valid_token(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009"
        }).credit_card

        found_credit_card = CreditCard.find(credit_card.token)
        self.assertTrue(re.search("\A\w{4,5}\Z", credit_card.token) != None)
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2009", credit_card.expiration_year)
        self.assertEquals("05/2009", credit_card.expiration_date)

    def test_find_returns_associated_subsriptions(self):
        customer = Customer.create().customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009"
        }).credit_card
        id = "id_" + str(random.randint(1, 1000000))
        subscription = Subscription.create({
            "id": id,
            "plan_id": "integration_trialless_plan",
            "payment_method_token": credit_card.token,
            "price": Decimal("1.00")
        }).subscription

        found_credit_card = CreditCard.find(credit_card.token)
        self.assertEquals(id, found_credit_card.subscriptions[0].id)
        self.assertEquals(Decimal("1.00"), found_credit_card.subscriptions[0].price)
        self.assertEquals(credit_card.token, found_credit_card.subscriptions[0].payment_method_token)

    def test_find_with_invalid_token(self):
        try:
            CreditCard.find("bad_token")
            self.assertTrue(False)
        except Exception, e:
            self.assertEquals("payment method with token bad_token not found", str(e))

    def test_create_from_transparent_redirect(self):
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
            "credit_card[billing_address][country_code_alpha2]": "MX",
            "credit_card[billing_address][country_code_alpha3]": "MEX",
            "credit_card[billing_address][country_code_numeric]": "484",
            "credit_card[billing_address][country_name]": "Mexico",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_create_url())
        result = CreditCard.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2012", credit_card.expiration_year)
        self.assertEquals(customer.id, credit_card.customer_id)
        self.assertEquals("MX", credit_card.billing_address.country_code_alpha2)
        self.assertEquals("MEX", credit_card.billing_address.country_code_alpha3)
        self.assertEquals("484", credit_card.billing_address.country_code_numeric)
        self.assertEquals("Mexico", credit_card.billing_address.country_name)


    def test_create_from_transparent_redirect_and_make_default(self):
        customer = Customer.create().customer
        card1 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": "John Doe"
        }).credit_card
        self.assertTrue(card1.default)

        tr_data = {
            "credit_card": {
                "customer_id": customer.id,
                "options": {
                    "make_default": True
                }
            }
        }
        post_params = {
            "tr_data": CreditCard.tr_data_for_create(tr_data, "http://example.com/path?foo=bar"),
            "credit_card[cardholder_name]": "Card Holder",
            "credit_card[number]": "4111111111111111",
            "credit_card[expiration_date]": "05/2012",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_create_url())
        card2 = CreditCard.confirm_transparent_redirect(query_string).credit_card

        self.assertFalse(CreditCard.find(card1.token).default)
        self.assertTrue(card2.default)

    def test_create_from_transparent_redirect_with_error_result(self):
        customer = Customer.create().customer
        tr_data = {
            "credit_card": {
                "customer_id": customer.id
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_create(tr_data, "http://example.com/path"),
            "credit_card[cardholder_name]": "Card Holder",
            "credit_card[number]": "eleventy",
            "credit_card[expiration_date]": "y2k"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_create_url())
        result = CreditCard.confirm_transparent_redirect(query_string)
        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.CreditCard.NumberHasInvalidLength,
            result.errors.for_object("credit_card").on("number")[0].code
        )
        self.assertEquals(
            ErrorCodes.CreditCard.ExpirationDateIsInvalid,
            result.errors.for_object("credit_card").on("expiration_date")[0].code
        )

    def test_update_from_transparent_redirect_with_successful_result(self):
        old_token = str(random.randint(1, 1000000))
        new_token = str(random.randint(1, 1000000))
        credit_card = Customer.create({
            "credit_card": {
                "cardholder_name": "Old Cardholder Name",
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "token": old_token
            }
        }).customer.credit_cards[0]

        tr_data = {
            "payment_method_token": old_token,
            "credit_card": {
                "token": new_token
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_update(tr_data, "http://example.com/path"),
            "credit_card[cardholder_name]": "New Cardholder Name",
            "credit_card[expiration_date]": "05/2014"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_update_url())
        result = CreditCard.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)
        credit_card = result.credit_card
        self.assertEquals(new_token, credit_card.token)
        self.assertEquals("411111", credit_card.bin)
        self.assertEquals("1111", credit_card.last_4)
        self.assertEquals("05", credit_card.expiration_month)
        self.assertEquals("2014", credit_card.expiration_year)

    def test_update_from_transparent_redirect_and_make_default(self):
        customer = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012"
            }
        }).customer
        card1 = customer.credit_cards[0]

        card2 = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
        }).credit_card

        self.assertTrue(card1.default)
        self.assertFalse(card2.default)

        tr_data = {
            "payment_method_token": card2.token,
            "credit_card": {
                "options": {
                    "make_default": True
                }
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_update(tr_data, "http://example.com/path"),
            "credit_card[cardholder_name]": "New Cardholder Name",
            "credit_card[expiration_date]": "05/2014"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_update_url())
        result = CreditCard.confirm_transparent_redirect(query_string)

        self.assertFalse(CreditCard.find(card1.token).default)
        self.assertTrue(CreditCard.find(card2.token).default)

    def test_update_from_transparent_redirect_and_update_existing_billing_address(self):
        customer = Customer.create({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "billing_address": {
                    "street_address": "123 Old St",
                    "locality": "Chicago",
                    "region": "Illinois",
                    "postal_code": "60621"
                }
            }
        }).customer
        card = customer.credit_cards[0]

        tr_data = {
            "payment_method_token": card.token,
            "credit_card": {
                "billing_address": {
                    "street_address": "123 New St",
                    "locality": "Columbus",
                    "region": "Ohio",
                    "postal_code": "43215",
                    "options": {
                        "update_existing": True
                    }
                }
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_update(tr_data, "http://example.com/path")
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_update_url())
        result = CreditCard.confirm_transparent_redirect(query_string)

        self.assertEquals(1, len(Customer.find(customer.id).addresses))
        updated_card = CreditCard.find(card.token)
        self.assertEquals("123 New St", updated_card.billing_address.street_address)
        self.assertEquals("Columbus", updated_card.billing_address.locality)
        self.assertEquals("Ohio", updated_card.billing_address.region)
        self.assertEquals("43215", updated_card.billing_address.postal_code)

    def test_update_from_transparent_redirect_with_error_result(self):
        old_token = str(random.randint(1, 1000000))
        credit_card = Customer.create({
            "credit_card": {
                "cardholder_name": "Old Cardholder Name",
                "number": "4111111111111111",
                "expiration_date": "05/2012",
                "token": old_token
            }
        }).customer.credit_cards[0]

        tr_data = {
            "payment_method_token": old_token,
            "credit_card": {
                "token": "bad token"
            }
        }

        post_params = {
            "tr_data": CreditCard.tr_data_for_update(tr_data, "http://example.com/path"),
            "credit_card[cardholder_name]": "New Cardholder Name",
            "credit_card[expiration_date]": "05/2014"
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, CreditCard.transparent_redirect_update_url())
        result = CreditCard.confirm_transparent_redirect(query_string)
        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.CreditCard.TokenInvalid,
            result.errors.for_object("credit_card").on("token")[0].code
        )

    def test_expired_can_iterate_over_all_items(self):
        customer_id = Customer.all().first.id

        for i in range(110 - CreditCard.expired().maximum_size):
            CreditCard.create({
                "customer_id": customer_id,
                "number": "4111111111111111",
                "expiration_date": "05/2009",
                "cvv": "100",
                "cardholder_name": "John Doe"
            })

        collection = CreditCard.expired()
        self.assertTrue(collection.maximum_size > 100)

        credit_card_tokens = [credit_card.token for credit_card in collection.items]
        self.assertEquals(collection.maximum_size, len(TestHelper.unique(credit_card_tokens)))

        self.assertEquals(set([True]), TestHelper.unique([credit_card.is_expired for credit_card in collection.items]))

    def test_expiring_between(self):
        customer_id = Customer.all().first.id

        for i in range(110 - CreditCard.expiring_between(date(2010, 1, 1), date(2010, 12, 31)).maximum_size):
            CreditCard.create({
                "customer_id": customer_id,
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100",
                "cardholder_name": "John Doe"
            })

        collection = CreditCard.expiring_between(date(2010, 1, 1), date(2010, 12, 31))
        self.assertTrue(collection.maximum_size > 100)

        credit_card_tokens = [credit_card.token for credit_card in collection.items]
        self.assertEquals(collection.maximum_size, len(TestHelper.unique(credit_card_tokens)))

        self.assertEquals(set(['2010']), TestHelper.unique([credit_card.expiration_year for credit_card in collection.items]))
