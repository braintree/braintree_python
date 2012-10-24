from braintree.credit_card_verification import CreditCardVerification
from braintree.credit_card_verification_search import CreditCardVerificationSearch
from braintree.exceptions.not_found_error import NotFoundError
from braintree.ids_search import IdsSearch
from braintree.resource_collection import ResourceCollection

class CreditCardVerificationGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def find(self, verification_id):
        try:
            if verification_id == None or verification_id.strip() == "":
                raise NotFoundError()
            response = self.config.http().get("/verifications/" + verification_id)
            return CreditCardVerification(self.gateway, response["verification"])
        except NotFoundError:
            raise NotFoundError("Verification with id " + verification_id + " not found")

    def __criteria(self, query):
        criteria = {}
        for term in query:
            if criteria.get(term.name):
                criteria[term.name] = dict(criteria[term.name].items() + term.to_param().items())
            else:
                criteria[term.name] = term.to_param()
        return criteria

    def __fetch(self, query, ids):
        criteria = self.__criteria(query)
        criteria["ids"] = CreditCardVerificationSearch.ids.in_list(ids).to_param()
        response = self.config.http().post("/verifications/advanced_search", {"search": criteria})
        return [CreditCardVerification(self.gateway, item) for item in
                ResourceCollection._extract_as_array(response["credit_card_verifications"], "verification")]


    def search(self, *query):
        if isinstance(query[0], list):
            query = query[0]

        response = self.config.http().post("/verifications/advanced_search_ids", {"search": self.__criteria(query)})
        return ResourceCollection(query, response, self.__fetch)

    def __fetch_verifications(self, query, verification_ids):
        criteria = {}
        criteria["ids"] = IdsSearch.ids.in_list(verification_ids).to_param()
        response = self.config.http().post("/verifications/advanced_search", {"search": criteria})
        return [CreditCardVerification(self.gateway, item) for item in ResourceCollection._extract_as_array(response["credit_card_verifications"], "verification")]
