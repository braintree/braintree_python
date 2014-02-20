from tests.test_helper import *
from datetime import date

class TestDisbursementException(unittest.TestCase):
    def test_constructor(self):
        attributes = {
            'merchant_account_id': 'sandbox_sub_merchant_account',
            'id': '123456',
            'message': 'invalid_account_number',
            'amount': '100.00',
            'disbursement_date': date(2013, 4, 10),
            'follow_up_action': 'update'
        }

        disbursement_exception = DisbursementException(None, attributes)

        self.assertEquals(disbursement_exception.id, '123456')
        self.assertEquals(disbursement_exception.amount, Decimal('100.00'))
