from tests.test_helper import *

# NEXT_MAJOR_VERSION remove this class
# SamsungPay is deprecated
@unittest.skip("deperacated - remove in next MAJOR release")
class TestSamsungPay(unittest.TestCase):
    def test_create_from_nonce(self):
        customer = Customer.create().customer
        result = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.SamsungPayVisa
        })

        self.assertTrue(result.is_success)
        samsung_pay_card = result.payment_method
        self.assertIsInstance(samsung_pay_card, braintree.SamsungPayCard)
        self.assertIsNotNone(samsung_pay_card.bin)
        self.assertIsNotNone(samsung_pay_card.card_type)
        self.assertIsNotNone(samsung_pay_card.commercial)
        self.assertIsNotNone(samsung_pay_card.country_of_issuance)
        self.assertIsNotNone(samsung_pay_card.created_at)
        self.assertIsNotNone(samsung_pay_card.customer_id)
        self.assertIsNotNone(samsung_pay_card.customer_location)
        self.assertIsNotNone(samsung_pay_card.debit)
        self.assertIsNotNone(samsung_pay_card.default)
        self.assertIsNotNone(samsung_pay_card.durbin_regulated)
        self.assertIsNotNone(samsung_pay_card.expiration_date)
        self.assertIsNotNone(samsung_pay_card.expiration_month)
        self.assertIsNotNone(samsung_pay_card.expiration_year)
        self.assertIsNotNone(samsung_pay_card.expired)
        self.assertIsNotNone(samsung_pay_card.healthcare)
        self.assertIsNotNone(samsung_pay_card.image_url)
        self.assertIsNotNone(samsung_pay_card.issuing_bank)
        self.assertIsNotNone(samsung_pay_card.last_4)
        self.assertIsNotNone(samsung_pay_card.masked_number)
        self.assertIsNotNone(samsung_pay_card.payroll)
        self.assertIsNotNone(samsung_pay_card.prepaid)
        self.assertIsNotNone(samsung_pay_card.product_id)
        self.assertIsNotNone(samsung_pay_card.subscriptions)
        self.assertIsNotNone(samsung_pay_card.token)
        self.assertIsNotNone(samsung_pay_card.unique_number_identifier)
        self.assertIsNotNone(samsung_pay_card.updated_at)

    def test_create_from_nonce_customer_attr(self):
        customer = Customer.create().customer
        result = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.SamsungPayVisa
        })

        samsung_pay_cards = Customer.find(customer.id).samsung_pay_cards
        self.assertEqual(len(samsung_pay_cards), 1)
        self.assertEqual(result.payment_method.token, samsung_pay_cards[0].token)

    def test_create_from_nonce_with_name_and_address(self):
        customer = Customer.create().customer
        result = PaymentMethod.create({
            "customer_id": customer.id,
            "payment_method_nonce": Nonces.SamsungPayVisa,
            "cardholder_name": "Gronk",
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
        self.assertEqual("Gronk", result.payment_method.cardholder_name)

        address = result.payment_method.billing_address
        self.assertEqual("123 Abc Way", address.street_address)
        self.assertEqual("Chicago", address.locality)
        self.assertEqual("Illinois", address.region)
        self.assertEqual("60622", address.postal_code)
        self.assertEqual("MX", address.country_code_alpha2)
        self.assertEqual("MEX", address.country_code_alpha3)
        self.assertEqual("484", address.country_code_numeric)
        self.assertEqual("Mexico", address.country_name)

    def test_search_for_transaction(self):
        result = Transaction.sale({
            "payment_method_nonce": Nonces.SamsungPayVisa,
            "amount": "1.69"
        })

        self.assertTrue(result.is_success)
        transaction = result.transaction

        collection = Transaction.search([
            TransactionSearch.id == transaction.id,
            TransactionSearch.payment_instrument_type == PaymentInstrumentType.SamsungPayCard
        ])

        self.assertEqual(1, collection.maximum_size)
        self.assertEqual(transaction.id, collection.first.id)

    def test_create_transaction_from_nonce_and_vault(self):
        customer = Customer.create().customer
        result = Transaction.sale({
            "payment_method_nonce": Nonces.SamsungPayVisa,
            "customer_id": customer.id,
            "amount": "69.69",
            "options": {
                "store_in_vault": True
            }
        })

        self.assertTrue(result.is_success)

        samsung_pay_card_details = result.transaction.samsung_pay_card_details
        self.assertIsInstance(samsung_pay_card_details, braintree.SamsungPayCard)
        self.assertIsNotNone(samsung_pay_card_details.bin)
        self.assertIsNotNone(samsung_pay_card_details.card_type)
        self.assertIsNotNone(samsung_pay_card_details.commercial)
        self.assertIsNotNone(samsung_pay_card_details.country_of_issuance)
        self.assertIsNotNone(samsung_pay_card_details.debit)
        self.assertIsNotNone(samsung_pay_card_details.durbin_regulated)
        self.assertIsNotNone(samsung_pay_card_details.expiration_date)
        self.assertIsNotNone(samsung_pay_card_details.expiration_year)
        self.assertIsNotNone(samsung_pay_card_details.expiration_month)
        self.assertIsNotNone(samsung_pay_card_details.healthcare)
        self.assertIsNotNone(samsung_pay_card_details.image_url)
        self.assertIsNotNone(samsung_pay_card_details.issuing_bank)
        self.assertIsNotNone(samsung_pay_card_details.last_4)
        self.assertIsNotNone(samsung_pay_card_details.payroll)
        self.assertIsNotNone(samsung_pay_card_details.prepaid)
        self.assertIsNotNone(samsung_pay_card_details.product_id)
        self.assertIsNotNone(samsung_pay_card_details.token)

