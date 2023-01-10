from tests.test_helper import *
from datetime import date

class TestSepaDirectDebitAccount(unittest.TestCase):
    def test_constructor(self):
        attributes = {
            "bank_reference_token": "a-reference-token",
            "mandate_type": "ONE_OFF",
            "last_4": "4321",
            "merchant_or_partner_customer_id": "a-mp-customer-id",
            "customer_global_id": "a-customer-global-id",
            "global_id": "a-global-id",
            "image_url": "a-image-url",
            "view_mandate_url": "a-view-mandate-url",
            "created_at": date(2013, 4, 10),
            "updated_at": date(2013, 4, 10),
        }

        sepa_direct_debit_account = SepaDirectDebitAccount({}, attributes)
        self.assertEqual(sepa_direct_debit_account.bank_reference_token, "a-reference-token")
        self.assertEqual(sepa_direct_debit_account.mandate_type, "ONE_OFF")
        self.assertEqual(sepa_direct_debit_account.last_4, "4321")
        self.assertEqual(sepa_direct_debit_account.merchant_or_partner_customer_id, "a-mp-customer-id")
        self.assertEqual(sepa_direct_debit_account.customer_global_id, "a-customer-global-id")
        self.assertEqual(sepa_direct_debit_account.global_id, "a-global-id")
        self.assertEqual(sepa_direct_debit_account.image_url, "a-image-url")
        self.assertEqual(sepa_direct_debit_account.view_mandate_url, "a-view-mandate-url")
        self.assertEqual(sepa_direct_debit_account.created_at, date(2013, 4, 10))
        self.assertEqual(sepa_direct_debit_account.updated_at, date(2013, 4, 10))
