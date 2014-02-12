from tests.test_helper import *
from datetime import date

class TestTransfer(unittest.TestCase):
    def test_constructor(self):
        attributes = {
            'merchant_account_id': 'sandbox_sub_merchant_account',
            'id': '123456',
            'message': 'invalid_account_number',
            'amount': '100.00',
            'disbursement_date': date(2013, 4, 10),
            'follow_up_action': 'update'
        }

        transfer = Transfer(None, attributes)

        self.assertEquals(transfer.id, '123456')
        self.assertEquals(transfer.amount, Decimal('100.00'))
