# -*- coding: latin-1 -*-
from tests.test_helper import *
from braintree.test.nonces import Nonces

class TestCustomer(unittest.TestCase):
    @unittest.skip("skip until CI is more stable")
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
            "international_phone": {"country_code": "1", "national_number": "3121234567"},
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
        self.assertEqual("1", customer.international_phone["country_code"])
        self.assertEqual("3121234567", customer.international_phone["national_number"])
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

    def test_create_with_tax_identifiers(self):
        result = Customer.create({
            "tax_identifiers": [
                {"country_code": "US", "identifier": "123456789"},
                {"country_code": "GB", "identifier": "987654321"}]
            })

        self.assertTrue(result.is_success)

    def test_create_with_device_data(self):
        result = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "company": "Fake Company",
            "email": "joe@email.com",
            "phone": "312.555.1234",
            "fax": "614.555.5678",
            "website": "www.email.com",
            "device_data": "abc123",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
                }
            })

        self.assertTrue(result.is_success)

    def test_create_with_device_session_id_and_fraud_merchant_id_sends_deprecation_warning(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = Customer.create({
                "first_name": "Joe",
                "last_name": "Brown",
                "company": "Fake Company",
                "email": "joe@email.com",
                "phone": "312.555.1234",
                "fax": "614.555.5678",
                "website": "www.email.com",
                "device_session_id": "abc123",
                "fraud_merchant_id": "456",
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "05/2010",
                    "cvv": "100"
                    }
                })

            self.assertTrue(result.is_success)
            assert len(w) > 0
            assert issubclass(w[-1].category, DeprecationWarning)

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

    def test_create_includes_risk_data_when_skip_advanced_fraud_checking_is_false(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            result = Customer.create({
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "05/2014",
                    "options": {
                        "verify_card": True,
                        "skip_advanced_fraud_checking": False
                        },
                    },
                })

            self.assertTrue(result.is_success)
            verification = result.customer.credit_cards[0].verification
            self.assertIsInstance(verification.risk_data, RiskData)

    def test_create_does_not_include_risk_data_when_skip_advanced_fraud_checking_is_true(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            result = Customer.create({
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "05/2014",
                    "options": {
                        "verify_card": True,
                        "skip_advanced_fraud_checking": True
                        },
                    },
                })

            self.assertTrue(result.is_success)
            verification = result.customer.credit_cards[0].verification
            self.assertIsNone(verification.risk_data)

    def test_create_and_update_with_verification_account_type(self):
        result_with_account_type_credit = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "credit_card": {
                "number": CreditCardNumbers.Hiper,
                "expiration_date": "05/2010",
                "options": {
                    "verify_card": True,
                    "verification_merchant_account_id": "hiper_brl",
                    "verification_account_type": "credit",
                    }
                },
            })

        update_with_account_type_credit = Customer.update(result_with_account_type_credit.customer.id, {
            "credit_card": {
                "number": CreditCardNumbers.Hiper,
                "expiration_date": "05/2010",
                "options": {
                    "verification_account_type": "credit",
                    }
                },
            })

        result_with_account_type_debit = Customer.create({
            "first_name": "Joe",
            "last_name": "Brown",
            "credit_card": {
                "number": CreditCardNumbers.Hiper,
                "expiration_date": "05/2010",
                "options": {
                    "verify_card": True,
                    "verification_merchant_account_id": TestHelper.card_processor_brl_merchant_account_id,
                    "verification_account_type": "debit",
                    }
                },
            })

        update_with_account_type_debit = Customer.update(result_with_account_type_debit.customer.id, {
            "credit_card": {
                "number": CreditCardNumbers.Hiper,
                "expiration_date": "05/2010",
                "options": {
                    "verification_account_type": "debit",
                    }
                },
            })

        self.assertTrue(result_with_account_type_credit.is_success)
        self.assertTrue(result_with_account_type_debit.is_success)
        self.assertTrue(update_with_account_type_credit.is_success)
        self.assertTrue(update_with_account_type_debit.is_success)

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
        self.assertNotEqual(customer.apple_pay_cards[0].bin, None)
        self.assertNotEqual(customer.apple_pay_cards[0].card_type, None)
        self.assertNotEqual(customer.apple_pay_cards[0].commercial, None)
        self.assertNotEqual(customer.apple_pay_cards[0].country_of_issuance, None)
        self.assertNotEqual(customer.apple_pay_cards[0].debit, None)
        self.assertNotEqual(customer.apple_pay_cards[0].durbin_regulated, None)
        self.assertNotEqual(customer.apple_pay_cards[0].healthcare, None)
        self.assertNotEqual(customer.apple_pay_cards[0].issuing_bank, None)
        self.assertNotEqual(customer.apple_pay_cards[0].last_4, None)
        self.assertNotEqual(customer.apple_pay_cards[0].payroll, None)
        self.assertNotEqual(customer.apple_pay_cards[0].prepaid, None)
        self.assertNotEqual(customer.apple_pay_cards[0].prepaid_reloadable, None)
        self.assertNotEqual(customer.apple_pay_cards[0].product_id, None)
        self.assertNotEqual(customer.apple_pay_cards[0].token, None)

    def test_create_with_three_d_secure_nonce(self):
        result = Customer.create({
            "payment_method_nonce": Nonces.ThreeDSecureVisaFullAuthentication,
            "credit_card": {
                "options": {
                    "verify_card": True,
                    },
            },
        })

        self.assertTrue(result.is_success)

        three_d_secure_info = result.customer.payment_methods[0].verification.three_d_secure_info

        self.assertEqual("authenticate_successful", three_d_secure_info.status)
        self.assertEqual(True, three_d_secure_info.liability_shifted)
        self.assertEqual(True, three_d_secure_info.liability_shift_possible)
        self.assertIsInstance(three_d_secure_info.enrolled, str)
        self.assertIsInstance(three_d_secure_info.cavv, str)
        self.assertIsInstance(three_d_secure_info.xid, str)
        self.assertIsInstance(three_d_secure_info.eci_flag, str)
        self.assertIsInstance(three_d_secure_info.three_d_secure_version, str)

    def test_create_with_three_d_secure_pass_thru(self):
        result = Customer.create({
            "payment_method_nonce": Nonces.Transactable,
            "credit_card": {
                "three_d_secure_pass_thru": {
                    "three_d_secure_version": "1.1.1",
                    "eci_flag": "05",
                    "cavv": "some-cavv",
                    "xid": "some-xid"
                    },
                "options": {
                    "verify_card": True,
                    },
                },
            })

        self.assertTrue(result.is_success)

    def test_create_with_three_d_secure_pass_thru_without_eci_flag(self):
        result = Customer.create({
            "payment_method_nonce": Nonces.Transactable,
            "credit_card": {
                "three_d_secure_pass_thru": {
                    "three_d_secure_version": "1.1.1",
                    "cavv": "some-cavv",
                    "xid": "some-xid"
                    },
                "options": {
                    "verify_card": True,
                    },
            },
        })

        self.assertFalse(result.is_success)
        self.assertEqual("EciFlag is required.", result.message)

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
        self.assertNotEqual(customer.android_pay_cards[0].bin, None)
        self.assertNotEqual(customer.android_pay_cards[0].card_type, None)
        self.assertNotEqual(customer.android_pay_cards[0].commercial, None)
        self.assertNotEqual(customer.android_pay_cards[0].country_of_issuance, None)
        self.assertNotEqual(customer.android_pay_cards[0].debit, None)
        self.assertNotEqual(customer.android_pay_cards[0].durbin_regulated, None)
        self.assertNotEqual(customer.android_pay_cards[0].healthcare, None)
        self.assertNotEqual(customer.android_pay_cards[0].issuing_bank, None)
        self.assertNotEqual(customer.android_pay_cards[0].last_4, None)
        self.assertNotEqual(customer.android_pay_cards[0].payroll, None)
        self.assertNotEqual(customer.android_pay_cards[0].prepaid, None)
        self.assertNotEqual(customer.android_pay_cards[0].prepaid_reloadable, None)
        self.assertNotEqual(customer.android_pay_cards[0].product_id, None)
        self.assertNotEqual(customer.android_pay_cards[0].token, None)

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
                    "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id
                }
            }
        })
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertEqual(1, len(customer.us_bank_accounts))
        self.assertIsInstance(customer.us_bank_accounts[0], UsBankAccount)

    def test_create_with_paypal_billing_agreements_nonce(self):
        result = Customer.create({"payment_method_nonce": Nonces.PayPalBillingAgreement})
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

    def test_create_for_raw_apple_pay(self):
        result = Customer.create({
            "first_name": "Rickey",
            "last_name": "Crabapple",
            "apple_pay_card": {
                "number": "4111111111111111",
                "expiration_month": "05",
                "expiration_year": "2014",
                "eci_indicator": "5",
                "cryptogram": "01010101010101010101",
                "cardholder_name": "John Doe",
                "billing_address": {
                    "postal_code": 83704
                }
            }
        })

        customer = result.customer
        self.assertEqual("Rickey", customer.first_name)
        self.assertEqual("Crabapple", customer.last_name)

        self.assertTrue(result.is_success)
        apple_pay_card = result.customer.apple_pay_cards[0]
        self.assertEqual("411111", apple_pay_card.bin)
        self.assertEqual("1111", apple_pay_card.last_4)
        self.assertEqual("2014", apple_pay_card.expiration_year)
        self.assertEqual("05", apple_pay_card.expiration_month)
        self.assertEqual(apple_pay_card.billing_address["postal_code"], "83704")

    def test_create_for_raw_apple_pay_with_invalid_params(self):
        result = Customer.create({
            "first_name": "Rickey",
            "last_name": "Crabapple",
            "apple_pay_card": {
                "number": "4111111111111111",
                "expiration_year": "2014",
                "expiration_month": "01",
                "eci_indicator": "5",
                "cryptogram": "01010101010101010101",
                "cardholder_name": "John Doe",
                "billing_address": {
                    "street_address": "head 100 yds south once you hear the beehive",
                    "postal_code": '$$$$',
                    "country_code_alpha2": "UX",
                }
            }
        })
