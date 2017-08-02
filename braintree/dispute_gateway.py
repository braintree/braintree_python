import braintree
from braintree.dispute import Dispute
from braintree.exceptions.not_found_error import NotFoundError

class DisputeGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, dispute_id):
        try:
            if dispute_id is None or dispute_id.strip() == "":
                raise NotFoundError()
            response = self.config.http().get(self.config.base_merchant_path() + "/disputes/" + dispute_id)
            return Dispute(response["dispute"])
        except NotFoundError:
            raise NotFoundError("dispute with id " + repr(dispute_id) + " not found")
