from braintree.error_result import ErrorResult
from braintree.sub_merchant_account import SubMerchantAccount
from braintree.resource import Resource
from braintree.successful_result import SuccessfulResult
from braintree.exceptions.not_found_error import NotFoundError

class SubMerchantAccountGateway(object):
    def __init__(self, gateway):
        self.gateway = gateway
        self.config = gateway.config

    def create(self, params={}):
        Resource.verify_keys(params, SubMerchantAccountGateway._create_signature())
        return self._post("/sub_merchant_accounts", {"sub_merchant_account": params})

    def _post(self, url, params={}):
        response = self.config.http().post(self.config.base_merchant_path() + url, params)
        return SuccessfulResult({"sub_merchant_account": SubMerchantAccount(self.gateway, response["sub_merchant_account"])})

    @staticmethod
    def _create_signature():
        return [
            {'director': [
                'first_name',
                'last_name',
                'email',
                ]
            },
            {'business': [
                'legal_name',
                'registered_as',
                {'address': [
                    'country'
                    ],
                },
                ],
            },
            {'funding': [
                'currency_iso_code',
                ]
            },
            'tos_accepted',
            'id',
        ]
