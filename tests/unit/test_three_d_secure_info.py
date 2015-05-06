from tests.test_helper import *
from braintree import *

class TestThreeDSecureInfo(unittest.TestCase):
    def test_initialization_of_attributes(self):
        three_d_secure_info = ThreeDSecureInfo({
            "enrolled": "Y",
            "status": "authenticate_successful",
            "liability_shifted": True,
            "liability_shift_possible": True,
        })

        self.assertEquals("Y", three_d_secure_info.enrolled)
        self.assertEquals("authenticate_successful", three_d_secure_info.status)
        self.assertEquals(True, three_d_secure_info.liability_shifted)
        self.assertEquals(True, three_d_secure_info.liability_shift_possible)

