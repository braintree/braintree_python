from tests.test_helper import *
import braintree.test.venmo_sdk as venmo_sdk
from braintree.test.nonces import Nonces

class TestCustomer(unittest.TestCase):
    def test_all(self):
        collection = Customer.all()
        self.assertTrue(collection.maximum_size > 100)
        customer_ids = [c.id for c in collection.items]
        self.assertEquals(collection.maximum_size, len(TestHelper.unique(customer_ids)))
        self.assertEquals(Customer, type(collection.first))

    def test_create(self):
        result = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "company": "Fake Company",
            "email": "joe@email.com",
            "phone": "312.555.1234",
            "fax": "614.555.5678",
            "website": "www.email.com"
        })

        self.assertTrue(result.is_success)
        customer = result.customer

        self.assertEqual("Joe", customer.first_name)
        self.assertEqual("Brown", customer.last_name)
        self.assertEqual("Fake Company", customer.company)
        self.assertEqual("joe@email.com", customer.email)
        self.assertEqual("312.555.1234", customer.phone)
        self.assertEqual("614.555.5678", customer.fax)
        self.assertEqual("www.email.com", customer.website)
        self.assertNotEqual(None, customer.id)
        self.assertNotEqual(None, re.search("\A\d{6,}\Z", customer.id))

    def test_create_with_device_session_id_and_fraud_merchant_id(self):
        result = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "company": "Fake Company",
            "email": "joe@email.com",
            "phone": "312.555.1234",
            "fax": "614.555.5678",
            "website": "www.email.com",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100",
                "device_session_id": "abc123",
                "fraud_merchant_id": "456"
            }
        })

        self.assertTrue(result.is_success)

    def test_create_with_risk_data_security_parameters(self):
        result = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "options": {
                    "verify_card": True,
                }
            },
            "risk_data": {
                "customer_browser": "IE7",
                "customer_ip": "192.168.0.1"
            }
        })

        self.assertTrue(result.is_success)

    def test_create_using_access_token(self):
        gateway = BraintreeGateway(
            client_id = "client_id$development$integration_client_id",
            client_secret = "client_secret$development$integration_client_secret",
            environment = Environment.Development
        )

        code = TestHelper.create_grant(gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "read_write"
        })

        result = gateway.oauth.create_token_from_code({
            "code": code
        })

        gateway = BraintreeGateway(
            access_token = result.credentials.access_token,
            environment = Environment.Development
        )

        result = gateway.customer.create({
            "first_name": "Joe",
            "last_name": "Brown"
        })

        self.assertTrue(result.is_success)
        customer = result.customer

        self.assertEqual("Joe", customer.first_name)

    def test_create_with_unicode(self):
        result = Customer.create({
            "first_name": u"Joe<&>",
            "last_name": u"G\u1F00t\u1F18s",
            "company": "Fake Company",
            "email": "joe@email.com",
            "phone": "312.555.1234",
            "fax": "614.555.5678",
            "website": "www.email.com"
        })

        self.assertTrue(result.is_success)
        customer = result.customer

        self.assertEqual(u"Joe<&>", customer.first_name)
        self.assertEqual(u"G\u1f00t\u1F18s", customer.last_name)
        self.assertEqual("Fake Company", customer.company)
        self.assertEqual("joe@email.com", customer.email)
        self.assertEqual("312.555.1234", customer.phone)
        self.assertEqual("614.555.5678", customer.fax)
        self.assertEqual("www.email.com", customer.website)
        self.assertNotEqual(None, customer.id)
        self.assertNotEqual(None, re.search("\A\d{6,}\Z", customer.id))

        found_customer = Customer.find(customer.id)
        self.assertEqual(u"G\u1f00t\u1F18s", found_customer.last_name)

    def test_create_with_apple_pay_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.ApplePayVisa})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertNotEqual(None, customer.apple_pay_cards[0])

    def test_create_with_android_pay_proxy_card_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.AndroidPayCardDiscover})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertIsInstance(customer.android_pay_cards[0], AndroidPayCard)

    def test_create_with_android_pay_network_token_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.AndroidPayCardMasterCard})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertIsInstance(customer.android_pay_cards[0], AndroidPayCard)

    def test_create_with_amex_express_checkout_card_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.AmexExpressCheckoutCard})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertIsInstance(customer.amex_express_checkout_cards[0], AmexExpressCheckoutCard)

    def test_create_with_venmo_account_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.VenmoAccount})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertIsInstance(customer.venmo_accounts[0], VenmoAccount)

    def test_create_with_paypal_future_payments_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.PayPalFuturePayment})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertNotEqual(None, customer.paypal_accounts[0])

    def test_create_with_paypal_one_time_nonce_fails(self):
        http = ClientApiHttp.create()
        result = Customer.create({"payment_method_nonce": Nonces.PayPalOneTimePayment})
        self.assertFalse(result.is_success)
        self.assertEquals(
            result.errors.for_object("customer").for_object("paypal_account").on("base")[0].code,
            ErrorCodes.PayPalAccount.CannotVaultOneTimeUsePayPalAccount
        )

    def test_create_with_no_attributes(self):
        result = Customer.create()
        self.assertTrue(result.is_success)
        self.assertNotEqual(None, result.customer.id)

    def test_create_with_special_chars(self):
        result = Customer.create({"first_name": "XML Chars <>&'\""})
        self.assertTrue(result.is_success)
        self.assertEqual("XML Chars <>&'\"", result.customer.first_name)

    def test_create_returns_an_error_response_if_invalid(self):
        result = Customer.create({
            "email": "@invalid.com",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "billing_address": {
                    "country_code_alpha2": "MX",
                    "country_code_alpha3": "USA"
                }
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(2, result.errors.size)
        self.assertEquals(ErrorCodes.Customer.EmailIsInvalid, result.errors.for_object("customer").on("email")[0].code)
        self.assertEquals(
            ErrorCodes.Address.InconsistentCountry,
            result.errors.for_object("customer").for_object("credit_card").for_object("billing_address").on("base")[0].code
        )

    def test_create_customer_and_payment_method_at_the_same_time(self):
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
        self.assertEqual("Mike", customer.first_name)
        self.assertEqual("Jones", customer.last_name)

        credit_card = customer.credit_cards[0]
        self.assertEqual("411111", credit_card.bin)
        self.assertEqual("1111", credit_card.last_4)
        self.assertEqual("05/2010", credit_card.expiration_date)

    def test_create_customer_and_verify_payment_method(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4000111111111115",
                "expiration_date": "05/2010",
                "cvv": "100",
                "options": {"verify_card": True}
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(CreditCardVerification.Status.ProcessorDeclined, result.credit_card_verification.status)

    def test_create_customer_and_verify_payment_method_with_verification_amount(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100",
                "options": {"verify_card": True, "verification_amount": "6.00"}
            }
        })

        self.assertTrue(result.is_success)

    def test_create_customer_with_check_duplicate_payment_method(self):
        attributes = {
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4000111111111115",
                "expiration_date": "05/2010",
                "cvv": "100",
                "options": {"fail_on_duplicate_payment_method": True}
            }
        }

        Customer.create(attributes)
        result = Customer.create(attributes)

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.CreditCard.DuplicateCardExists, result.errors.for_object("customer").for_object("credit_card").on("number")[0].code)
        self.assertEquals("Duplicate card exists in the vault.", result.message)

    def test_create_customer_with_payment_method_and_billing_address(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100",
                "billing_address": {
                    "street_address": "123 Abc Way",
                    "locality": "Chicago",
                    "region": "Illinois",
                    "postal_code": "60622",
                    "country_code_alpha2": "US",
                    "country_code_alpha3": "USA",
                    "country_code_numeric": "840",
                    "country_name": "United States of America"
                }
            }
        })

        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual("Mike", customer.first_name)
        self.assertEqual("Jones", customer.last_name)

        address = customer.credit_cards[0].billing_address
        self.assertEqual("123 Abc Way", address.street_address)
        self.assertEqual("Chicago", address.locality)
        self.assertEqual("Illinois", address.region)
        self.assertEqual("60622", address.postal_code)
        self.assertEqual("US", address.country_code_alpha2)
        self.assertEqual("USA", address.country_code_alpha3)
        self.assertEqual("840", address.country_code_numeric)
        self.assertEqual("United States of America", address.country_name)

    def test_create_with_customer_fields(self):
        result = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "custom_fields": {
                "store_me": "custom value"
            }
        })

        self.assertTrue(result.is_success)
        self.assertEquals("custom value", result.customer.custom_fields["store_me"])

    def test_create_returns_nested_errors(self):
        result = Customer.create({
            "email": "invalid",
            "credit_card": {
                "number": "invalid",
                "billing_address": {
                    "country_name": "invalid"
                }
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.Customer.EmailIsInvalid,
            result.errors.for_object("customer").on("email")[0].code
        )
        self.assertEquals(
            ErrorCodes.CreditCard.NumberHasInvalidLength,
            result.errors.for_object("customer").for_object("credit_card").on("number")[0].code
        )
        self.assertEquals(
            ErrorCodes.Address.CountryNameIsNotAccepted,
            result.errors.for_object("customer").for_object("credit_card").for_object("billing_address").on("country_name")[0].code
        )

    def test_create_returns_errors_if_custom_fields_are_not_registered(self):
        result = Customer.create({
            "first_name": "Jack",
            "last_name": "Kennedy",
            "custom_fields": {
                "spouse_name": "Jacqueline"
            }
        })

        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.Customer.CustomFieldIsInvalid, result.errors.for_object("customer").on("custom_fields")[0].code)

    def test_create_with_venmo_sdk_session(self):
        result = Customer.create({
            "first_name": "Jack",
            "last_name": "Kennedy",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "options": {
                    "venmo_sdk_session": venmo_sdk.Session
                }
            }
        })

        self.assertTrue(result.is_success)
        self.assertTrue(result.customer.credit_cards[0].venmo_sdk)

    def test_create_with_venmo_sdk_payment_method_code(self):
        result = Customer.create({
            "first_name": "Jack",
            "last_name": "Kennedy",
            "credit_card": {
                "venmo_sdk_payment_method_code": venmo_sdk.generate_test_payment_method_code("4111111111111111")
            }
        })

        self.assertTrue(result.is_success)
        self.assertEquals("411111", result.customer.credit_cards[0].bin)

    def test_create_with_payment_method_nonce(self):
        config = Configuration.instantiate()
        authorization_fingerprint = json.loads(TestHelper.generate_decoded_client_token())["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })
        status_code, response = http.add_card({
            "credit_card": {
                "number": "4111111111111111",
                "expiration_month": "11",
                "expiration_year": "2099",
            },
            "share": True
        })
        nonce = json.loads(response)["creditCards"][0]["nonce"]

        result = Customer.create({
            "credit_card": {
                "payment_method_nonce": nonce
            }
        })

        self.assertTrue(result.is_success)
        self.assertEquals("411111", result.customer.credit_cards[0].bin)

    def test_delete_with_valid_customer(self):
        customer = Customer.create().customer
        result = Customer.delete(customer.id)

        self.assertTrue(result.is_success)

    @raises(NotFoundError)
    def test_delete_with_invalid_customer(self):
        customer = Customer.create().customer
        Customer.delete(customer.id)
        Customer.delete(customer.id)

    def test_find_with_valid_customer(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Cool"
        }).customer

        found_customer = Customer.find(customer.id)
        self.assertEquals(customer.id, found_customer.id)
        self.assertEquals(customer.first_name, found_customer.first_name)
        self.assertEquals(customer.last_name, found_customer.last_name)

    @raises_with_regexp(NotFoundError, "customer with id 'badid' not found")
    def test_find_with_invalid_customer(self):
        Customer.find("badid")

    def test_update_with_valid_options(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "company": "Fake Company",
            "email": "joe@email.com",
            "phone": "312.555.5555",
            "fax": "614.555.5555",
            "website": "www.email.com"
        }).customer

        result = Customer.update(customer.id, {
            "first_name": "Joe",
            "last_name": "Brown",
            "company": "Fake Company",
            "email": "joe@email.com",
            "phone": "312.555.1234",
            "fax": "614.555.5678",
            "website": "www.email.com"
        })

        self.assertTrue(result.is_success)
        customer = result.customer

        self.assertEqual("Joe", customer.first_name)
        self.assertEqual("Brown", customer.last_name)
        self.assertEqual("Fake Company", customer.company)
        self.assertEqual("joe@email.com", customer.email)
        self.assertEqual("312.555.1234", customer.phone)
        self.assertEqual("614.555.5678", customer.fax)
        self.assertEqual("www.email.com", customer.website)
        self.assertNotEqual(None, customer.id)
        self.assertNotEqual(None, re.search("\A\d{6,}\Z", customer.id))

    def test_update_with_default_payment_method(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
        }).customer

        token1 = str(random.randint(1, 1000000))

        payment_method1 = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.TransactableVisa,
            "token": token1
        }).payment_method

        payment_method1 = PaymentMethod.find(payment_method1.token)
        self.assertTrue(payment_method1.default)

        token2 = str(random.randint(1, 1000000))

        payment_method2 = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.TransactableMasterCard,
            "token": token2
        }).payment_method

        result = Customer.update(customer.id, {
            "default_payment_method_token": payment_method2.token
        })

        payment_method2 = PaymentMethod.find(payment_method2.token)
        self.assertTrue(payment_method2.default)

    def test_update_with_default_payment_method_in_options(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
        }).customer

        token1 = str(random.randint(1, 1000000))

        payment_method1 = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.TransactableVisa,
            "token": token1
        }).payment_method

        payment_method1 = PaymentMethod.find(payment_method1.token)
        self.assertTrue(payment_method1.default)

        token2 = str(random.randint(1, 1000000))

        payment_method2 = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.TransactableMasterCard,
            "token": token2
        }).payment_method

        Customer.update(customer.id, {
            "credit_card": {
                "options": {
                    "update_existing_token": token2,
                    "make_default": True
                    }
                }
            })

        payment_method2 = PaymentMethod.find(payment_method2.token)
        self.assertTrue(payment_method2.default)

    def test_update_with_nested_values(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "10/10",
                "billing_address": {
                    "postal_code": "11111"
                }
            }
        }).customer
        credit_card = customer.credit_cards[0]
        address = credit_card.billing_address

        updated_customer = Customer.update(customer.id, {
            "first_name": "Joe",
            "last_name": "Brown",
            "credit_card": {
                "expiration_date": "12/12",
                "options": {
                    "update_existing_token": credit_card.token
                },
                "billing_address": {
                    "postal_code": "44444",
                    "country_code_alpha2": "US",
                    "country_code_alpha3": "USA",
                    "country_code_numeric": "840",
                    "country_name": "United States of America",
                    "options": {
                        "update_existing": True
                    }
                }
            }
        }).customer
        updated_credit_card = CreditCard.find(credit_card.token)
        updated_address = Address.find(customer.id, address.id)

        self.assertEqual("Joe", updated_customer.first_name)
        self.assertEqual("Brown", updated_customer.last_name)
        self.assertEqual("12/2012", updated_credit_card.expiration_date)
        self.assertEqual("44444", updated_address.postal_code)
        self.assertEqual("US", updated_address.country_code_alpha2)
        self.assertEqual("USA", updated_address.country_code_alpha3)
        self.assertEqual("840", updated_address.country_code_numeric)
        self.assertEqual("United States of America", updated_address.country_name)

    def test_update_with_nested_billing_address_id(self):
        customer = Customer.create().customer
        address = Address.create({
            "customer_id": customer.id,
            "postal_code": "11111"
        }).address

        updated_customer = Customer.update(customer.id, {
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "12/12",
                "billing_address_id": address.id
            }
        }).customer

        credit_card = updated_customer.credit_cards[0]

        self.assertEqual(address.id, credit_card.billing_address.id)
        self.assertEqual("11111", credit_card.billing_address.postal_code)

    def test_update_with_invalid_options(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "company": "Fake Company",
            "email": "joe@email.com",
            "phone": "312.555.5555",
            "fax": "614.555.5555",
            "website": "www.email.com"
        }).customer

        result = Customer.update(customer.id, {
            "email": "@email.com",
        })

        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.Customer.EmailIsInvalid,
            result.errors.for_object("customer").on("email")[0].code
        )

    def test_update_with_paypal_future_payments_nonce(self):
        customer = Customer.create().customer

        result = Customer.update(customer.id, {
            "payment_method_nonce": Nonces.PayPalFuturePayment
        })
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertNotEqual(None, customer.paypal_accounts[0])

    def test_update_with_paypal_one_time_nonce_fails(self):
        customer = Customer.create().customer
        result = Customer.update(customer.id, {
            "payment_method_nonce": Nonces.PayPalOneTimePayment
        })
        self.assertFalse(result.is_success)
        self.assertEquals(
            result.errors.for_object("customer").for_object("paypal_account").on("base")[0].code,
            ErrorCodes.PayPalAccount.CannotVaultOneTimeUsePayPalAccount
        )

    def test_update_with_nested_verification_amount(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "10/10",
                "billing_address": {
                    "postal_code": "11111"
                }
            }
        }).customer
        credit_card = customer.credit_cards[0]
        address = credit_card.billing_address

        result = Customer.update(customer.id, {
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "10/10",
                "options": {
                    "verify_card": True,
                    "verification_amount": "2.00"
                },
            }
        })

        self.assertTrue(result.is_success)

    def test_create_from_transparent_redirect_with_successful_result(self):
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
            "customer[website]": "www.johndoe.com",
            "customer[credit_card][number]": "4111111111111111",
            "customer[credit_card][expiration_date]": "05/2012",
            "customer[credit_card][billing_address][country_code_alpha2]": "MX",
            "customer[credit_card][billing_address][country_code_alpha3]": "MEX",
            "customer[credit_card][billing_address][country_code_numeric]": "484",
            "customer[credit_card][billing_address][country_name]": "Mexico",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Customer.transparent_redirect_create_url())
        result = Customer.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)
        customer = result.customer
        self.assertEquals("John", customer.first_name)
        self.assertEquals("Doe", customer.last_name)
        self.assertEquals("Doe Co", customer.company)
        self.assertEquals("john@doe.com", customer.email)
        self.assertEquals("312.555.2323", customer.phone)
        self.assertEquals("614.555.5656", customer.fax)
        self.assertEquals("www.johndoe.com", customer.website)
        self.assertEquals("05/2012", customer.credit_cards[0].expiration_date)
        self.assertEquals("MX", customer.credit_cards[0].billing_address.country_code_alpha2)
        self.assertEquals("MEX", customer.credit_cards[0].billing_address.country_code_alpha3)
        self.assertEquals("484", customer.credit_cards[0].billing_address.country_code_numeric)
        self.assertEquals("Mexico", customer.credit_cards[0].billing_address.country_name)

    def test_create_from_transparent_redirect_with_error_result(self):
        tr_data = {
            "customer": {
                "company": "Doe Co",
            }
        }
        post_params = {
            "tr_data": Customer.tr_data_for_create(tr_data, "http://example.com/path"),
            "customer[email]": "john#doe.com",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Customer.transparent_redirect_create_url())
        result = Customer.confirm_transparent_redirect(query_string)
        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.Customer.EmailIsInvalid, result.errors.for_object("customer").on("email")[0].code)

    def test_update_from_transparent_redirect_with_successful_result(self):
        customer = Customer.create({
            "first_name": "Jane",
        }).customer

        tr_data = {
            "customer_id": customer.id,
            "customer": {
                "first_name": "John",
            }
        }
        post_params = {
            "tr_data": Customer.tr_data_for_update(tr_data, "http://example.com/path"),
            "customer[email]": "john@doe.com",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Customer.transparent_redirect_update_url())
        result = Customer.confirm_transparent_redirect(query_string)
        self.assertTrue(result.is_success)
        customer = result.customer
        self.assertEquals("John", customer.first_name)
        self.assertEquals("john@doe.com", customer.email)

    def test_update_with_nested_values_via_transparent_redirect(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "10/10",
                "billing_address": {
                    "postal_code": "11111"
                }
            }
        }).customer
        credit_card = customer.credit_cards[0]
        address = credit_card.billing_address

        tr_data = {
            "customer_id": customer.id,
            "customer": {
                "first_name": "Joe",
                "last_name": "Brown",
                "credit_card": {
                    "expiration_date": "12/12",
                    "options": {
                        "update_existing_token": credit_card.token
                    },
                    "billing_address": {
                        "postal_code": "44444",
                        "options": {
                            "update_existing": True
                        }
                    }
                }
            }
        }
        post_params = {
            "tr_data": Customer.tr_data_for_update(tr_data, "http://example.com/path"),
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Customer.transparent_redirect_update_url())
        updated_customer = Customer.confirm_transparent_redirect(query_string).customer
        updated_credit_card = CreditCard.find(credit_card.token)
        updated_address = Address.find(customer.id, address.id)

        self.assertEqual("Joe", updated_customer.first_name)
        self.assertEqual("Brown", updated_customer.last_name)
        self.assertEqual("12/2012", updated_credit_card.expiration_date)
        self.assertEqual("44444", updated_address.postal_code)

    def test_update_from_transparent_redirect_with_error_result(self):
        customer = Customer.create({
            "first_name": "Jane",
        }).customer

        tr_data = {
            "customer_id": customer.id,
            "customer": {
                "first_name": "John",
            }
        }
        post_params = {
            "tr_data": Customer.tr_data_for_update(tr_data, "http://example.com/path"),
            "customer[email]": "john#doe.com",
        }

        query_string = TestHelper.simulate_tr_form_post(post_params, Customer.transparent_redirect_update_url())
        result = Customer.confirm_transparent_redirect(query_string)
        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.Customer.EmailIsInvalid, result.errors.for_object("customer").on("email")[0].code)

    def test_customer_payment_methods(self):
        customer = Customer("gateway", {
            "credit_cards": [ {"token": "credit_card"} ],
            "paypal_accounts": [ {"token": "paypal_account"} ],
            "apple_pay_cards": [ {"token": "apple_pay_card"} ],
            "android_pay_cards": [ {"token": "android_pay_card"} ],
            "europe_bank_accounts": [ {"token": "europe_bank_account"} ],
            "coinbase_accounts": [ {"token": "coinbase_account"} ]
            })

        payment_method_tokens = map(lambda payment_method: payment_method.token, customer.payment_methods)

        self.assertEqual(sorted(payment_method_tokens), ["android_pay_card", "apple_pay_card", "coinbase_account", "credit_card", "europe_bank_account", "paypal_account"])

