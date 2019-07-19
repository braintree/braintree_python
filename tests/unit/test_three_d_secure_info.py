from tests.test_helper import *
from braintree import *

class TestThreeDSecureInfo(unittest.TestCase):
    def test_initialization_of_attributes(self):
        three_d_secure_info = ThreeDSecureInfo({
            "enrolled": "Y",
            "status": "authenticate_successful",
            "liability_shifted": True,
            "liability_shift_possible": True,
            "cavv": "some_cavv",
            "xid": "some_xid",
            "ds_transaction_id": "some_ds_txn_id",
            "eci_flag": "07",
            "three_d_secure_version": "1.0.2",
        })

        self.assertEqual("Y", three_d_secure_info.enrolled)
        self.assertEqual("authenticate_successful", three_d_secure_info.status)
        self.assertEqual(True, three_d_secure_info.liability_shifted)
        self.assertEqual(True, three_d_secure_info.liability_shift_possible)
        self.assertEqual("some_cavv", three_d_secure_info.cavv)
        self.assertEqual("some_xid", three_d_secure_info.xid)
        self.assertEqual("some_ds_txn_id", three_d_secure_info.ds_transaction_id)
        self.assertEqual("07", three_d_secure_info.eci_flag)
        self.assertEqual("1.0.2", three_d_secure_info.three_d_secure_version)
