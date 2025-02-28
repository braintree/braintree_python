from tests.test_helper import *

class TestMasterpass(unittest.TestCase):
    def test_create_from_nonce(self):
        customer = Customer.create().customer
        result = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.MasterpassVisa
        })

        self.assertTrue(result.is_success)

        masterpass_card = result.payment_method
        self.assertIsNotNone(masterpass_card.billing_address)
        self.assertIsNotNone(masterpass_card.bin)
        self.assertIsNotNone(masterpass_card.card_type)
        self.assertIsNotNone(masterpass_card.cardholder_name)
        self.assertIsNotNone(masterpass_card.commercial)
        self.assertIsNotNone(masterpass_card.country_of_issuance)
        self.assertIsNotNone(masterpass_card.created_at)
        self.assertIsNotNone(masterpass_card.customer_id)
        self.assertIsNotNone(masterpass_card.customer_location)
        self.assertIsNotNone(masterpass_card.debit)
        self.assertIsNotNone(masterpass_card.default)
        self.assertIsNotNone(masterpass_card.durbin_regulated)
        self.assertIsNotNone(masterpass_card.expiration_date)
        self.assertIsNotNone(masterpass_card.expiration_month)
        self.assertIsNotNone(masterpass_card.expiration_year)
        self.assertIsNotNone(masterpass_card.expired)
        self.assertIsNotNone(masterpass_card.healthcare)
        self.assertIsNotNone(masterpass_card.image_url)
        self.assertIsNotNone(masterpass_card.issuing_bank)
        self.assertIsNotNone(masterpass_card.last_4)
        self.assertIsNotNone(masterpass_card.masked_number)
        self.assertIsNotNone(masterpass_card.payroll)
        self.assertIsNotNone(masterpass_card.prepaid)
        self.assertIsNotNone(masterpass_card.prepaid_reloadable)
        self.assertIsNotNone(masterpass_card.product_id)
        self.assertIsNotNone(masterpass_card.subscriptions)
        self.assertIsNotNone(masterpass_card.token)
        self.assertIsNotNone(masterpass_card.unique_number_identifier)
        self.assertIsNotNone(masterpass_card.updated_at)

        customer = Customer.find(customer.id)
        self.assertEqual(len(customer.masterpass_cards), 1)
        self.assertEqual(result.payment_method.token, customer.masterpass_cards[0].token)

    def test_search_for_transaction(self):
        result = Transaction.sale({
            "payment_method_nonce": Nonces.MasterpassVisa,
            "amount": "1.23"
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == PaymentInstrumentType.MasterpassCard
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

    def test_create_transaction_from_nonce_and_vault(self):
        customer = Customer.create().customer
        result = Transaction.sale({
            "payment_method_nonce": Nonces.MasterpassVisa,
            "customer_id": customer.id,
            "amount": "1.23",
            "options": {
                "store_in_vault": "true"
            }
        })

        self.assertTrue(result.is_success)
        masterpass_card_details = result.transaction.masterpass_card_details

        self.assertIsNotNone(masterpass_card_details.bin)
        self.assertIsNotNone(masterpass_card_details.card_type)
        self.assertIsNotNone(masterpass_card_details.cardholder_name)
        self.assertIsNotNone(masterpass_card_details.commercial)
        self.assertIsNotNone(masterpass_card_details.country_of_issuance)
        self.assertIsNotNone(masterpass_card_details.debit)
        self.assertIsNotNone(masterpass_card_details.durbin_regulated)
        self.assertIsNotNone(masterpass_card_details.expiration_date)
        self.assertIsNotNone(masterpass_card_details.expiration_month)
        self.assertIsNotNone(masterpass_card_details.expiration_year)
        self.assertIsNotNone(masterpass_card_details.healthcare)
        self.assertIsNotNone(masterpass_card_details.image_url)
        self.assertIsNotNone(masterpass_card_details.issuing_bank)
        self.assertIsNotNone(masterpass_card_details.last_4)
        self.assertIsNotNone(masterpass_card_details.payroll)
        self.assertIsNotNone(masterpass_card_details.prepaid)
        self.assertIsNotNone(masterpass_card_details.prepaid_reloadable)
        self.assertIsNotNone(masterpass_card_details.product_id)
        self.assertIsNotNone(masterpass_card_details.token)
