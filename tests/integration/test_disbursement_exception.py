from tests.test_helper import *
from datetime import date

class TestDisbursementException(unittest.TestCase):
    def test_disbursement_exception_has_merchant_account(self):
        disbursement_exception = DisbursementException(Configuration.gateway(), {"merchant_account_id": "sandbox_sub_merchant_account", "amount": 100})

        self.assertEquals("sandbox_sub_merchant_account", disbursement_exception.merchant_account.id)

    def test_disbursement_exception_memoizes_merchant_account(self):
        disbursement_exception = DisbursementException(Configuration.gateway(), {"merchant_account_id": "sandbox_sub_merchant_account", "amount": 100})

        merchant_account = disbursement_exception.merchant_account

        disbursement_exception.merchant_account_id = 'non_existant'
        self.assertEquals(merchant_account.id, disbursement_exception.merchant_account.id)

    def test_disbursement_exception_finds_transactions(self):
        disbursement_exception = DisbursementException(Configuration.gateway(), {
            "merchant_account_id": "sandbox_sub_merchant_account",
            "amount": 100,
            "disbursement_date": date(2013, 4, 10)
        })

        self.assertEquals(1, disbursement_exception.transactions.maximum_size)
        self.assertEquals("sub_merchant_transaction", disbursement_exception.transactions.first.id)
