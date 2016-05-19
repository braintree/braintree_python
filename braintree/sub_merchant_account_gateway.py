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

    def update(self, sub_merchant_account_id, params={}):
        Resource.verify_keys(params, SubMerchantAccountGateway._update_signature())
        return self._put("/sub_merchant_accounts/" + sub_merchant_account_id, {"sub_merchant_account": params})

    def _post(self, url, params={}):
        response = self.config.http().post(self.config.base_merchant_path() + url, params)
        if "sub_merchant_account" in response:
            return SuccessfulResult({"sub_merchant_account": SubMerchantAccount(self.gateway, response["sub_merchant_account"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        else:
            pass

    def _put(self, url, params={}):
        response = self.config.http().put(self.config.base_merchant_path() + url, params)
        if "sub_merchant_account" in response:
            return SuccessfulResult({"sub_merchant_account": SubMerchantAccount(self.gateway, response["sub_merchant_account"])})
        elif "api_error_response" in response:
            return ErrorResult(self.gateway, response["api_error_response"])
        else:
            pass

    @staticmethod
    def _create_signature():
        return [
            {'business': [
                {'address': [
                    'country',
                    'locality',
                    'postal_code',
                    'region',
                    'street_address',
                    ],
                },
                'dba_name',
                'legal_name',
                'registered_as',
                'registration_number',
                'tax_id',
                'vat',
                ],
            },
            {'contacts': [
                {'address': [
                    'country',
                    'locality',
                    'postal_code',
                    'region',
                    'street_address',
                    ],
                },
                'date_of_birth',
                'email',
                'first_name',
                'last_name',
                'phone',
                ]
            },
            {'funding': [
                'account_holder_name',
                'account_number',
                'currency_iso_code',
                'descriptor',
                'routing_number',
                ]
            },
            'id',
            'tos_accepted',
            'verify_identity',
        ]

    @staticmethod
    def _update_signature():
        return [
            {'business': [
                {'address': [
                    'country',
                    'locality',
                    'postal_code',
                    'region',
                    'street_address',
                    ],
                },
                'dba_name',
                'legal_name',
                'registered_as',
                'registration_number',
                'tax_id',
                'vat',
                ],
            },
            {'contacts': [
                {'address': [
                    'country',
                    'locality',
                    'postal_code',
                    'region',
                    'street_address',
                    ],
                },
                'date_of_birth',
                'email',
                'first_name',
                'id',
                'last_name',
                'phone',
                ]
            },
            {'funding': [
                'account_holder_name',
                'account_number',
                'currency_iso_code',
                'descriptor',
                'routing_number',
                ]
            },
            'id',
            'tos_accepted',
            'verify_identity',
        ]
