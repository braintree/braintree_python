import braintree
import re
from braintree.dispute import Dispute
from braintree.dispute_details import DisputeEvidence
from braintree.error_result import ErrorResult
from braintree.successful_result import SuccessfulResult
from braintree.exceptions.not_found_error import NotFoundError

class DisputeGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def accept(self, dispute_id):
        try:
            if dispute_id is None or dispute_id.strip() == "":
                raise NotFoundError()

            response = self.config.http().put(self.config.base_merchant_path() + "/disputes/" + dispute_id + "/accept")

            if "api_error_response" in response:
                return ErrorResult(self.gateway, response["api_error_response"])
            else:
                return SuccessfulResult()
        except NotFoundError:
            raise NotFoundError("dispute with id " + repr(dispute_id) + " not found")

    def add_text_evidence(self, dispute_id, content):
        try:
            if dispute_id is None or dispute_id.strip() == "":
                raise NotFoundError()
            if content is None or content.strip() == "":
                raise ValueError("content cannot be blank")

            response = self.config.http().post(self.config.base_merchant_path() + "/disputes/" + dispute_id + "/evidence", {
                "comments": content
                })

            if "evidence" in response:
                return SuccessfulResult({
                    "evidence": DisputeEvidence(response["evidence"])
                    })
            elif "api_error_response" in response:
                return ErrorResult(self.gateway, response["api_error_response"])
        except NotFoundError:
            raise NotFoundError("dispute with id " + repr(dispute_id) + " not found")

    def finalize(self, dispute_id):
        try:
            if dispute_id is None or dispute_id.strip() == "":
                raise NotFoundError()

            response = self.config.http().put(self.config.base_merchant_path() + "/disputes/" + dispute_id + "/finalize")

            if "api_error_response" in response:
                return ErrorResult(self.gateway, response["api_error_response"])
            else:
                return SuccessfulResult()
        except NotFoundError:
            raise NotFoundError("dispute with id " + repr(dispute_id) + " not found")

    def find(self, dispute_id):
        try:
            if dispute_id is None or dispute_id.strip() == "":
                raise NotFoundError()

            response = self.config.http().get(self.config.base_merchant_path() + "/disputes/" + dispute_id)
            return Dispute(response["dispute"])
        except NotFoundError:
            raise NotFoundError("dispute with id " + repr(dispute_id) + " not found")

    def remove_evidence(self, dispute_id, evidence_id):
        try:
            if dispute_id is None or dispute_id.strip() == "":
                raise NotFoundError()
            if evidence_id is None or evidence_id.strip() == "":
                raise NotFoundError()

            response = self.config.http().delete(self.config.base_merchant_path() + "/disputes/" + dispute_id + "/evidence/" + evidence_id)

            if "api_error_response" in response:
                return ErrorResult(self.gateway, response["api_error_response"])
            else:
                return SuccessfulResult()
        except NotFoundError:
            raise NotFoundError("evidence with id " + repr(evidence_id) + " for dispute with id " + repr(dispute_id) + " not found")
