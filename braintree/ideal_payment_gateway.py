import braintree
from braintree.ideal_payment import IdealPayment
from braintree.exceptions.not_found_error import NotFoundError

# NEXT_MAJOR_VERSION Remove this class as legacy Ideal has been removed/disabled in the Braintree Gateway
# DEPRECATED If you're looking to accept iDEAL as a payment method contact accounts@braintreepayments.com for a solution.
class IdealPaymentGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, ideal_payment_id):
        try:
            if ideal_payment_id is None or ideal_payment_id.strip() == "":
                raise NotFoundError()

            response = self.config.http().get(self.config.base_merchant_path() + "/ideal_payments/" + ideal_payment_id)
            if "ideal_payment" in response:
                return IdealPayment(self.gateway, response["ideal_payment"])
        except NotFoundError:
            raise NotFoundError("iDEAL payment with token" + repr(ideal_payment_id) + " not found")
