from tests.test_helper import *

class TestVisaCheckout(unittest.TestCase):
    def test_create_from_nonce(self):
        customer = Customer.create().customer
        result = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.VisaCheckoutVisa
        })

        self.assertTrue(result.is_success)

        visa_checkout_card = result.payment_method
        self.assertEqual("abc123", visa_checkout_card.call_id)
        self.assertIsNotNone(visa_checkout_card.billing_address)
        self.assertIsNotNone(visa_checkout_card.bin)
        self.assertIsNotNone(visa_checkout_card.card_type)
        self.assertIsNotNone(visa_checkout_card.cardholder_name)
        self.assertIsNotNone(visa_checkout_card.commercial)
        self.assertIsNotNone(visa_checkout_card.country_of_issuance)
        self.assertIsNotNone(visa_checkout_card.created_at)
        self.assertIsNotNone(visa_checkout_card.customer_id)
        self.assertIsNotNone(visa_checkout_card.customer_location)
        self.assertIsNotNone(visa_checkout_card.debit)
        self.assertIsNotNone(visa_checkout_card.default)
        self.assertIsNotNone(visa_checkout_card.durbin_regulated)
        self.assertIsNotNone(visa_checkout_card.expiration_date)
        self.assertIsNotNone(visa_checkout_card.expiration_month)
        self.assertIsNotNone(visa_checkout_card.expiration_year)
        self.assertIsNotNone(visa_checkout_card.expired)
        self.assertIsNotNone(visa_checkout_card.healthcare)
        self.assertIsNotNone(visa_checkout_card.image_url)
        self.assertIsNotNone(visa_checkout_card.issuing_bank)
        self.assertIsNotNone(visa_checkout_card.last_4)
        self.assertIsNotNone(visa_checkout_card.masked_number)
        self.assertIsNotNone(visa_checkout_card.payroll)
        self.assertIsNotNone(visa_checkout_card.prepaid)
        self.assertIsNotNone(visa_checkout_card.prepaid_reloadable)
        self.assertIsNotNone(visa_checkout_card.product_id)
        self.assertIsNotNone(visa_checkout_card.subscriptions)
        self.assertIsNotNone(visa_checkout_card.token)
        self.assertIsNotNone(visa_checkout_card.unique_number_identifier)
        self.assertIsNotNone(visa_checkout_card.updated_at)

        customer = Customer.find(customer.id)
        self.assertEqual(len(customer.visa_checkout_cards), 1)
        self.assertEqual(result.payment_method.token, customer.visa_checkout_cards[0].token)

    def test_create_with_verification(self):
        customer = Customer.create().customer
        result = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.VisaCheckoutVisa,
            "options": {
                "verify_card": "true"
            }
        })

        self.assertTrue(result.is_success)
        verification = result.payment_method.verification
        self.assertEqual(CreditCardVerification.Status.Verified, verification.status)


    def test_search_for_transaction(self):
        result = Transaction.sale({
            "payment_method_nonce": Nonces.VisaCheckoutVisa,
            "amount": "1.23"
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == PaymentInstrumentType.VisaCheckoutCard
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

    def test_create_transaction_from_nonce_and_vault(self):
        customer = Customer.create().customer
        result = Transaction.sale({
            "payment_method_nonce": Nonces.VisaCheckoutVisa,
            "customer_id": customer.id,
            "amount": "1.23",
            "options": {
                "store_in_vault": "true"
            }
        })

        self.assertTrue(result.is_success)
        visa_checkout_card_details = result.transaction.visa_checkout_card_details

        self.assertEqual("abc123", visa_checkout_card_details.call_id)
        self.assertIsNotNone(visa_checkout_card_details.bin)
        self.assertIsNotNone(visa_checkout_card_details.card_type)
        self.assertIsNotNone(visa_checkout_card_details.cardholder_name)
        self.assertIsNotNone(visa_checkout_card_details.commercial)
        self.assertIsNotNone(visa_checkout_card_details.country_of_issuance)
        self.assertIsNotNone(visa_checkout_card_details.debit)
        self.assertIsNotNone(visa_checkout_card_details.durbin_regulated)
        self.assertIsNotNone(visa_checkout_card_details.expiration_date)
        self.assertIsNotNone(visa_checkout_card_details.expiration_month)
        self.assertIsNotNone(visa_checkout_card_details.expiration_year)
        self.assertIsNotNone(visa_checkout_card_details.healthcare)
        self.assertIsNotNone(visa_checkout_card_details.image_url)
        self.assertIsNotNone(visa_checkout_card_details.issuing_bank)
        self.assertIsNotNone(visa_checkout_card_details.last_4)
        self.assertIsNotNone(visa_checkout_card_details.payroll)
        self.assertIsNotNone(visa_checkout_card_details.prepaid)
        self.assertIsNotNone(visa_checkout_card_details.prepaid_reloadable)
        self.assertIsNotNone(visa_checkout_card_details.product_id)
        self.assertIsNotNone(visa_checkout_card_details.token)
