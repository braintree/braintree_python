from tests.test_helper import *
from braintree import *

class TestThreeDSecureInfo(unittest.TestCase):
    def test_initialization_of_attributes(self):
        three_d_secure_info = ThreeDSecureInfo({
            "cavv": "somebase64value",
            "xid": "xidvalue",
            "enrolled": "Y",
            "status": "authenticate_successful",
            "liability_shifted": True,
            "liability_shift_possible": True,
        })

        self.assertEquals("Y", three_d_secure_info.enrolled)
        self.assertEquals("authenticate_successful", three_d_secure_info.status)
        self.assertEquals("xidvalue", three_d_secure_info.xid)
        self.assertEquals("somebase64value", three_d_secure_info.cavv)
        self.assertEquals(True, three_d_secure_info.liability_shifted)
        self.assertEquals(True, three_d_secure_info.liability_shift_possible)

