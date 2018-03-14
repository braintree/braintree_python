# -*- coding: latin-1 -*-
from tests.test_helper import *
import braintree.test.venmo_sdk as venmo_sdk
from braintree.test.nonces import Nonces

class TestCustomer(unittest.TestCase):
    def test_all(self):
        collection = Customer.all()
        self.assertTrue(collection.maximum_size > 100)
        customer_ids = [c.id for c in collection.items]
        self.assertEqual(collection.maximum_size, len(TestHelper.unique(customer_ids)))
        self.assertEqual(Customer, type(collection.first))

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
        self.assertNotEqual(None, re.search(r"\A\d{6,}\Z", customer.id))

    def test_create_unicode(self):
        result = Customer.create({
            "first_name": "Kimi",
            "last_name": u"Räikkönen",
            "company": "Fake Company",
            "email": "joe@email.com",
            "phone": "312.555.1234",
            "fax": "614.555.5678",
            "website": "www.email.com"
        })

        self.assertTrue(result.is_success)
        customer = result.customer

        self.assertEqual("Kimi", customer.first_name)
        self.assertEqual(u"Räikkönen", customer.last_name)
        self.assertEqual("Fake Company", customer.company)
        self.assertEqual("joe@email.com", customer.email)
        self.assertEqual("312.555.1234", customer.phone)
        self.assertEqual("614.555.5678", customer.fax)
        self.assertEqual("www.email.com", customer.website)
        self.assertNotEqual(None, customer.id)

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
            client_id="client_id$development$integration_client_id",
            client_secret="client_secret$development$integration_client_secret",
            environment=Environment.Development
        )

        code = TestHelper.create_grant(gateway, {
            "merchant_public_id": "integration_merchant_id",
            "scope": "read_write"
        })

        result = gateway.oauth.create_token_from_code({
            "code": code
        })

        gateway = BraintreeGateway(
            access_token=result.credentials.access_token,
            environment=Environment.Development
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
        self.assertNotEqual(None, re.search(r"\A\d{6,}\Z", customer.id))

        found_customer = Customer.find(customer.id)
        self.assertEqual(u"G\u1f00t\u1F18s", found_customer.last_name)

    def test_create_with_apple_pay_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.ApplePayVisa})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.apple_pay_cards))
        self.assertIsInstance(customer.apple_pay_cards[0], ApplePayCard)

    def test_create_with_android_pay_proxy_card_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.AndroidPayCardDiscover})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.android_pay_cards))
        self.assertIsInstance(customer.android_pay_cards[0], AndroidPayCard)

    def test_create_with_android_pay_network_token_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.AndroidPayCardMasterCard})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.android_pay_cards))
        self.assertIsInstance(customer.android_pay_cards[0], AndroidPayCard)

    def test_create_with_amex_express_checkout_card_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.AmexExpressCheckoutCard})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.amex_express_checkout_cards))
        self.assertIsInstance(customer.amex_express_checkout_cards[0], AmexExpressCheckoutCard)

    def test_create_with_venmo_account_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.VenmoAccount})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.venmo_accounts))
        self.assertIsInstance(customer.venmo_accounts[0], VenmoAccount)

    def test_create_with_us_bank_account_nonce(self):
        result = Customer.create({
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "credit_card": {
                "options": {
                    "verification_merchant_account_id": "us_bank_merchant_account"
                }
            }
        })
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.us_bank_accounts))
        self.assertIsInstance(customer.us_bank_accounts[0], UsBankAccount)

    def test_create_with_paypal_future_payments_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.PayPalFuturePayment})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.paypal_accounts))
        self.assertIsInstance(customer.paypal_accounts[0], PayPalAccount)

    def test_create_with_paypal_order_payment_nonce(self):
        http = ClientApiHttp.create()
        status_code, payment_method_nonce = http.get_paypal_nonce({
            "intent": "order",
            "payment-token": "fake-paypal-payment-token",
            "payer-id": "fake-paypal-payer-id"
        })

        result = Customer.create({"payment_method_nonce": payment_method_nonce})
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.paypal_accounts))
        self.assertIsInstance(customer.paypal_accounts[0], PayPalAccount)

    def test_create_with_paypal_order_payment_nonce_and_paypal_options(self):
        http = ClientApiHttp.create()
        status_code, payment_method_nonce = http.get_paypal_nonce({
            "intent": "order",
            "payment-token": "fake-paypal-payment-token",
            "payer-id": "fake-paypal-payer-id"
        })

        result = Customer.create({
            "payment_method_nonce": payment_method_nonce,
            "options": {
                "paypal": {
                    "payee_email": "payee@example.com",
                    "order_id": "merchant-order-id",
                    "custom_field": "custom merchant field",
                    "description": "merchant description",
                    "amount": "1.23",
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
                    },
                },
            },
        })
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.paypal_accounts))
        self.assertIsInstance(customer.paypal_accounts[0], PayPalAccount)

    def test_create_with_paypal_one_time_nonce_fails(self):
        result = Customer.create({"payment_method_nonce": Nonces.PayPalOneTimePayment})
        self.assertFalse(result.is_success)

        paypal_account_errors = result.errors.for_object("customer").for_object("paypal_account").on("base")
        self.assertEqual(1, len(paypal_account_errors))
        self.assertEqual(ErrorCodes.PayPalAccount.CannotVaultOneTimeUsePayPalAccount, paypal_account_errors[0].code)

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

        customer_email_errors = result.errors.for_object("customer").on("email")
        self.assertEqual(1, len(customer_email_errors))
        self.assertEqual(ErrorCodes.Customer.EmailIsInvalid, customer_email_errors[0].code)

        billing_address_errors = result.errors.for_object("customer").for_object("credit_card").for_object("billing_address").on("base")
        self.assertEqual(1, len(billing_address_errors))
        self.assertEqual(ErrorCodes.Address.InconsistentCountry, billing_address_errors[0].code)

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
        self.assertEqual(CreditCardVerification.Status.ProcessorDeclined, result.credit_card_verification.status)

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
        self.assertEqual("Duplicate card exists in the vault.", result.message)

        card_number_errors = result.errors.for_object("customer").for_object("credit_card").on("number")
        self.assertEqual(1, len(card_number_errors))
        self.assertEqual(ErrorCodes.CreditCard.DuplicateCardExists, card_number_errors[0].code)

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
        self.assertEqual("custom value", result.customer.custom_fields["store_me"])

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

        email_errors = result.errors.for_object("customer").on("email")
        self.assertEqual(1, len(email_errors))
        self.assertEqual(ErrorCodes.Customer.EmailIsInvalid, email_errors[0].code)

        card_number_errors = result.errors.for_object("customer").for_object("credit_card").on("number")
        self.assertEqual(1, len(card_number_errors))
        self.assertEqual(ErrorCodes.CreditCard.NumberHasInvalidLength, card_number_errors[0].code)

        country_name_errors = result.errors.for_object("customer").for_object("credit_card").for_object("billing_address").on("country_name")
        self.assertEqual(1, len(country_name_errors))
        self.assertEqual(ErrorCodes.Address.CountryNameIsNotAccepted, country_name_errors[0].code)

    def test_create_returns_errors_if_custom_fields_are_not_registered(self):
        result = Customer.create({
            "first_name": "Jack",
            "last_name": "Kennedy",
            "custom_fields": {
                "spouse_name": "Jacqueline"
            }
        })

        self.assertFalse(result.is_success)

        custom_fields_errors = result.errors.for_object("customer").on("custom_fields")
        self.assertEqual(1, len(custom_fields_errors))
        self.assertEqual(ErrorCodes.Customer.CustomFieldIsInvalid, custom_fields_errors[0].code)

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
        self.assertFalse(result.customer.credit_cards[0].venmo_sdk)

    def test_create_with_venmo_sdk_payment_method_code(self):
        result = Customer.create({
            "first_name": "Jack",
            "last_name": "Kennedy",
            "credit_card": {
                "venmo_sdk_payment_method_code": venmo_sdk.generate_test_payment_method_code("4111111111111111")
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual("411111", result.customer.credit_cards[0].bin)

    def test_create_with_payment_method_nonce(self):
        config = Configuration.instantiate()
        authorization_fingerprint = json.loads(TestHelper.generate_decoded_client_token())["authorizationFingerprint"]
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

        result = Customer.create({
            "credit_card": {
                "payment_method_nonce": nonce
            }
        })

        self.assertTrue(result.is_success)
        self.assertEqual("411111", result.customer.credit_cards[0].bin)

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
        self.assertEqual(customer.id, found_customer.id)
        self.assertEqual(customer.first_name, found_customer.first_name)
        self.assertEqual(customer.last_name, found_customer.last_name)

    def test_find_customer_with_us_bank_account(self):
        customer = Customer.create({
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "credit_card": {
                "options": {
                    "verification_merchant_account_id": "us_bank_merchant_account"
                }
            }
        }).customer

        found_customer = Customer.find(customer.id)
        self.assertEqual(customer.id, found_customer.id)
        self.assertEqual(customer.first_name, found_customer.first_name)
        self.assertEqual(customer.last_name, found_customer.last_name)
        self.assertEqual(1, len(found_customer.us_bank_accounts))
        self.assertIsInstance(found_customer.us_bank_accounts[0], UsBankAccount)

    @raises_with_regexp(NotFoundError, "customer with id 'badid' not found")
    def test_find_with_invalid_customer(self):
        Customer.find("badid")

    def test_find_customer_with_all_filterable_associations_filtered_out(self):
        customer = Customer.create({
            "custom_fields": {
                "store_me": "custom value"
            }
        }).customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "billing_address": {
                "street_address": "123 Abc Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60622",
                "country_name": "United States of America"
            }
        }).credit_card
        subscription_id = "id_" + str(random.randint(1, 1000000))
        subscription = Subscription.create({
            "id": subscription_id,
            "plan_id": "integration_trialless_plan",
            "payment_method_token": credit_card.token,
            "price": Decimal("1.00")
        }).subscription

        found_customer = Customer.find(customer.id, "customernoassociations")
        self.assertEqual(len(found_customer.credit_cards), 0)
        self.assertEqual(len(found_customer.payment_methods), 0)
        self.assertEqual(len(found_customer.addresses), 0)
        self.assertEqual(len(found_customer.custom_fields), 0)

    def test_find_customer_with_nested_filterable_associations_filtered_out(self):
        customer = Customer.create({
            "custom_fields": {
                "store_me": "custom value"
            }
        }).customer
        credit_card = CreditCard.create({
            "customer_id": customer.id,
            "number": "4111111111111111",
            "expiration_date": "05/2014",
            "billing_address": {
                "street_address": "123 Abc Way",
                "locality": "Chicago",
                "region": "Illinois",
                "postal_code": "60622",
                "country_name": "United States of America"
            }
        }).credit_card
        subscription_id = "id_" + str(random.randint(1, 1000000))
        subscription = Subscription.create({
            "id": subscription_id,
            "plan_id": "integration_trialless_plan",
            "payment_method_token": credit_card.token,
            "price": Decimal("1.00")
        }).subscription

        found_customer = Customer.find(customer.id, "customertoplevelassociations")
        self.assertEqual(len(found_customer.credit_cards), 1)
        self.assertEqual(len(found_customer.credit_cards[0].subscriptions), 0)
        self.assertEqual(len(found_customer.payment_methods), 1)
        self.assertEqual(len(found_customer.payment_methods[0].subscriptions), 0)
        self.assertEqual(len(found_customer.addresses), 1)
        self.assertEqual(len(found_customer.custom_fields), 1)

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
        self.assertNotEqual(None, re.search(r"\A\d{6,}\Z", customer.id))

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

        Customer.update(customer.id, {
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

        email_errors = result.errors.for_object("customer").on("email")
        self.assertEqual(1, len(email_errors))
        self.assertEqual(ErrorCodes.Customer.EmailIsInvalid, email_errors[0].code)

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

        paypal_account_errors = result.errors.for_object("customer").for_object("paypal_account").on("base")
        self.assertEqual(1, len(paypal_account_errors))
        self.assertEqual(ErrorCodes.PayPalAccount.CannotVaultOneTimeUsePayPalAccount, paypal_account_errors[0].code)


    def test_update_with_paypal_order_nonce(self):
        customer = Customer.create().customer

        http = ClientApiHttp.create()
        status_code, payment_method_nonce = http.get_paypal_nonce({
            "intent": "order",
            "payment-token": "fake-paypal-payment-token",
            "payer-id": "fake-paypal-payer-id"
        })

        result = Customer.update(customer.id, {
            "payment_method_nonce": payment_method_nonce,
            "options": {
                "paypal": {
                    "payee_email": "payee@example.com",
                    "order_id": "merchant-order-id",
                    "custom_field": "custom merchant field",
                    "description": "merchant description",
                    "amount": "1.23",
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
                    },
                },
            },
        })

        self.assertTrue(result.is_success)
        customer = result.customer
        self.assertNotEqual(None, customer.paypal_accounts[0])
        self.assertEqual(1, len(customer.paypal_accounts))
        self.assertIsInstance(customer.paypal_accounts[0], PayPalAccount)

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
        self.assertEqual("John", customer.first_name)
        self.assertEqual("Doe", customer.last_name)
        self.assertEqual("Doe Co", customer.company)
        self.assertEqual("john@doe.com", customer.email)
        self.assertEqual("312.555.2323", customer.phone)
        self.assertEqual("614.555.5656", customer.fax)
        self.assertEqual("www.johndoe.com", customer.website)
        self.assertEqual("05/2012", customer.credit_cards[0].expiration_date)
        self.assertEqual("MX", customer.credit_cards[0].billing_address.country_code_alpha2)
        self.assertEqual("MEX", customer.credit_cards[0].billing_address.country_code_alpha3)
        self.assertEqual("484", customer.credit_cards[0].billing_address.country_code_numeric)
        self.assertEqual("Mexico", customer.credit_cards[0].billing_address.country_name)

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

        email_errors = result.errors.for_object("customer").on("email")
        self.assertEqual(1, len(email_errors))
        self.assertEqual(ErrorCodes.Customer.EmailIsInvalid, email_errors[0].code)

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
        self.assertEqual("John", customer.first_name)
        self.assertEqual("john@doe.com", customer.email)

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

        customer_email_errors = result.errors.for_object("customer").on("email")
        self.assertEqual(1, len(customer_email_errors))
        self.assertEqual(ErrorCodes.Customer.EmailIsInvalid, customer_email_errors[0].code)

    def test_customer_payment_methods(self):
        customer = Customer("gateway", {
            "credit_cards": [{"token": "credit_card"}],
            "paypal_accounts": [{"token": "paypal_account"}],
            "apple_pay_cards": [{"token": "apple_pay_card"}],
            "android_pay_cards": [{"token": "android_pay_card"}],
            "europe_bank_accounts": [{"token": "europe_bank_account"}],
            "us_bank_accounts": [{"token": "us_bank_account"}]
            })

        payment_method_tokens = [ pm.token for pm in customer.payment_methods ]

        self.assertEqual(sorted(payment_method_tokens), ["android_pay_card", "apple_pay_card", "credit_card", "europe_bank_account", "paypal_account", "us_bank_account"])
