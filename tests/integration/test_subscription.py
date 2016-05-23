from tests.test_helper import *
from braintree.test.nonces import Nonces

class TestSubscription(unittest.TestCase):
    def setUp(self):
        self.credit_card = Customer.create({
            "first_name": "Mike",
            "last_name": "Jones",
            "credit_card": {
                "number": "4111111111111111",
                "expiration_date": "05/2010",
                "cvv": "100"
            }
        }).customer.credit_cards[0]

        self.updateable_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "price": Decimal("54.32"),
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription


    def test_create_returns_successful_result_if_valid(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        })

        self.assertTrue(result.is_success)
        subscription = result.subscription
        self.assertNotEquals(None, re.search("\A\w{6}\Z", subscription.id))
        self.assertEquals(Decimal("12.34"), subscription.price)
        self.assertEquals(Decimal("12.34"), subscription.next_bill_amount)
        self.assertEquals(Decimal("12.34"), subscription.next_billing_period_amount)
        self.assertEquals(Subscription.Status.Active, subscription.status)
        self.assertEquals("integration_trialless_plan", subscription.plan_id)
        self.assertEquals(TestHelper.default_merchant_account_id, subscription.merchant_account_id)
        self.assertEquals(Decimal("0.00"), subscription.balance)

        self.assertEquals(date, type(subscription.first_billing_date))
        self.assertEquals(date, type(subscription.next_billing_date))
        self.assertEquals(date, type(subscription.billing_period_start_date))
        self.assertEquals(date, type(subscription.billing_period_end_date))
        self.assertEquals(date, type(subscription.paid_through_date))

        self.assertEquals(datetime, type(subscription.created_at))
        self.assertEquals(datetime, type(subscription.updated_at))
        
        self.assertEquals(1, subscription.current_billing_cycle)
        self.assertEquals(0, subscription.failure_count)
        self.assertEquals(self.credit_card.token, subscription.payment_method_token)

        self.assertEquals(Subscription.Status.Active, subscription.status_history[0].status)
        self.assertEquals(Decimal("12.34"), subscription.status_history[0].price)
        self.assertEquals(Decimal("0.00"), subscription.status_history[0].balance)
        self.assertEquals(Subscription.Source.Api, subscription.status_history[0].subscription_source)

    def test_create_returns_successful_result_with_payment_method_nonce(self):
        config = Configuration.instantiate()
        customer_id = Customer.create().customer.id
        parsed_client_token = TestHelper.generate_decoded_client_token({"customer_id": customer_id})
        authorization_fingerprint = json.loads(parsed_client_token)["authorizationFingerprint"]
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

        result = Subscription.create({
            "payment_method_nonce": nonce,
            "plan_id": TestHelper.trialless_plan["id"]
        })

        self.assertTrue(result.is_success)
        transaction = result.subscription.transactions[0]
        self.assertEqual("411111", transaction.credit_card_details.bin)


    def test_create_can_set_the_id(self):
        new_id = str(random.randint(1, 1000000))
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "id": new_id
        })

        self.assertTrue(result.is_success)
        self.assertEquals(new_id, result.subscription.id)

    def test_create_can_set_the_merchant_account_id(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "merchant_account_id": TestHelper.non_default_merchant_account_id
        })

        self.assertTrue(result.is_success)
        self.assertEquals(TestHelper.non_default_merchant_account_id, result.subscription.merchant_account_id)

    def test_create_defaults_to_plan_without_trial(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription

        self.assertEquals(TestHelper.trialless_plan["trial_period"], subscription.trial_period)
        self.assertEquals(None, subscription.trial_duration)
        self.assertEquals(None, subscription.trial_duration_unit)

    def test_create_defaults_to_plan_with_trial(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
        }).subscription

        self.assertEquals(TestHelper.trial_plan["trial_period"], subscription.trial_period)
        self.assertEquals(TestHelper.trial_plan["trial_duration"], subscription.trial_duration)
        self.assertEquals(TestHelper.trial_plan["trial_duration_unit"], subscription.trial_duration_unit)

    def test_create_and_override_plan_with_trial(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "trial_duration": 5,
            "trial_duration_unit": Subscription.TrialDurationUnit.Month
        }).subscription

        self.assertEquals(True, subscription.trial_period)
        self.assertEquals(5, subscription.trial_duration)
        self.assertEquals(Subscription.TrialDurationUnit.Month, subscription.trial_duration_unit)

    def test_create_and_override_trial_period(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "trial_period": False
        }).subscription

        self.assertEquals(False, subscription.trial_period)

    def test_create_and_override_number_of_billing_cycles(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "number_of_billing_cycles": 10
        }).subscription

        self.assertEquals(10, subscription.number_of_billing_cycles)

    def test_create_and_override_number_of_billing_cycles_to_never_expire(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "never_expires": True
        }).subscription

        self.assertEquals(None, subscription.number_of_billing_cycles)

    def test_create_creates_a_transaction_if_no_trial_period(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription

        self.assertEquals(1, len(subscription.transactions))
        transaction = subscription.transactions[0]
        self.assertEquals(Transaction, type(transaction))
        self.assertEquals(TestHelper.trialless_plan["price"], transaction.amount)
        self.assertEquals("sale", transaction.type)
        self.assertEquals(subscription.id, transaction.subscription_id)

    def test_create_has_transaction_with_billing_period_dates(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription
        transaction = subscription.transactions[0]
        self.assertEquals(subscription.billing_period_start_date, transaction.subscription_details.billing_period_start_date)
        self.assertEquals(subscription.billing_period_end_date, transaction.subscription_details.billing_period_end_date)

    def test_create_returns_a_transaction_if_transaction_is_declined(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "price": TransactionAmounts.Decline
        })

        self.assertFalse(result.is_success)
        self.assertEquals(Transaction.Status.ProcessorDeclined, result.transaction.status)

    def test_create_doesnt_creates_a_transaction_if_trial_period(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
        }).subscription

        self.assertEquals(0, len(subscription.transactions))

    def test_create_with_error_result(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "id": "invalid token"
        })

        self.assertFalse(result.is_success)
        self.assertEquals("81906", result.errors.for_object("subscription").on("id")[0].code)

    def test_create_inherits_billing_day_of_month_from_plan(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.billing_day_of_month_plan["id"],
        })

        self.assertTrue(result.is_success)
        self.assertEquals(5, result.subscription.billing_day_of_month)

    def test_create_allows_overriding_billing_day_of_month(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.billing_day_of_month_plan["id"],
            "billing_day_of_month": 19
        })

        self.assertTrue(result.is_success)
        self.assertEquals(19, result.subscription.billing_day_of_month)

    def test_create_allows_overriding_billing_day_of_month_with_start_immediately(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.billing_day_of_month_plan["id"],
            "options": {
                "start_immediately": True
            }
        })

        self.assertTrue(result.is_success)
        self.assertEquals(1, len(result.subscription.transactions))

    def test_create_allows_specifying_first_billing_date(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.billing_day_of_month_plan["id"],
            "first_billing_date": date.today() + timedelta(days=3)
        })

        self.assertTrue(result.is_success)
        self.assertEquals(date.today() + timedelta(days=3), result.subscription.first_billing_date)
        self.assertEquals(Subscription.Status.Pending, result.subscription.status)

    def test_create_does_not_allow_first_billing_date_in_the_past(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.billing_day_of_month_plan["id"],
            "first_billing_date": date.today() - timedelta(days=3)
        })

        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.Subscription.FirstBillingDateCannotBeInThePast,
            result.errors.for_object("subscription").on("first_billing_date")[0].code
        )

    def test_create_does_not_inherit_add_ons_or_discounts_from_the_plan_when_flag_is_set(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
            "options": {
                "do_not_inherit_add_ons_or_discounts": True
            }
        }).subscription

        self.assertEquals(0, len(subscription.add_ons))
        self.assertEquals(0, len(subscription.discounts))

    def test_create_inherits_add_ons_and_discounts_from_the_plan_when_not_specified(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"]
        }).subscription

        self.assertEquals(2, len(subscription.add_ons))
        add_ons = sorted(subscription.add_ons, key=lambda add_on: add_on.id)

        self.assertEquals("increase_10", add_ons[0].id)
        self.assertEquals(Decimal("10.00"), add_ons[0].amount)
        self.assertEquals(1, add_ons[0].quantity)
        self.assertEquals(None, add_ons[0].number_of_billing_cycles)
        self.assertTrue(add_ons[0].never_expires)
        self.assertEquals(0, add_ons[0].current_billing_cycle)

        self.assertEquals("increase_20", add_ons[1].id)
        self.assertEquals(Decimal("20.00"), add_ons[1].amount)
        self.assertEquals(1, add_ons[1].quantity)
        self.assertEquals(None, add_ons[1].number_of_billing_cycles)
        self.assertTrue(add_ons[1].never_expires)
        self.assertEquals(0, add_ons[1].current_billing_cycle)

        self.assertEquals(2, len(subscription.discounts))
        discounts = sorted(subscription.discounts, key=lambda discount: discount.id)

        self.assertEquals("discount_11", discounts[0].id)
        self.assertEquals(Decimal("11.00"), discounts[0].amount)
        self.assertEquals(1, discounts[0].quantity)
        self.assertEquals(None, discounts[0].number_of_billing_cycles)
        self.assertTrue(discounts[0].never_expires)
        self.assertEquals(0, discounts[0].current_billing_cycle)

        self.assertEquals("discount_7", discounts[1].id)
        self.assertEquals(Decimal("7.00"), discounts[1].amount)
        self.assertEquals(1, discounts[1].quantity)
        self.assertEquals(None, discounts[1].number_of_billing_cycles)
        self.assertTrue(discounts[1].never_expires)
        self.assertEquals(0, discounts[1].current_billing_cycle)

    def test_create_allows_overriding_of_inherited_add_ons_and_discounts(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
            "add_ons": {
                "update": [
                    {
                        "amount": Decimal("50.00"),
                        "existing_id": "increase_10",
                        "quantity": 2,
                        "number_of_billing_cycles": 5
                    },
                    {
                        "amount": Decimal("100.00"),
                        "existing_id": "increase_20",
                        "quantity": 4,
                        "never_expires": True
                    }
                ]
            },
            "discounts": {
                "update": [
                    {
                        "amount": Decimal("15.00"),
                        "existing_id": "discount_7",
                        "quantity": 3,
                        "number_of_billing_cycles": 19
                    }
                ]
            }
        }).subscription

        self.assertEquals(2, len(subscription.add_ons))
        add_ons = sorted(subscription.add_ons, key=lambda add_on: add_on.id)

        self.assertEquals("increase_10", add_ons[0].id)
        self.assertEquals(Decimal("50.00"), add_ons[0].amount)
        self.assertEquals(2, add_ons[0].quantity)
        self.assertEquals(5, add_ons[0].number_of_billing_cycles)
        self.assertFalse(add_ons[0].never_expires)
        self.assertEquals(0, add_ons[0].current_billing_cycle)

        self.assertEquals("increase_20", add_ons[1].id)
        self.assertEquals(Decimal("100.00"), add_ons[1].amount)
        self.assertEquals(4, add_ons[1].quantity)
        self.assertEquals(None, add_ons[1].number_of_billing_cycles)
        self.assertTrue(add_ons[1].never_expires)
        self.assertEquals(0, add_ons[1].current_billing_cycle)

        self.assertEquals(2, len(subscription.discounts))
        discounts = sorted(subscription.discounts, key=lambda discount: discount.id)

        self.assertEquals("discount_11", discounts[0].id)
        self.assertEquals(Decimal("11.00"), discounts[0].amount)
        self.assertEquals(1, discounts[0].quantity)
        self.assertEquals(None, discounts[0].number_of_billing_cycles)
        self.assertTrue(discounts[0].never_expires)
        self.assertEquals(0, discounts[0].current_billing_cycle)

        self.assertEquals("discount_7", discounts[1].id)
        self.assertEquals(Decimal("15.00"), discounts[1].amount)
        self.assertEquals(3, discounts[1].quantity)
        self.assertEquals(19, discounts[1].number_of_billing_cycles)
        self.assertFalse(discounts[1].never_expires)
        self.assertEquals(0, discounts[1].current_billing_cycle)

    def test_create_allows_deleting_of_inherited_add_ons_and_discounts(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
            "add_ons": {
                "remove": ["increase_10", "increase_20"]
            },
            "discounts": {
                "remove": ["discount_7"]
            }
        }).subscription

        self.assertEquals(0, len(subscription.add_ons))
        self.assertEquals(1, len(subscription.discounts))
        self.assertEquals("discount_11", subscription.discounts[0].id)

    def test_create_allows_adding_add_ons_and_discounts(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
            "add_ons": {
                "add": [
                    {
                        "amount": Decimal("50.00"),
                        "inherited_from_id": "increase_30",
                        "quantity": 2,
                        "number_of_billing_cycles": 5
                    }
                ],
                "remove": ["increase_10", "increase_20"]
            },
            "discounts": {
                "add": [
                    {
                        "amount": Decimal("17.00"),
                        "inherited_from_id": "discount_15",
                        "never_expires": True
                    }
                ],
                "remove": ["discount_7", "discount_11"]
            }
        }).subscription

        self.assertEquals(1, len(subscription.add_ons))

        self.assertEquals("increase_30", subscription.add_ons[0].id)
        self.assertEquals(Decimal("50.00"), subscription.add_ons[0].amount)
        self.assertEquals(2, subscription.add_ons[0].quantity)
        self.assertEquals(5, subscription.add_ons[0].number_of_billing_cycles)
        self.assertFalse(subscription.add_ons[0].never_expires)
        self.assertEquals(0, subscription.add_ons[0].current_billing_cycle)

        self.assertEquals(1, len(subscription.discounts))

        self.assertEquals("discount_15", subscription.discounts[0].id)
        self.assertEquals(Decimal("17.00"), subscription.discounts[0].amount)
        self.assertEquals(1, subscription.discounts[0].quantity)
        self.assertEquals(None, subscription.discounts[0].number_of_billing_cycles)
        self.assertTrue(subscription.discounts[0].never_expires)
        self.assertEquals(0, subscription.discounts[0].current_billing_cycle)

    def test_create_properly_parses_validation_errors_for_arrays(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
            "add_ons": {
                "update": [
                    {
                        "existing_id": "increase_10",
                        "amount": "invalid"
                    },
                    {
                        "existing_id": "increase_20",
                        "quantity": -2
                    }
                ]
            }
        })

        self.assertFalse(result.is_success)

        self.assertEquals(
            ErrorCodes.Subscription.Modification.AmountIsInvalid,
            result.errors.for_object("subscription").for_object("add_ons").for_object("update").for_index(0).on("amount")[0].code
        )
        self.assertEquals(
            ErrorCodes.Subscription.Modification.QuantityIsInvalid,
            result.errors.for_object("subscription").for_object("add_ons").for_object("update").for_index(1).on("quantity")[0].code
        )

    def test_descriptors_accepts_name_phone_and_url(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "descriptor": {
                "name": "123*123456789012345678",
                "phone": "3334445555",
                "url": "ebay.com"
            }
        })

        self.assertTrue(result.is_success)
        subscription = result.subscription
        self.assertEquals("123*123456789012345678", subscription.descriptor.name)
        self.assertEquals("3334445555", subscription.descriptor.phone)

        transaction = subscription.transactions[0]
        self.assertEquals("123*123456789012345678", transaction.descriptor.name)
        self.assertEquals("3334445555", transaction.descriptor.phone)
        self.assertEquals("ebay.com", transaction.descriptor.url)

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

    def test_find_with_valid_id(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
        }).subscription

        found_subscription = Subscription.find(subscription.id)
        self.assertEquals(subscription.id, found_subscription.id)

    @raises_with_regexp(NotFoundError, "subscription with id bad_token not found")
    def test_find_with_invalid_token(self):
        Subscription.find("bad_token")

    def test_update_creates_a_prorated_transaction_when_merchant_is_set_to_prorate(self):
        new_id = str(random.randint(1, 1000000))
        result = Subscription.update(self.updateable_subscription.id, {
            "price": self.updateable_subscription.price + Decimal("1"),
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(2, len(subscription.transactions))

    def test_update_creates_a_prorated_transaction_when_flag_is_passed_as_True(self):
        new_id = str(random.randint(1, 1000000))
        result = Subscription.update(self.updateable_subscription.id, {
            "price": self.updateable_subscription.price + Decimal("1"),
            "options": {
                "prorate_charges": True
            }
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(2, len(subscription.transactions))

    def test_update_does_not_create_a_prorated_transaction_when_flag_is_passed_as_False(self):
        new_id = str(random.randint(1, 1000000))
        result = Subscription.update(self.updateable_subscription.id, {
            "price": self.updateable_subscription.price + Decimal("1"),
            "options": {
                "prorate_charges": False
            }
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(1, len(subscription.transactions))

    def test_update_does_not_update_subscription_when_revert_subscription_on_proration_failure_is_true(self):
        new_id = str(random.randint(1, 1000000))
        result = Subscription.update(self.updateable_subscription.id, {
            "price": self.updateable_subscription.price + Decimal("2100"),
            "options": {
                "prorate_charges": True,
                "revert_subscription_on_proration_failure": True
            }
        })

        self.assertFalse(result.is_success)

        found_subscription = Subscription.find(result.subscription.id)
        self.assertEquals(len(self.updateable_subscription.transactions) + 1, len(result.subscription.transactions))
        self.assertEqual("processor_declined", result.subscription.transactions[0].status)

        self.assertEqual(Decimal("0.00"), found_subscription.balance)
        self.assertEquals(self.updateable_subscription.price, found_subscription.price)

    def test_update_updates_subscription_when_revert_subscription_on_proration_failure_is_false(self):
        new_id = str(random.randint(1, 1000000))
        result = Subscription.update(self.updateable_subscription.id, {
            "price": self.updateable_subscription.price + Decimal("2100"),
            "options": {
                "prorate_charges": True,
                "revert_subscription_on_proration_failure": False
            }
        })

        self.assertTrue(result.is_success)

        found_subscription = Subscription.find(result.subscription.id)
        self.assertEquals(len(self.updateable_subscription.transactions) + 1, len(result.subscription.transactions))
        self.assertEqual("processor_declined", result.subscription.transactions[0].status)

        self.assertEqual(result.subscription.transactions[0].amount, Decimal(found_subscription.balance))
        self.assertEquals(self.updateable_subscription.price + Decimal("2100"), found_subscription.price)

    def test_update_with_successful_result(self):
        new_id = str(random.randint(1, 1000000))
        result = Subscription.update(self.updateable_subscription.id, {
            "id": new_id,
            "price": Decimal("9999.88"),
            "plan_id": TestHelper.trial_plan["id"]
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(new_id, subscription.id)
        self.assertEquals(TestHelper.trial_plan["id"], subscription.plan_id)
        self.assertEquals(Decimal("9999.88"), subscription.price)

    def test_update_with_merchant_account_id(self):
        result = Subscription.update(self.updateable_subscription.id, {
            "merchant_account_id": TestHelper.non_default_merchant_account_id,
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(TestHelper.non_default_merchant_account_id, subscription.merchant_account_id)

    def test_update_with_payment_method_token(self):
        newCard = CreditCard.create({
            "customer_id": self.credit_card.customer_id,
            "number": "4111111111111111",
            "expiration_date": "05/2009",
            "cvv": "100",
            "cardholder_name": self.credit_card.cardholder_name
        }).credit_card

        result = Subscription.update(self.updateable_subscription.id, {
            "payment_method_token": newCard.token
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(newCard.token, subscription.payment_method_token)

    def test_update_with_payment_method_nonce(self):
        config = Configuration.instantiate()
        customer_id = self.credit_card.customer_id
        parsed_client_token = TestHelper.generate_decoded_client_token({"customer_id": customer_id})
        authorization_fingerprint = json.loads(parsed_client_token)["authorizationFingerprint"]
        http = ClientApiHttp(config, {
            "authorization_fingerprint": authorization_fingerprint,
            "shared_customer_identifier": "fake_identifier",
            "shared_customer_identifier_type": "testing"
        })
        status_code, response = http.add_card({
            "credit_card": {
                "number": "4242424242424242",
                "expiration_month": "11",
                "expiration_year": "2099",
            },
            "share": True
        })
        nonce = json.loads(response)["creditCards"][0]["nonce"]

        result = Subscription.update(self.updateable_subscription.id, {
            "payment_method_nonce": nonce
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        newCard = CreditCard.find(subscription.payment_method_token)
        self.assertEquals("4242", newCard.last_4)
        self.assertNotEquals(newCard.last_4, self.credit_card.last_4)

    def test_update_with_number_of_billing_cycles(self):
        result = Subscription.update(self.updateable_subscription.id, {
            "number_of_billing_cycles": 10
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(10, subscription.number_of_billing_cycles)

    def test_update_with_never_expires(self):
        result = Subscription.update(self.updateable_subscription.id, {
            "never_expires": True
        })

        self.assertTrue(result.is_success)

        subscription = result.subscription
        self.assertEquals(None, subscription.number_of_billing_cycles)

    def test_update_with_error_result(self):
        result = Subscription.update(self.updateable_subscription.id, {
            "id": "bad id",
        })

        self.assertFalse(result.is_success)
        self.assertEquals("81906", result.errors.for_object("subscription").on("id")[0].code)

    @raises(NotFoundError)
    def test_update_raises_error_when_subscription_not_found(self):
        Subscription.update("notfound", {
            "id": "newid",
        })

    def test_update_allows_overriding_of_inherited_add_ons_and_discounts(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
        }).subscription

        subscription = Subscription.update(subscription.id, {
            "add_ons": {
                "update": [
                    {
                        "amount": Decimal("50.00"),
                        "existing_id": "increase_10",
                        "quantity": 2,
                        "number_of_billing_cycles": 5
                    },
                    {
                        "amount": Decimal("100.00"),
                        "existing_id": "increase_20",
                        "quantity": 4,
                        "never_expires": True
                    }
                ]
            },
            "discounts": {
                "update": [
                    {
                        "amount": Decimal("15.00"),
                        "existing_id": "discount_7",
                        "quantity": 3,
                        "number_of_billing_cycles": 19
                    }
                ]
            }
        }).subscription

        self.assertEquals(2, len(subscription.add_ons))
        add_ons = sorted(subscription.add_ons, key=lambda add_on: add_on.id)

        self.assertEquals("increase_10", add_ons[0].id)
        self.assertEquals(Decimal("50.00"), add_ons[0].amount)
        self.assertEquals(2, add_ons[0].quantity)
        self.assertEquals(5, add_ons[0].number_of_billing_cycles)
        self.assertFalse(add_ons[0].never_expires)

        self.assertEquals("increase_20", add_ons[1].id)
        self.assertEquals(Decimal("100.00"), add_ons[1].amount)
        self.assertEquals(4, add_ons[1].quantity)
        self.assertEquals(None, add_ons[1].number_of_billing_cycles)
        self.assertTrue(add_ons[1].never_expires)

        self.assertEquals(2, len(subscription.discounts))
        discounts = sorted(subscription.discounts, key=lambda discount: discount.id)

        self.assertEquals("discount_11", discounts[0].id)
        self.assertEquals(Decimal("11.00"), discounts[0].amount)
        self.assertEquals(1, discounts[0].quantity)
        self.assertEquals(None, discounts[0].number_of_billing_cycles)
        self.assertTrue(discounts[0].never_expires)

        self.assertEquals("discount_7", discounts[1].id)
        self.assertEquals(Decimal("15.00"), discounts[1].amount)
        self.assertEquals(3, discounts[1].quantity)
        self.assertEquals(19, discounts[1].number_of_billing_cycles)
        self.assertFalse(discounts[1].never_expires)

    def test_update_allows_adding_and_removing_add_ons_and_discounts(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
        }).subscription

        subscription = Subscription.update(subscription.id, {
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
            "add_ons": {
                "add": [
                    {
                        "amount": Decimal("50.00"),
                        "inherited_from_id": "increase_30",
                        "quantity": 2,
                        "number_of_billing_cycles": 5
                    }
                ],
                "remove": ["increase_10", "increase_20"]
            },
            "discounts": {
                "add": [
                    {
                        "amount": Decimal("17.00"),
                        "inherited_from_id": "discount_15",
                        "never_expires": True
                    }
                ],
                "remove": ["discount_7", "discount_11"]
            }
        }).subscription

        self.assertEquals(1, len(subscription.add_ons))

        self.assertEquals("increase_30", subscription.add_ons[0].id)
        self.assertEquals(Decimal("50.00"), subscription.add_ons[0].amount)
        self.assertEquals(2, subscription.add_ons[0].quantity)
        self.assertEquals(5, subscription.add_ons[0].number_of_billing_cycles)
        self.assertFalse(subscription.add_ons[0].never_expires)

        self.assertEquals(1, len(subscription.discounts))

        self.assertEquals("discount_15", subscription.discounts[0].id)
        self.assertEquals(Decimal("17.00"), subscription.discounts[0].amount)
        self.assertEquals(1, subscription.discounts[0].quantity)
        self.assertEquals(None, subscription.discounts[0].number_of_billing_cycles)
        self.assertTrue(subscription.discounts[0].never_expires)

    def test_update_can_replace_entire_set_of_add_ons_and_discounts(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
        }).subscription

        subscription = Subscription.update(subscription.id, {
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.add_on_discount_plan["id"],
            "add_ons": {
                "add": [
                    { "inherited_from_id": "increase_30", },
                    { "inherited_from_id": "increase_20", }
                ]
            },
            "discounts": {
                "add": [
                    { "inherited_from_id": "discount_15", }
                ]
            },
            "options": {
                "replace_all_add_ons_and_discounts": True
            }
        }).subscription

        self.assertEquals(2, len(subscription.add_ons))
        add_ons = sorted(subscription.add_ons, key=lambda add_on: add_on.id)

        self.assertEquals("increase_20", add_ons[0].id)
        self.assertEquals(Decimal("20.00"), add_ons[0].amount)
        self.assertEquals(1, add_ons[0].quantity)
        self.assertEquals(None, add_ons[0].number_of_billing_cycles)
        self.assertTrue(add_ons[0].never_expires)

        self.assertEquals("increase_30", add_ons[1].id)
        self.assertEquals(Decimal("30.00"), add_ons[1].amount)
        self.assertEquals(1, add_ons[1].quantity)
        self.assertEquals(None, add_ons[1].number_of_billing_cycles)
        self.assertTrue(add_ons[1].never_expires)

        self.assertEquals(1, len(subscription.discounts))

        self.assertEquals("discount_15", subscription.discounts[0].id)
        self.assertEquals(Decimal("15.00"), subscription.discounts[0].amount)
        self.assertEquals(1, subscription.discounts[0].quantity)
        self.assertEquals(None, subscription.discounts[0].number_of_billing_cycles)
        self.assertTrue(subscription.discounts[0].never_expires)

    def test_update_descriptor_name_and_phone(self):
        result = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "descriptor": {
                "name": "123*123456789012345678",
                "phone": "1234567890"
            }
        })

        self.assertTrue(result.is_success)
        subscription = result.subscription
        updated_subscription = Subscription.update(subscription.id, {
            "descriptor": {
                "name": "999*99",
                "phone": "1234567890"
            }
        }).subscription

        self.assertEquals("999*99", updated_subscription.descriptor.name)
        self.assertEquals("1234567890", updated_subscription.descriptor.phone)

    def test_cancel_with_successful_response(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        result = Subscription.cancel(subscription.id)
        self.assertTrue(result.is_success)
        self.assertEqual("Canceled", result.subscription.status)

    def test_unsuccessful_cancel_returns_validation_error(self):
        Subscription.cancel(self.updateable_subscription.id)
        result = Subscription.cancel(self.updateable_subscription.id)

        self.assertFalse(result.is_success)
        self.assertEquals("81905", result.errors.for_object("subscription").on("status")[0].code)

    @raises(NotFoundError)
    def test_cancel_raises_not_found_error_with_bad_subscription(self):
        Subscription.cancel("notreal")

    def test_search_with_argument_list_rather_than_literal_list(self):
        trial_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "price": Decimal("1")
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "price": Decimal("1")
        }).subscription

        collection = Subscription.search(
            SubscriptionSearch.plan_id == "integration_trial_plan",
            SubscriptionSearch.price == Decimal("1")
        )

        self.assertTrue(TestHelper.includes(collection, trial_subscription))
        self.assertFalse(TestHelper.includes(collection, trialless_subscription))

    def test_search_on_billing_cycles_remaining(self):
        subscription_5 = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "number_of_billing_cycles": 5
        }).subscription

        subscription_10 = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "number_of_billing_cycles": 10
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.billing_cycles_remaining >= 7
        ])

        self.assertTrue(TestHelper.includes(collection, subscription_10))
        self.assertFalse(TestHelper.includes(collection, subscription_5))

    def test_search_on_days_past_due(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription
        TestHelper.make_past_due(subscription, 3)

        collection = Subscription.search([
            SubscriptionSearch.days_past_due.between(2, 10)
        ])

        self.assertTrue(collection.maximum_size > 0)
        for subscription in collection.items:
            self.assertTrue(2 <= subscription.days_past_due <= 10)

    def test_search_on_plan_id(self):
        trial_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "price": Decimal("2")
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "price": Decimal("2")
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.plan_id == "integration_trial_plan",
            SubscriptionSearch.price == Decimal("2")
        ])

        self.assertTrue(TestHelper.includes(collection, trial_subscription))
        self.assertFalse(TestHelper.includes(collection, trialless_subscription))

        collection = Subscription.search([
            SubscriptionSearch.plan_id.in_list("integration_trial_plan", "integration_trialless_plan"),
            SubscriptionSearch.price == Decimal("2")
        ])

        self.assertTrue(TestHelper.includes(collection, trial_subscription))
        self.assertTrue(TestHelper.includes(collection, trialless_subscription))

    def test_search_on_plan_id_is_acts_like_text_node_instead_of_multiple_value(self):
        trial_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "price": Decimal("3")
        }).subscription

        trialless_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "price": Decimal("3")
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.plan_id == "no such plan id",
            SubscriptionSearch.price == Decimal("3")
        ])

        self.assertEquals(0, collection.maximum_size)

    def test_search_on_status(self):
        active_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "price": Decimal("3")
        }).subscription

        canceled_subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
            "price": Decimal("3")
        }).subscription
        Subscription.cancel(canceled_subscription.id)

        collection = Subscription.search([
            SubscriptionSearch.status.in_list([Subscription.Status.Active, Subscription.Status.Canceled]),
            SubscriptionSearch.price == Decimal("3")
        ])

        self.assertTrue(TestHelper.includes(collection, active_subscription))
        self.assertTrue(TestHelper.includes(collection, canceled_subscription))

    def test_search_on_merchant_account_id(self):
        subscription_default_ma = Subscription.create({
            "merchant_account_id": TestHelper.default_merchant_account_id,
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "price": Decimal("4")
        }).subscription

        subscription_non_default_ma = Subscription.create({
            "merchant_account_id": TestHelper.non_default_merchant_account_id,
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "price": Decimal("4")
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.merchant_account_id == TestHelper.default_merchant_account_id,
            SubscriptionSearch.price == Decimal("4")
        ])

        self.assertTrue(TestHelper.includes(collection, subscription_default_ma))
        self.assertFalse(TestHelper.includes(collection, subscription_non_default_ma))

    def test_search_on_bogus_merchant_account_id(self):
        subscription = Subscription.create({
            "merchant_account_id": TestHelper.default_merchant_account_id,
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "price": Decimal("4")
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.merchant_account_id == subscription.merchant_account_id,
            SubscriptionSearch.price == Decimal("4")
        ])

        self.assertTrue(TestHelper.includes(collection, subscription))

        collection = Subscription.search([
            SubscriptionSearch.merchant_account_id.in_list(["totally_bogus_id", subscription.merchant_account_id]),
            SubscriptionSearch.price == Decimal("4")
        ])

        self.assertTrue(TestHelper.includes(collection, subscription))

        collection = Subscription.search([
            SubscriptionSearch.merchant_account_id == "totally_bogus_id",
            SubscriptionSearch.price == Decimal("4")
        ])

        self.assertFalse(TestHelper.includes(collection, subscription))

    def test_search_on_price(self):
        subscription_900 = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "price": Decimal("900")
        }).subscription

        subscription_1000 = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
            "price": Decimal("1000")
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.price >= Decimal("950")
        ])

        self.assertTrue(TestHelper.includes(collection, subscription_1000))
        self.assertFalse(TestHelper.includes(collection, subscription_900))

    def test_search_on_transaction_id(self):
        subscription_found = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription

        subscription_not_found = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription

        collection = Subscription.search(
            SubscriptionSearch.transaction_id == subscription_found.transactions[0].id
        )

        self.assertTrue(TestHelper.includes(collection, subscription_found))
        self.assertFalse(TestHelper.includes(collection, subscription_not_found))

    def test_search_on_id(self):
        subscription_found = Subscription.create({
            "id": "find_me_%s" % random.randint(1,1000000),
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
        }).subscription

        subscription_not_found = Subscription.create({
            "id": "do_not_find_me_%s" % random.randint(1,1000000),
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"],
        }).subscription

        collection = Subscription.search([
            SubscriptionSearch.id.starts_with("find_me")
        ])

        self.assertTrue(TestHelper.includes(collection, subscription_found))
        self.assertFalse(TestHelper.includes(collection, subscription_not_found))

    def test_search_on_next_billing_date(self):
        subscription_found = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"]
        }).subscription

        subscription_not_found = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trial_plan["id"]
        }).subscription

        next_billing_date_cutoff = datetime.today() + timedelta(days=5)

        collection = Subscription.search(
            SubscriptionSearch.next_billing_date >= next_billing_date_cutoff
        )

        self.assertTrue(TestHelper.includes(collection, subscription_found))
        self.assertFalse(TestHelper.includes(collection, subscription_not_found))

    def test_retryCharge_without_amount__deprecated(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription
        TestHelper.make_past_due(subscription)

        result = Subscription.retryCharge(subscription.id);

        self.assertTrue(result.is_success);
        transaction = result.transaction;

        self.assertEquals(subscription.price, transaction.amount);
        self.assertNotEqual(None, transaction.processor_authorization_code);
        self.assertEquals(Transaction.Type.Sale, transaction.type);
        self.assertEquals(Transaction.Status.Authorized, transaction.status);

    def test_retry_charge_without_amount(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription
        TestHelper.make_past_due(subscription)

        result = Subscription.retry_charge(subscription.id);

        self.assertTrue(result.is_success);
        transaction = result.transaction;

        self.assertEquals(subscription.price, transaction.amount);
        self.assertNotEqual(None, transaction.processor_authorization_code);
        self.assertEquals(Transaction.Type.Sale, transaction.type);
        self.assertEquals(Transaction.Status.Authorized, transaction.status);

    def test_retryCharge_with_amount__deprecated(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription
        TestHelper.make_past_due(subscription)

        result = Subscription.retryCharge(subscription.id, Decimal(TransactionAmounts.Authorize));

        self.assertTrue(result.is_success);
        transaction = result.transaction;

        self.assertEquals(Decimal(TransactionAmounts.Authorize), transaction.amount);
        self.assertNotEqual(None, transaction.processor_authorization_code);
        self.assertEquals(Transaction.Type.Sale, transaction.type);
        self.assertEquals(Transaction.Status.Authorized, transaction.status);


    def test_retry_charge_with_amount(self):
        subscription = Subscription.create({
            "payment_method_token": self.credit_card.token,
            "plan_id": TestHelper.trialless_plan["id"],
        }).subscription
        TestHelper.make_past_due(subscription)

        result = Subscription.retry_charge(subscription.id, Decimal(TransactionAmounts.Authorize));

        self.assertTrue(result.is_success);
        transaction = result.transaction;

        self.assertEquals(Decimal(TransactionAmounts.Authorize), transaction.amount);
        self.assertNotEqual(None, transaction.processor_authorization_code);
        self.assertEquals(Transaction.Type.Sale, transaction.type);
        self.assertEquals(Transaction.Status.Authorized, transaction.status);

    def test_create_with_paypal_future_payment_method_token(self):
        http = ClientApiHttp.create()
        status_code, nonce = http.get_paypal_nonce({
            "consent-code": "consent-code",
            "options": {"validate": False}
        })
        self.assertEquals(status_code, 202)

        payment_method_token = PaymentMethod.create({
            "customer_id": Customer.create().customer.id,
            "payment_method_nonce": nonce
        }).payment_method.token

        result = Subscription.create({
            "payment_method_token": payment_method_token,
            "plan_id": TestHelper.trialless_plan["id"]
        })

        self.assertTrue(result.is_success)
        subscription = result.subscription
        self.assertEquals(payment_method_token, subscription.payment_method_token)

    def test_create_fails_with_paypal_one_time_payment_method_nonce(self):
        result = Subscription.create({
            "payment_method_nonce": Nonces.PayPalOneTimePayment,
            "plan_id": TestHelper.trialless_plan["id"]
        })

        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.Subscription.PaymentMethodNonceIsInvalid,
            result.errors.for_object("subscription")[0].code
        )

    def test_create_fails_with_paypal_future_payment_method_nonce(self):
        result = Subscription.create({
            "payment_method_nonce": Nonces.PayPalFuturePayment,
            "plan_id": TestHelper.trialless_plan["id"]
        })

        self.assertFalse(result.is_success)
        self.assertEquals(
            ErrorCodes.Subscription.PaymentMethodNonceIsInvalid,
            result.errors.for_object("subscription")[0].code
        )
