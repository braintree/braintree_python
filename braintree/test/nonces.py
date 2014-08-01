from tests.test_helper import *

class Nonces(object):
    Transactable = "fake-valid-nonce"
    Consumed = "fake-consumed-nonce"
    PayPalOneTimePayment = "fake-paypal-one-time-nonce"
    PayPalFuturePayment = "fake-paypal-future-nonce"

    @staticmethod
    def nonce_for_paypal_account(paypal_account_details):
        client_token =json.loads(TestHelper.generate_decoded_client_token())
        client = ClientApiHttp(Configuration.instantiate(), {
            "authorization_fingerprint": client_token["authorizationFingerprint"]
        })

        status_code, nonce = client.get_paypal_nonce(paypal_account_details)
        return nonce
