from tests.test_helper import *
from datetime import date

class TestTransfer(unittest.TestCase):
    def test_transfer_has_merchant_account(self):
        transfer = Transfer(Configuration.gateway(), {"merchant_account_id": "sandbox_sub_merchant_account", "amount": 100})

        self.assertEquals("sandbox_sub_merchant_account", transfer.merchant_account.id)

    def test_transfer_memoizes_merchant_account(self):
        transfer = Transfer(Configuration.gateway(), {"merchant_account_id": "sandbox_sub_merchant_account", "amount": 100})

        merchant_account = transfer.merchant_account

        transfer.merchant_account_id = 'non_existant'
        self.assertEquals(merchant_account.id, transfer.merchant_account.id)

    def test_transfer_finds_transactions(self):
        transfer = Transfer(Configuration.gateway(), {
            "merchant_account_id": "sandbox_sub_merchant_account",
            "amount": 100,
            "disbursement_date": date(2013, 4, 10)
        })

        self.assertEquals(1, transfer.transactions.maximum_size)
        self.assertEquals("sub_merchant_transaction", transfer.transactions.first.id)
