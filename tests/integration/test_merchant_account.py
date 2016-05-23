from tests.test_helper import *

class TestMerchantAccount(unittest.TestCase):
    DEPRECATED_APPLICATION_PARAMS = {
        "applicant_details": {
            "company_name": "Garbage Garage",
            "first_name": "Joe",
            "last_name": "Bloggs",
            "email": "joe@bloggs.com",
            "phone": "555-555-5555",
            "address": {
                "street_address": "123 Credibility St.",
                "postal_code": "60606",
                "locality": "Chicago",
                "region": "IL",
            },
            "date_of_birth": "10/9/1980",
            "ssn": "123-00-1234",
            "tax_id": "123456789",
            "routing_number": "122100024",
            "account_number": "43759348798"
        },
        "tos_accepted": True,
        "master_merchant_account_id": "sandbox_master_merchant_account"
    }

    VALID_APPLICATION_PARAMS = {
        "individual": {
            "first_name": "Joe",
            "last_name": "Bloggs",
            "email": "joe@bloggs.com",
            "phone": "555-555-5555",
            "address": {
                "street_address": "123 Credibility St.",
                "postal_code": "60606",
                "locality": "Chicago",
                "region": "IL",
            },
            "date_of_birth": "10/9/1980",
            "ssn": "123-00-1234",
        },
        "business": {
            "dba_name": "Garbage Garage",
            "legal_name": "Junk Jymnasium",
            "tax_id": "123456789",
            "address": {
                "street_address": "123 Reputation St.",
                "postal_code": "40222",
                "locality": "Louisville",
                "region": "KY",
            },
        },
        "funding": {
            "routing_number": "122100024",
            "account_number": "43759348798",
            "destination": MerchantAccount.FundingDestination.Bank,
            "descriptor": "Joes Bloggs KY",
        },
        "tos_accepted": True,
        "master_merchant_account_id": "sandbox_master_merchant_account"
    }

    def test_create_accepts_deprecated_parameters(self):
        result = MerchantAccount.create(self.DEPRECATED_APPLICATION_PARAMS)

        self.assertTrue(result.is_success)
        self.assertEquals(MerchantAccount.Status.Pending, result.merchant_account.status)
        self.assertEquals("sandbox_master_merchant_account", result.merchant_account.master_merchant_account.id)

    def test_create_application_with_valid_params_and_no_id(self):
        customer = Customer.create().customer
        result = MerchantAccount.create(self.VALID_APPLICATION_PARAMS)

        self.assertTrue(result.is_success)
        self.assertEquals(MerchantAccount.Status.Pending, result.merchant_account.status)
        self.assertEquals("sandbox_master_merchant_account", result.merchant_account.master_merchant_account.id)

    def test_create_allows_an_id_to_pass(self):
        params_with_id = self.VALID_APPLICATION_PARAMS.copy()
        rand = str(random.randrange(1000000))
        params_with_id['id'] = 'sub_merchant_account_id' + rand
        result = MerchantAccount.create(params_with_id)

        self.assertTrue(result.is_success)
        self.assertEquals(MerchantAccount.Status.Pending, result.merchant_account.status)
        self.assertEquals(params_with_id['id'], result.merchant_account.id)
        self.assertEquals("sandbox_master_merchant_account", result.merchant_account.master_merchant_account.id)

    def test_create_handles_unsuccessful_results(self):
        result = MerchantAccount.create({})
        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.MerchantAccount.MasterMerchantAccountIdIsRequired, result.errors.for_object("merchant_account").on("master_merchant_account_id")[0].code)

    def test_create_requires_all_fields(self):
        result = MerchantAccount.create(
            {"master_merchant_account_id": "sandbox_master_merchant_account",
             "applicant_details": {},
            "tos_accepted": True}
        )
        self.assertFalse(result.is_success)
        self.assertEquals(ErrorCodes.MerchantAccount.ApplicantDetails.FirstNameIsRequired, result.errors.for_object("merchant_account").for_object("applicant_details").on("first_name")[0].code)

    def test_create_funding_destination_accepts_a_bank(self):
        params = self.VALID_APPLICATION_PARAMS.copy()
        params['funding']['destination'] = MerchantAccount.FundingDestination.Bank
        result = MerchantAccount.create(params)
        self.assertTrue(result.is_success)

    def test_create_funding_destination_accepts_an_email(self):
        params = self.VALID_APPLICATION_PARAMS.copy()
        params['funding']['destination'] = MerchantAccount.FundingDestination.Email
        params['funding']['email'] = "junkman@hotmail.com"
        result = MerchantAccount.create(params)
        self.assertTrue(result.is_success)

    def test_create_funding_destination_accepts_a_mobile_phone(self):
        params = self.VALID_APPLICATION_PARAMS.copy()
        params['funding']['destination'] = MerchantAccount.FundingDestination.MobilePhone
        params['funding']['mobile_phone'] = "1112223333"
        result = MerchantAccount.create(params)
        self.assertTrue(result.is_success)

    def test_update_all_merchant_account_fields(self):
        UPDATE_PARAMS = {
            "individual": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "phone": "312-555-1234",
                "address": {
                    "street_address": "123 Fake St",
                    "postal_code": "60622",
                    "locality": "Chicago",
                    "region": "IL",
                },
                "date_of_birth": "1970-01-01",
                "ssn": "987-65-4321",
            },
            "business": {
                "dba_name": "James's Bloggs",
                "legal_name": "James's Junkyard",
                "tax_id": "987654321",
                "address": {
                    "street_address": "456 Fake St",
                    "postal_code": "48104",
                    "locality": "Ann Arbor",
                    "region": "MI",
                },
            },
            "funding": {
                "routing_number": "071000013",
                "account_number": "666666789",
                "destination": MerchantAccount.FundingDestination.Email,
                "email": "check@this.com",
                "mobile_phone": "9998887777",
                "descriptor": "Joes Bloggs MI",
            }
        }

        result = MerchantAccount.update("sandbox_sub_merchant_account", UPDATE_PARAMS)
        self.assertTrue(result.is_success)
        self.assertEquals(result.merchant_account.status, "active")
        self.assertEquals(result.merchant_account.id, "sandbox_sub_merchant_account")
        self.assertEquals(result.merchant_account.master_merchant_account.id, "sandbox_master_merchant_account")
        self.assertEquals(result.merchant_account.individual_details.first_name, "John")
        self.assertEquals(result.merchant_account.individual_details.last_name, "Doe")
        self.assertEquals(result.merchant_account.individual_details.email, "john.doe@example.com")
        self.assertEquals(result.merchant_account.individual_details.date_of_birth, "1970-01-01")
        self.assertEquals(result.merchant_account.individual_details.phone, "3125551234")
        self.assertEquals(result.merchant_account.individual_details.address_details.street_address, "123 Fake St")
        self.assertEquals(result.merchant_account.individual_details.address_details.locality, "Chicago")
        self.assertEquals(result.merchant_account.individual_details.address_details.region, "IL")
        self.assertEquals(result.merchant_account.individual_details.address_details.postal_code, "60622")
        self.assertEquals(result.merchant_account.business_details.dba_name, "James's Bloggs")
        self.assertEquals(result.merchant_account.business_details.legal_name, "James's Junkyard")
        self.assertEquals(result.merchant_account.business_details.tax_id, "987654321")
        self.assertEquals(result.merchant_account.business_details.address_details.street_address, "456 Fake St")
        self.assertEquals(result.merchant_account.business_details.address_details.postal_code, "48104")
        self.assertEquals(result.merchant_account.business_details.address_details.locality, "Ann Arbor")
        self.assertEquals(result.merchant_account.business_details.address_details.region, "MI")
        self.assertEquals(result.merchant_account.funding_details.routing_number, "071000013")
        self.assertEquals(result.merchant_account.funding_details.account_number_last_4, "6789")
        self.assertEquals(result.merchant_account.funding_details.destination, MerchantAccount.FundingDestination.Email)
        self.assertEquals(result.merchant_account.funding_details.email, "check@this.com")
        self.assertEquals(result.merchant_account.funding_details.mobile_phone, "9998887777")
        self.assertEquals(result.merchant_account.funding_details.descriptor, "Joes Bloggs MI")

    def test_update_does_not_require_all_fields(self):
        result = MerchantAccount.update("sandbox_sub_merchant_account", { "individual": { "first_name": "Jose" } })
        self.assertTrue(result.is_success)

    def test_update_handles_validation_errors_for_blank_fields(self):
        params = {
            "individual": {
                "first_name": "",
                "last_name": "",
                "email": "",
                "phone": "",
                "date_of_birth": "",
                "ssn": "",
                "address": {
                    "street_address": "",
                    "postal_code": "",
                    "locality": "",
                    "region": "",
                },
            },
            "business": {
                "legal_name": "",
                "dba_name": "",
                "tax_id": ""
            },
            "funding": {
                "destination": "",
                "routing_number": "",
                "account_number": ""
            }
        }
        result = MerchantAccount.update("sandbox_sub_merchant_account", params)

        self.assertFalse(result.is_success)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("first_name")[0].code, ErrorCodes.MerchantAccount.Individual.FirstNameIsRequired)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("last_name")[0].code, ErrorCodes.MerchantAccount.Individual.LastNameIsRequired)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("date_of_birth")[0].code, ErrorCodes.MerchantAccount.Individual.DateOfBirthIsRequired)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("email")[0].code, ErrorCodes.MerchantAccount.Individual.EmailAddressIsRequired)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").for_object("address").on("street_address")[0].code, ErrorCodes.MerchantAccount.Individual.Address.StreetAddressIsRequired)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").for_object("address").on("postal_code")[0].code, ErrorCodes.MerchantAccount.Individual.Address.PostalCodeIsRequired)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").for_object("address").on("locality")[0].code, ErrorCodes.MerchantAccount.Individual.Address.LocalityIsRequired)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").for_object("address").on("region")[0].code, ErrorCodes.MerchantAccount.Individual.Address.RegionIsRequired)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("destination")[0].code, ErrorCodes.MerchantAccount.Funding.DestinationIsRequired)
        self.assertEquals(len(result.errors.for_object("merchant_account").on("base")), 0)

    def test_update_handles_validation_errors_for_invalid_fields(self):
        params = {
          "individual": {
            "first_name": "<>",
            "last_name": "<>",
            "email": "bad",
            "phone": "999",
            "address": {
              "street_address": "nope",
              "postal_code": "1",
              "region": "QQ",
            },
            "date_of_birth": "hah",
            "ssn": "12345",
          },
          "business": {
            "legal_name": "``{}",
            "dba_name": "{}``",
            "tax_id": "bad",
            "address": {
              "street_address": "nope",
              "postal_code": "1",
              "region": "QQ",
            },
          },
          "funding": {
            "destination": "MY WALLET",
            "routing_number": "LEATHER",
            "account_number": "BACK POCKET",
            "email": "BILLFOLD",
            "mobile_phone": "TRIFOLD"
          },
        }

        result = MerchantAccount.update("sandbox_sub_merchant_account", params)

        self.assertFalse(result.is_success)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("first_name")[0].code, ErrorCodes.MerchantAccount.Individual.FirstNameIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("last_name")[0].code, ErrorCodes.MerchantAccount.Individual.LastNameIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("email")[0].code, ErrorCodes.MerchantAccount.Individual.EmailAddressIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("phone")[0].code, ErrorCodes.MerchantAccount.Individual.PhoneIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").for_object("address").on("street_address")[0].code,  ErrorCodes.MerchantAccount.Individual.Address.StreetAddressIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").for_object("address").on("postal_code")[0].code, ErrorCodes.MerchantAccount.Individual.Address.PostalCodeIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").for_object("address").on("region")[0].code, ErrorCodes.MerchantAccount.Individual.Address.RegionIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("individual").on("ssn")[0].code, ErrorCodes.MerchantAccount.Individual.SsnIsInvalid)

        self.assertEquals(result.errors.for_object("merchant_account").for_object("business").on("legal_name")[0].code, ErrorCodes.MerchantAccount.Business.LegalNameIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("business").on("dba_name")[0].code, ErrorCodes.MerchantAccount.Business.DbaNameIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("business").on("tax_id")[0].code, ErrorCodes.MerchantAccount.Business.TaxIdIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("business").for_object("address").on("street_address")[0].code,  ErrorCodes.MerchantAccount.Business.Address.StreetAddressIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("business").for_object("address").on("postal_code")[0].code, ErrorCodes.MerchantAccount.Business.Address.PostalCodeIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("business").for_object("address").on("region")[0].code, ErrorCodes.MerchantAccount.Business.Address.RegionIsInvalid)

        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("destination")[0].code, ErrorCodes.MerchantAccount.Funding.DestinationIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("routing_number")[0].code, ErrorCodes.MerchantAccount.Funding.RoutingNumberIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("account_number")[0].code, ErrorCodes.MerchantAccount.Funding.AccountNumberIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("email")[0].code, ErrorCodes.MerchantAccount.Funding.EmailAddressIsInvalid)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("mobile_phone")[0].code, ErrorCodes.MerchantAccount.Funding.MobilePhoneIsInvalid)

        self.assertEquals(len(result.errors.for_object("merchant_account").on("base")), 0)

    def test_update_handles_validation_errors_for_business_fields(self):
        result = MerchantAccount.update("sandbox_sub_merchant_account", {
            "business": {
                "legal_name": "",
                "tax_id": "111223333"
                }
            }
        )

        self.assertFalse(result.is_success)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("business").on("legal_name")[0].code, ErrorCodes.MerchantAccount.Business.LegalNameIsRequiredWithTaxId)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("business").on("tax_id")[0].code, ErrorCodes.MerchantAccount.Business.TaxIdMustBeBlank)

        result = MerchantAccount.update("sandbox_sub_merchant_account", {
            "business": {
                "legal_name": "legal name",
                "tax_id": ""
                }
            }
        )

        self.assertFalse(result.is_success)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("business").on("tax_id")[0].code, ErrorCodes.MerchantAccount.Business.TaxIdIsRequiredWithLegalName)

    def test_update_handles_validation_errors_for_funding_fields(self):
        result = MerchantAccount.update("sandbox_sub_merchant_account", {
            "funding": {
                "destination": MerchantAccount.FundingDestination.Bank,
                "routing_number": "",
                "account_number": ""
                }
            }
        )

        self.assertFalse(result.is_success)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("routing_number")[0].code, ErrorCodes.MerchantAccount.Funding.RoutingNumberIsRequired)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("account_number")[0].code, ErrorCodes.MerchantAccount.Funding.AccountNumberIsRequired)

        result = MerchantAccount.update("sandbox_sub_merchant_account", {
            "funding": {
                "destination": MerchantAccount.FundingDestination.Email,
                "email": ""
                }
            }
        )

        self.assertFalse(result.is_success)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("email")[0].code, ErrorCodes.MerchantAccount.Funding.EmailAddressIsRequired)

        result = MerchantAccount.update("sandbox_sub_merchant_account", {
            "funding": {
                "destination": MerchantAccount.FundingDestination.MobilePhone,
                "mobile_phone": ""
                }
            }
        )

        self.assertFalse(result.is_success)
        self.assertEquals(result.errors.for_object("merchant_account").for_object("funding").on("mobile_phone")[0].code, ErrorCodes.MerchantAccount.Funding.MobilePhoneIsRequired)

    def test_find(self):
        result = MerchantAccount.create(self.VALID_APPLICATION_PARAMS)
        self.assertTrue(result.is_success)
        merchant_account_id = result.merchant_account.id
        merchant_account = MerchantAccount.find(merchant_account_id)

    def test_retrieves_master_merchant_account_currency_iso_code(self):
        merchant_account = MerchantAccount.find("sandbox_master_merchant_account")
        self.assertEqual(merchant_account.currency_iso_code,"USD")

    @raises(NotFoundError)
    def test_find_404(self):
        MerchantAccount.find("not_a_real_id")
