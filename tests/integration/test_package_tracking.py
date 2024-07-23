import json
from tests.test_helper import *
from braintree.transaction import Transaction

class PackageTracking(unittest.TestCase):
    def setUp(self):
        # Create successful transaction to obtain id
        result = Transaction.sale({
            "amount": "100",
            "options": {
                "submit_for_settlement": True
                },
            "paypal_account": {
                "payer_id": "fake-payer-id",
                "payment_id": "fake-payment-id",
                },
            })
        self.transaction = result.transaction

    def test_package_tracking_returns_error_when_transaction_id_is_not_present(self):
        with self.assertRaisesRegex(NotFoundError, "transaction with id ' ' not found"):
            Transaction.package_tracking(" ")

    def test_package_tracking_returns_api_error_when_carrier_is_not_present(self):
        # Create package without carrier
        package_result = Transaction.package_tracking(
            self.transaction.id,
            {
                "notify_payer": True,
                "tracking_number": "1Z5338FF0107231059",
                "line_items": [
                    {
                        "product_code": "ABC 01",
                        "name": "Best Product Ever",
                        "quantity": "1",
                        "description": "Best Description Ever",
                    },
                ],
            })
        self.assertFalse(package_result.is_success)
        self.assertEqual(package_result.message, 'Carrier name is required.')

    def test_package_tracking_returns_api_error_when_tracking_number_is_not_present(self):
        # Create package without tracking_number
        package_result = Transaction.package_tracking(
            self.transaction.id,
            {
                "notify_payer": True,
                "carrier": "UPS",
                "line_items": [ ],
            })
        self.assertFalse(package_result.is_success)
        self.assertEqual(package_result.message, 'Tracking number is required.')


    def test_package_tracking_adds_information_and_returns_valid_response(self):
        # Create first package with 2 products
        package_result_1 = Transaction.package_tracking(
            self.transaction.id,
            {
                "carrier": "UPS",
                "notify_payer": True,
                "tracking_number": "1Z5338FF0107231059",
                "line_items": [
                    {
                        "product_code": "ABC 01",
                        "name": "Best Product Ever",
                        "quantity": "1",
                        "description": "Best Description Ever",
                        "upc_type": "UPC-A",
                        "upc_code": "9248093u5",
                        "image_url": "https://example.com/image.png"
                    },
                    {
                        "product_code": "ABC 02",
                        "name": "Second best product ever",
                        "quantity": "2",
                        "description": "Second best description ever",
                        "upc_type": "UPC-B",
                        "upc_code": "0586967ABD",
                        "image_url": "https://example.com/image2.png"
                    }
                ],
            })
        self.assertTrue(package_result_1.is_success)
        self.assertIsNotNone(package_result_1.transaction.packages[0])
        self.assertEqual("UPS", package_result_1.transaction.packages[0].carrier)
        self.assertEqual("1Z5338FF0107231059", package_result_1.transaction.packages[0].tracking_number)
        self.assertIsNone(package_result_1.transaction.packages[0].paypal_tracker_id)

        # Create second package with 1 more product
        package_result_2 = Transaction.package_tracking(
            self.transaction.id,
            {
                "carrier": "FEDEX",
                "notify_payer": True,
                "tracking_number": "08594809767HGH0L",
                "line_items": [
                    {
                        "product_code": "ABC 03",
                        "name": "Worst Product Ever",
                        "quantity": "25",
                        "description": "Worst Description Ever",
                    }
                ],
            })
        self.assertTrue(package_result_2.is_success)
        self.assertIsNotNone(package_result_2.transaction.packages[1])
        self.assertEqual("FEDEX", package_result_2.transaction.packages[1].carrier)
        self.assertEqual("08594809767HGH0L", package_result_2.transaction.packages[1].tracking_number)
        self.assertIsNone(package_result_2.transaction.packages[1].paypal_tracker_id)

        transaction_found = Transaction.find(package_result_2.transaction.id)
        self.assertTrue(2, len(transaction_found.packages))
        self.assertIsNotNone(transaction_found.packages[0].id)
        self.assertEqual("UPS", transaction_found.packages[0].carrier)
        self.assertEqual("1Z5338FF0107231059", transaction_found.packages[0].tracking_number)
        # In test environment, since we do not have jobstream setup paypal tracker id is going to be nil, this is just to assert that we could access it
        self.assertIsNone(transaction_found.packages[0].paypal_tracker_id)

        self.assertIsNotNone(transaction_found.packages[1].id)
        self.assertEqual("FEDEX", transaction_found.packages[1].carrier)
        self.assertEqual("08594809767HGH0L", transaction_found.packages[1].tracking_number)
        self.assertIsNone(transaction_found.packages[1].paypal_tracker_id)

    def test_package_tracking_render_paypal_tracker_id(self):
        #find transaction with existing tracker created
        transaction_found = Transaction.find("package_tracking_tx")
        self.assertEqual("paypal_tracker_id_1", transaction_found.packages[0].paypal_tracker_id)
        self.assertEqual("paypal_tracker_id_2", transaction_found.packages[1].paypal_tracker_id)