#
        errors = result.errors.for_object("apple_pay").on("billing_address")
        self.assertFalse(result.is_success)

        postal_errors = result.errors.for_object("apple_pay").for_object("billing_address").on("postal_code")
        country_errors = result.errors.for_object("apple_pay").for_object("billing_address").on("country_code_alpha2")
        self.assertEqual(1, len(postal_errors))
        self.assertEqual(1, len(country_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted, country_errors[0].code)
        self.assertEqual(ErrorCodes.Address.PostalCodeInvalidCharacters, postal_errors[0].code)

    def test_create_for_raw_android_pay_card(self):
        result = Customer.create({
            "first_name": "Rickey",
            "last_name": "Crabapple",
            "android_pay_card": {
                "number": "4111111111111111",
                "expiration_month": "05",
                "expiration_year": "2014",
                "google_transaction_id": "dontbeevil",
                "billing_address": {
                    "postal_code": 83704
                }
            }
        })

        customer = result.customer
        self.assertEqual("Rickey", customer.first_name)
        self.assertEqual("Crabapple", customer.last_name)

        self.assertTrue(result.is_success)
        android_pay_card = result.customer.android_pay_cards[0]
        self.assertEqual("411111", android_pay_card.bin)
        self.assertEqual("1111", android_pay_card.last_4)
        self.assertEqual("2014", android_pay_card.expiration_year)
        self.assertEqual("05", android_pay_card.expiration_month)
        self.assertEqual("dontbeevil", android_pay_card.google_transaction_id)
        self.assertEqual(android_pay_card.billing_address["postal_code"], "83704")

    def test_create_for_raw_android_pay_card_with_invalid_params(self):
        result = Customer.create({
            "first_name": "Rickey",
            "last_name": "Crabapple",
            "android_pay_card": {
                "number": "4111111111111111",
                "expiration_year": "2014",
                "expiration_month": "01",
                "google_transaction_id": "dontbeevil",
                "billing_address": {
                    "street_address": "head 100 yds south once you hear the beehive",
                    "postal_code": '$$$$',
                    "country_code_alpha2": "UX",
                }
            }
        })

        errors = result.errors.for_object("android_pay_card").on("billing_address")
        self.assertFalse(result.is_success)

        postal_errors = result.errors.for_object("android_pay_card").for_object("billing_address").on("postal_code")
        country_errors = result.errors.for_object("android_pay_card").for_object("billing_address").on("country_code_alpha2")
        self.assertEqual(1, len(postal_errors))
        self.assertEqual(1, len(country_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted, country_errors[0].code)
        self.assertEqual(ErrorCodes.Address.PostalCodeInvalidCharacters, postal_errors[0].code)

    def test_create_for_raw_android_pay_network_token(self):
        result = Customer.create({
            "first_name": "Rickey",
            "last_name": "Crabapple",
            "android_pay_network_token": {
                "number": "4111111111111111",
                "expiration_month": "05",
                "expiration_year": "2014",
                "cryptogram": "01010101010101010101",
                "eci_indicator": "5",
                "google_transaction_id": "dontbeevil",
                "billing_address": {
                    "postal_code": 83704
                }
            }
        })
        customer = result.customer
        self.assertEqual("Rickey", customer.first_name)
        self.assertEqual("Crabapple", customer.last_name)

        self.assertTrue(result.is_success)
        android_pay_network_token = result.customer.android_pay_cards[0]
        self.assertEqual("411111", android_pay_network_token.bin)
        self.assertEqual("1111", android_pay_network_token.last_4)
        self.assertEqual("2014", android_pay_network_token.expiration_year)
        self.assertEqual("05", android_pay_network_token.expiration_month)
        self.assertEqual("dontbeevil", android_pay_network_token.google_transaction_id)
        self.assertEqual(android_pay_network_token.billing_address["postal_code"], "83704")

    def test_create_for_raw_android_pay_network_token_with_invalid_params(self):
        result = Customer.create({
            "first_name": "Rickey",
            "last_name": "Crabapple",
            "android_pay_network_token": {
                "number": "4111111111111111",
                "expiration_year": "2014",
                "expiration_month": "01",
                "google_transaction_id": "dontbeevil",
                "cryptogram": "01010101010101010101",
                "cardholder_name": "John Doe",
                "billing_address": {
                    "street_address": "head 100 yds south once you hear the beehive",
                    "postal_code": '$$$$',
                    "country_code_alpha2": "UX",
                }
            }
        })

        errors = result.errors.for_object("android_pay_network_token").on("billing_address")
        self.assertFalse(result.is_success)

        postal_errors = result.errors.for_object("android_pay_network_token").for_object("billing_address").on("postal_code")
        country_errors = result.errors.for_object("android_pay_network_token").for_object("billing_address").on("country_code_alpha2")
        self.assertEqual(1, len(postal_errors))
        self.assertEqual(1, len(country_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted, country_errors[0].code)
        self.assertEqual(ErrorCodes.Address.PostalCodeInvalidCharacters, postal_errors[0].code)

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

    def test_create_customer_with_check_duplicate_payment_method_for_customer(self):
        attributes = {
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4000111111111115",
                "expiration_date": "05/2010",
                "cvv": "100",
            }
        }

        customer = Customer.create(attributes).customer
        result = Customer.update(customer.id, {
            "credit_card": {
                "expiration_date": "12/12",
                "number": "4000111111111115",
                "options": {"fail_on_duplicate_payment_method_for_customer": True}
            }
        })

        self.assertFalse(result.is_success)
        self.assertEqual("Duplicate card exists in the vault for the customer.", result.message)

        card_number_errors = result.errors.for_object("customer").for_object("credit_card").on("number")
        self.assertEqual(1, len(card_number_errors))
        self.assertEqual(ErrorCodes.CreditCard.DuplicateCardExistsForCustomer, card_number_errors[0].code)

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

    def test_delete_with_invalid_customer(self):
        with self.assertRaises(NotFoundError):
            customer = Customer.create().customer
            Customer.delete(customer.id)
            Customer.delete(customer.id)

    def test_delete_payment_method_with_path_traversal(self):
        try:
            customer = Customer.create().customer
            credit_card = CreditCard.create({
                "customer_id": customer.id,
                "number": "4111111111111111",
                "expiration_date": "05/2009",
                "cvv": "100",
                "cardholder_name": "John Doe"
            }).credit_card
            Customer.delete("../payment_methods/any/{}".format(credit_card.token))
        except NotFoundError:
            pass

        payment_method = PaymentMethod.find(credit_card.token)
        self.assertNotEqual(None, payment_method)
        self.assertEqual(credit_card.token, payment_method.token)
        self.assertEqual(credit_card.customer_id, payment_method.customer_id)
        self.assertEqual("John Doe", payment_method.cardholder_name)

    def test_find_with_valid_customer(self):
        customer = Customer.create({
            "first_name": "Joe",
            "last_name": "Cool"
        }).customer

        found_customer = Customer.find(customer.id)
        self.assertEqual(customer.id, found_customer.id)
        self.assertEqual(customer.first_name, found_customer.first_name)
        self.assertEqual(customer.last_name, found_customer.last_name)
        self.assertNotEqual(None, customer.graphql_id)

    def test_find_customer_with_us_bank_account(self):
        customer = Customer.create({
            "payment_method_nonce": TestHelper.generate_valid_us_bank_account_nonce(),
            "credit_card": {
                "options": {
                    "verification_merchant_account_id": TestHelper.us_bank_merchant_account_id
                }
            }
        }).customer

        found_customer = Customer.find(customer.id)
        self.assertEqual(customer.id, found_customer.id)
        self.assertEqual(customer.first_name, found_customer.first_name)
        self.assertEqual(customer.last_name, found_customer.last_name)
        self.assertEqual(1, len(found_customer.us_bank_accounts))
        self.assertIsInstance(found_customer.us_bank_accounts[0], UsBankAccount)

    def test_find_with_invalid_customer(self):
        with self.assertRaisesRegex(NotFoundError, "customer with id 'badid' not found"):
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
            "international_phone": {"country_code": "1", "national_number": "3121234567"},
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
        self.assertEqual("1", customer.international_phone["country_code"])
        self.assertEqual("3121234567", customer.international_phone["national_number"])
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
            "payment_method_nonce": Nonces.PayPalBillingAgreement
        })
        self.assertTrue(result.is_success)

        customer = result.customer
        self.assertNotEqual(None, customer.paypal_accounts[0])

    def test_update_with_invalid_three_d_secure_pass_thru_params(self):
        customer = Customer.create().customer
        result = Customer.update(customer.id, {
            "payment_method_nonce": Nonces.Transactable,
            "credit_card": {
                "three_d_secure_pass_thru": {
                    "eci_flag": "05",
                    "cavv": "some-cavv",
                    "xid": "some-xid"
                    },
                "options": {
                    "verify_card": True,
                    },
                },
            })
        self.assertFalse(result.is_success)
        self.assertEqual("ThreeDSecureVersion is required.", result.message)

    def test_update_with_valid_three_d_secure_pass_thru_params(self):
        customer = Customer.create().customer
        result = Customer.update(customer.id, {
            "payment_method_nonce": Nonces.Transactable,
            "credit_card": {
                "three_d_secure_pass_thru": {
                    "eci_flag": "05",
                    "cavv": "some-cavv",
                    "three_d_secure_version": "1.2.0",
                    "xid": "some-xid"
                    },
                "options": {
                    "verify_card": True,
                    },
                },
            })
        self.assertTrue(result.is_success)

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

    def test_update_includes_risk_data_when_skip_advanced_fraud_checking_is_false(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            customer = Customer.create().customer

            result = Customer.update(customer.id, {
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "05/2014",
                    "cvv": "100",
                    "cardholder_name": "John Doe",
                    "options": {
                        "verify_card": True,
                        "skip_advanced_fraud_checking": False
                        }
                    }
                })

            self.assertTrue(result.is_success)
            verification = result.customer.credit_cards[0].verification
            self.assertIsInstance(verification.risk_data, RiskData)

    def test_update_does_not_include_risk_data_when_skip_advanced_fraud_checking_is_true(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            customer = Customer.create().customer

            result = Customer.update(customer.id, {
                "credit_card": {
                    "number": "4111111111111111",
                    "expiration_date": "05/2014",
                    "cvv": "100",
                    "cardholder_name": "John Doe",
                    "options": {
                        "verify_card": True,
                        "skip_advanced_fraud_checking": True
                        }
                    }
                })

            self.assertTrue(result.is_success)
            verification = result.customer.credit_cards[0].verification
            self.assertIsNone(verification.risk_data)

    def test_update_works_for_raw_apple_pay(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            customer = Customer.create().customer
            secure_token = TestHelper.random_token_block(None)

            result = Customer.update(customer.id, {
                "apple_pay_card": {
                    "number": "4111111111111111",
                    "expiration_month": "05",
                    "expiration_year": "2014",
                    "eci_indicator": "0",
                    "cryptogram": "01010101010101010101",
                    "cardholder_name": "John Doe",
                    "token": secure_token,
                    "options": {
                        "make_default": True
                    },
                    "billing_address": {
                        "street_address": "123 Abc Way",
                        "locality": "Chicago",
                        "region": "Illinois",
                        "postal_code": "60622",
                        "phone_number": "312.555.1234",
                        "country_code_alpha2": "US",
                        "country_code_alpha3": "USA",
                        "country_code_numeric": "840",
                        "country_name": "United States of America"
                    }
                },
            })

            self.assertTrue(result.is_success)
            self.assertEqual(secure_token, result.customer.payment_methods[0].token)

            self.assertNotEqual(0, len(result.customer.apple_pay_cards))
            apple_pay_card = result.customer.apple_pay_cards[0]
            self.assertTrue(apple_pay_card.default)
            self.assertEqual(apple_pay_card.expiration_month, "05")
            self.assertEqual(apple_pay_card.expiration_year, "2014")
            self.assertEqual(apple_pay_card.cardholder_name, "John Doe")
            self.assertEqual(apple_pay_card.bin, "411111")

            self.assertEqual(apple_pay_card.billing_address["street_address"], "123 Abc Way")
            self.assertEqual(apple_pay_card.billing_address["locality"], "Chicago")
            self.assertEqual(apple_pay_card.billing_address["region"], "Illinois")
            self.assertEqual(apple_pay_card.billing_address["postal_code"], "60622")
            self.assertEqual(apple_pay_card.billing_address["phone_number"], "312.555.1234")
            self.assertEqual(apple_pay_card.billing_address["country_code_alpha2"], "US")
            self.assertEqual(apple_pay_card.billing_address["country_code_alpha3"], "USA")
            self.assertEqual(apple_pay_card.billing_address["country_code_numeric"], "840")
            self.assertEqual(apple_pay_card.billing_address["country_name"], "United States of America")

    def test_update_works_for_raw_android_pay_card(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            customer = Customer.create().customer
            secure_token = TestHelper.random_token_block(None)

            result = Customer.update(customer.id, {
                "android_pay_card": {
                    "number": "4111111111111111",
                    "expiration_month": "05",
                    "expiration_year": "2014",
                    "google_transaction_id": "iliketurtles",
                    "token": secure_token,
                    "options": {
                        "make_default": True
                    },
                    "billing_address": {
                        "street_address": "123 Abc Way",
                        "locality": "Chicago",
                        "region": "Illinois",
                        "postal_code": "60622",
                        "phone_number": "312.555.1234",
                        "country_code_alpha2": "US",
                        "country_code_alpha3": "USA",
                        "country_code_numeric": "840",
                        "country_name": "United States of America"
                    }
                },
            })

            self.assertTrue(result.is_success)
            self.assertEqual(secure_token, result.customer.payment_methods[0].token)

            self.assertNotEqual(0, len(result.customer.android_pay_cards))
            android_pay_card = result.customer.android_pay_cards[0]
            self.assertTrue(android_pay_card.default)
            self.assertEqual(android_pay_card.expiration_month, "05")
            self.assertEqual(android_pay_card.expiration_year, "2014")
            self.assertEqual(android_pay_card.google_transaction_id, "iliketurtles")
            self.assertEqual(android_pay_card.bin, "411111")

            self.assertEqual(android_pay_card.billing_address["street_address"], "123 Abc Way")
            self.assertEqual(android_pay_card.billing_address["locality"], "Chicago")
            self.assertEqual(android_pay_card.billing_address["region"], "Illinois")
            self.assertEqual(android_pay_card.billing_address["postal_code"], "60622")
            self.assertEqual(android_pay_card.billing_address["phone_number"], "312.555.1234")
            self.assertEqual(android_pay_card.billing_address["country_code_alpha2"], "US")
            self.assertEqual(android_pay_card.billing_address["country_code_alpha3"], "USA")
            self.assertEqual(android_pay_card.billing_address["country_code_numeric"], "840")
            self.assertEqual(android_pay_card.billing_address["country_name"], "United States of America")

    def test_update_for_raw_android_pay_card_with_invalid_params(self):
        customer = Customer.create().customer
        secure_token = TestHelper.random_token_block(None)

        result = Customer.update(customer.id, {
            "first_name": "Rickey",
            "last_name": "Crabapple",
            "android_pay_card": {
                "number": "4111111111111111",
                "expiration_year": "2014",
                "expiration_month": "01",
                "google_transaction_id": "dontbeevil",
                "billing_address": {
                    "street_address": "head 100 yds south once you hear the beehive",
                    "postal_code": '$$$$',
                    "country_code_alpha2": "UX",
                }
            }
        })

        errors = result.errors.for_object("android_pay_card").on("billing_address")
        self.assertFalse(result.is_success)

        postal_errors = result.errors.for_object("android_pay_card").for_object("billing_address").on("postal_code")
        country_errors = result.errors.for_object("android_pay_card").for_object("billing_address").on("country_code_alpha2")
        self.assertEqual(1, len(postal_errors))
        self.assertEqual(1, len(country_errors))
        self.assertEqual(ErrorCodes.Address.CountryCodeAlpha2IsNotAccepted, country_errors[0].code)
        self.assertEqual(ErrorCodes.Address.PostalCodeInvalidCharacters, postal_errors[0].code)

    def test_update_works_for_raw_android_pay_network_token(self):
        with FraudProtectionEnterpriseIntegrationMerchant():
            customer = Customer.create().customer
            secure_token = TestHelper.random_token_block(None)

            result = Customer.update(customer.id, {
                "android_pay_network_token": {
                    "number": "4111111111111111",
                    "expiration_month": "05",
                    "expiration_year": "2014",
                    "cryptogram": "01010101010101010101",
                    "eci_indicator": "05",
                    "google_transaction_id": "iliketurtles",
                    "token": secure_token,
                    "options": {
                        "make_default": True
                    },
                    "billing_address": {
                        "street_address": "123 Abc Way",
                        "locality": "Chicago",
                        "region": "Illinois",
                        "postal_code": "60622",
                        "phone_number": "312.555.1234",
                        "country_code_alpha2": "US",
                        "country_code_alpha3": "USA",
                        "country_code_numeric": "840",
                        "country_name": "United States of America"
                    }
                },
            })

            self.assertTrue(result.is_success)
            self.assertEqual(secure_token, result.customer.payment_methods[0].token)

            self.assertNotEqual(0, len(result.customer.android_pay_cards))
            android_pay_network_token = result.customer.android_pay_cards[0]
            self.assertTrue(android_pay_network_token.default)
            self.assertEqual(android_pay_network_token.expiration_month, "05")
            self.assertEqual(android_pay_network_token.expiration_year, "2014")
            self.assertEqual(android_pay_network_token.google_transaction_id, "iliketurtles")
            self.assertEqual(android_pay_network_token.bin, "411111")

            self.assertEqual(android_pay_network_token.billing_address["street_address"], "123 Abc Way")
            self.assertEqual(android_pay_network_token.billing_address["locality"], "Chicago")
            self.assertEqual(android_pay_network_token.billing_address["region"], "Illinois")
            self.assertEqual(android_pay_network_token.billing_address["postal_code"], "60622")
            self.assertEqual(android_pay_network_token.billing_address["phone_number"], "312.555.1234")
            self.assertEqual(android_pay_network_token.billing_address["country_code_alpha2"], "US")
            self.assertEqual(android_pay_network_token.billing_address["country_code_alpha3"], "USA")
            self.assertEqual(android_pay_network_token.billing_address["country_code_numeric"], "840")
            self.assertEqual(android_pay_network_token.billing_address["country_name"], "United States of America")

    def test_update_with_tax_identifiers(self):
        customer = Customer.create({
            "tax_identifiers": [
                {"country_code": "US", "identifier": "123456789"},
                {"country_code": "GB", "identifier": "987654321"}]
            }).customer

        result = Customer.update(customer.id, {
            "tax_identifiers": [{
                "country_code": "GB",
                "identifier": "567891234"
                }]
            })

        self.assertTrue(result.is_success)

    def test_customer_payment_methods(self):
        customer = Customer("gateway", {
            "credit_cards": [{"token": "credit_card"}],
            "paypal_accounts": [{"token": "paypal_account"}],
            "apple_pay_cards": [{"token": "apple_pay_card"}],
            "android_pay_cards": [{"token": "android_pay_card"}],
            "us_bank_accounts": [{"token": "us_bank_account"}]
            })

        payment_method_tokens = [ pm.token for pm in customer.payment_methods ]

        self.assertEqual(sorted(payment_method_tokens), ["android_pay_card", "apple_pay_card", "credit_card", "paypal_account", "us_bank_account"])
