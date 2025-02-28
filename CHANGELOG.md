# Changelog
## 4.34.0
* Add prepaid_reloadable from bin data in credit card responses
* Add support for `PayPalPaymentResource` requests

## 4.33.1
* Fixes issue related to missing folders in package paths

## 4.33.0
* Add support for creating and updating PayPal customer session
* Add support for getting PayPal customer recommendations

## 4.32.0 
* Add recipient/contact info: `recipient_email`and `recipient_phone` to `Transaction` 

## 4.31.0
* Add `fail_on_duplicate_payment_method_for_customer` option to 
  * `ClientToken`
  * `PaymentMethod`
  * `CreditCard`
* Add `blik_aliases` to LocalPaymentCompleted webhook and LocalPaymentDetail
* Deprecate `samsung_pay_card`
* Updated expiring pinned vendor SSL certificates

## 4.30.0
* Add `payer_name`, `bic` and `iban_last_chars` to LocalPaymentCompleted webhook
* Add `edit_paypal_vault_id` to PayPalAccount
* Add `ani_first_name_response_code` and `ani_last_name_response_code` to CreditCardVerification
* Add `shippingTaxAmount` to Transaction
* Add `network_tokenization_attributes` parameter to `Transaction.sale`
* Add validation error code `NetworkTokenizationAttributeCryptogramIsRequired` to `CreditCard`

## 4.29.0
* Add `foreign_retailer` to Transaction
* Add `international_phone` to `Address` and `Customer`
* Add `funding_source_description` to PayPalAccount
* Add missing `AndroidPayCard` error code
* Add `REFUND_FAILED` to `WebhookNotification.Kind`
* Add `final_capture` to Transaction `submit_for_partial_settlement_signature`
* Deprecate `paypal_tracking_id` in favor of `paypal_tracker_id` in `package_details`

## 4.28.0
* Add `domains` parameter support to `ClientToken.generate`

## 4.27.0
* Add `UnderReview` status to `Dispute`
* Add `DisputeUnderReview` to `WebhookNotification.Kind`

## 4.26.0
* Remove usage of standard library deprecated `cgi` module. _Note: this will break integrations on versions of Python below 3.2. However, this is NOT a breaking change to this library, due to our current support of Python 3.5+._
* Add `PackageDetails` class.
* Add `packages` to `Transaction` attributes.
* Add `package_tracking` method to `TransactionGateway` to make request to add tracking information to transactions.
* Add `process_debit_as_credit` to `credit_card` field in `options` field during Transaction create.
* Deprecate `three_d_secure_token` in favor of `three_d_secure_authentication_id`
* Add `upc_code`, `upc_type`, and `image_url` to `line_items` in `transaction`
* Deprecate `venmo_sdk_session` and `venmo_sdk_payment_method_code`

## 4.25.0
* Add `PickupInStore` to `ShippingMethod` enum
* Add `external_vault` and `risk_data` to `CreditCardVerification.create` request
* Add `phone_number` in `CreditCard`
* Add `debit_network` to `Transaction` field
* Add `debit_network` to `TransactionSearch` Request
* Add `DebitNetwork` enum to `CreditCard`

## 4.24.0
* Add `SubscriptionBillingSkipped` to `WebhookNotification.Kind`
* Add `arrivalDate` and `ticketIssuerAddress` to `Transaction.sale` request and `industry` data support for Transaction.submitForSettlement
* Add `date_of_birth` and `country_code` to IndustryData params
* Add `MetaCheckoutCard`, `MetaCheckoutToken` payment methods
* Add `MetaCheckoutCardDetails`, `MetaCheckoutTokenDetails` to `Transaction`
* Add `verification_add_ons` to `PaymentMethod` create options for `ACH NetworkCheck`
* Fix unittest compatibility with Python 3.12 (Thanks @mgorny)

## 4.23.0
* Deprecate `evidenceSubmittable` in Dispute 
* Add missing `escape` calls in `generator` for:
  * list
  * bool
  * integer
  * datetime

## 4.22.0 
* Add `processing_overrides` to `Transaction.sale` options

## 4.21.0
* Add `evidence_submittable` to `Dispute`
* Add `merchant_token_identifier` and `source_card_last4` to `ApplePayCard`
* Add a check for empty month and year before generating `expiration_date` in:
  * `CrediCard`
  * `AndroidPayCard`
  * `ApplePayCard`
  * `SamsungPayCard`
  * `VisaCheckoutCard`
* Add `retry_ids` and `retried_transaction_id` to Transaction object

## 4.20.0
* Add `merchant_advice_code` and `merchant_advice_code_text` to Transaction object
* Allow vaulting of raw AndroidPayCards with billing address via Customer.create/update

## 4.19.0
* Add `intended_transaction_source` to `CreditCardVerification`
* Add `three_d_secure_pass_thru` to `CreditCardVerification`
* Add `payment_method_nonce` to `CreditCardVerification`
* Add `three_d_secure_authentication_id` to `CreditCardVerification`
* Add support for subscriptions in SEPA direct debit accounts

## 4.18.1
* Fixup issue where request sessions weren't including proxy settings (see [#5677](https://github.com/psf/requests/issues/5677) for details).

## 4.18.0
* Replace nose usage for tests with unittest (Thanks @arthurzam)
* Remove mock dev dependency (Thanks @arthurzam)
* Add `ExcessiveRetry` to `GatewayRejectionReason`
* Add `pre_dispute_program` to `Dispute` and `DisputeSearch`
* Add `AutoAccepted` status to `Dispute`
* Add `DisputeAutoAccepted` to `WebhookNotification.Kind`
* Deprecate `chargeback_protection_level` and add `protection_level` to `Dispute` and `DisputeSearch`
* Add `shipping` object to `submit_for_settlement_signature`
* Add `SEPADirectDebitAccount` payment method
* Add `SEPADirectDebitAccount` to transaction object
* Add `SEPA_DIRECT_DEBIT_ACCOUNT` to `PaymentInstrumentType`
* Add `sepa_debit_paypal_v2_order_id` to `TransactionSearch`
* Add `sepa_direct_debit_accounts` to `Customer`
* Add SEPA Direct Debit specific error codes

## 4.17.1
* Prepare http request before setting url to resolve issue where dot segments get normalized

## 4.17.0
* Fix `DeprecationWarning` on invalid escape sequences (thanks @DavidCain)
* Add validation for arguments in Address.delete, Address.find, and Address.update

## 4.16.0
* Add `LiabilityShift` class and `liability_shift` to RiskData
* Add ExchangeRateQuote API
* Add `ach_return_responses_created_at` and `reason_code` fields in TransactionSearch
* Allow vaulting of raw ApplePayCards with billing address via Customer.create/update

## 4.15.2
* Add `retried` to `Transaction`

## 4.14.0
* Add `PaymentMethodCustomerDataUpdated` webhook

## 4.13.0
* Add plan create/update/find API endpoint
* Add `TransactionReview` webhook notification
* Fix typos (@timgates42)

## 4.12.0
* Add `localPaymentFunded` and `localPaymentExpired` webhooks

## 4.11.0
* Add `exchange_rate_quote_id` to `Transaction.sale`
* Add validation error code `ExchangeRateQuoteIdIsTooLong` to `Transaction`
* Add the following fields to `ApplePayCard` and `AndroidPayCard`:
  * `commercial`
  * `debit`
  * `durbin_regulated`
  * `healthcare`
  * `payroll`
  * `prepaid`
  * `product_id`
  * `country_of_issuance`
  * `issuing_bank`
* Add error code `Transaction.TaxAmountIsRequiredForAibSwedish` for attribute `tax_amount` to handle validation for AIB:Domestic Transactions in Sweden


## 4.10.0
* Add `payment_reader_card_details` parameter to `Transaction.sale`
* Add webhook sample for `GrantedPaymentMethodRevoked`
* Add `chargeback_protection_level` to `DisputeSearch`
* Add `skip_advanced_fraud_checking` to:
  * `PaymentMethod.create` and `PaymentMethod.update`
  * `CreditCard.create` and `CreditCard.update`

## 4.9.0
* Add `paypal_messages` to `Dispute`
* Add `tax_identifiers` parameter to `Customer.create` and `Customer.update`

## 4.8.0
* Add `LocalPaymentReversed` webhook
* Add `store_id` and `store_ids` to `Transaction.search`

## 4.7.0
* Add `merchant_account_id` to `Transaction.refund`
* Add `Transaction.adjust_authorization` method to support for multiple authorizations for a single transaction

## 4.6.0
* Add `installments` to `Transaction` requests
* Add `count` to `installments`
* Deprecate `device_session_id` and `fraud_merchant_id` in `CreditCardGateway`, `CustomerGateway`, `PaymentMethodGateway`, and `TransactionGateway` classes
* Add `sca_exemption` to Transaction.sale request

## 4.5.0
* Add `acquirer_reference_number` to `Transaction`
* Deprecate `recurring` in Transaction sale requests

## 4.4.0
* Deprecate `masterpass_card` and `amex_checkout_card` payment methods
* Fix issue where `transaction.credit` could not be called using a gateway object

## 4.3.0
* Add validation error code `Transaction.ProductSkuIsInvalid`
* Add 'RiskThreshold' gateway rejection reason
* Add `processed_with_network_token` to `Transaction`
* Add `is_network_tokenized` to `CreditCard`

## 4.2.0
* Add `retrieval_reference_number` to `Transaction`
* Add `network_transaction_id` to `CreditCardVerification`
* Add `product_sku` to `Transaction`
* Add `customer_device_id`, `customer_location_zip`, and `customer_tenure` to `RiskData`
* Add `phone_number` and `shipping_method` to `Address`
* Add validation error codes:
  * `Transaction.ShippingMethodIsInvalid`
  * `Transaction.ShippingPhoneNumberIsInvalid`
  * `Transaction.BillingPhoneNumberIsInvalid`
  * `RiskData.CustomerBrowserIsTooLong`
  * `RiskData.CustomerDeviceIdIsTooLong`
  * `RiskData.CustomerLocationZipInvalidCharacters`
  * `RiskData.CustomerLocationZipIsInvalid`
  * `RiskData.CustomerLocationZipIsTooLong`
  * `RiskData.CustomerTenureIsTooLong`

## 4.1.0
* Add `DisputeAccepted`, `DisputeDisputed`, and `DisputeExpired` webhook constants
* Add `three_d_secure_pass_thru` to `CreditCard.create`, `CreditCard.update`, `PaymentMethod.create`, `PaymentMethod.update`, `Customer.create`, and `Customer.update`.
* Add `Verification` validation errors for 3D Secure
* Add `payment_method_token` to `CreditCardVerificationSearch`
* Add `recurring_customer_consent` and `recurring_max_amount` to `authentication_insight_options` for `PaymentMethodNonce.create`
* Add `FileIsEmpty` error code
* Eliminates usage of mutable objects for function parameters. Resolves #113 Thank you @maneeshd!

## 4.0.0
* Split development and deployments requirements files out
* Add `Authentication Insight` to payment method nonce create
* Add ThreeDSecure test payment method nonces
* Add test `AuthenticationId`s
* Add `three_d_secure_authentication_id` to `three_d_secure_info`
* Add `three_d_secure_authentication_id` support for transaction sale
* Breaking Changes
  * Require Python 3.5+
  * Remove deprecated Transparent Redirect
  * Remove deprecated iDeal payment method
  * Apple Pay register_domains returns an ApplePayOptions object
  * Remove `unrecognized` status from Transaction, Subscription, and CreditCardVerification
  * Remove `GrantedPaymentInstrumentUpdate` kind from Webhook
  * Remove Coinbase references
  * Add GatewayTimeoutError, RequestTimeoutError exceptions
  * Rename DownForMaintenanceError exception to ServiceUnavailableError
  * Transaction `line_items` only returns the line items for a transaction response object. Use TransactionLineItem `find_all` to search all line items on a transaction, given a transaction_id
  * Upgrade API version to retrieve declined refund transactions
  * Remove all deprecated parameters, errors, and methods

## 3.59.0
* Add `RefundAuthHardDeclined` and `RefundAuthSoftDeclined` to validation errors
* Fix issue where managing Apple Pay domains would fail in Python 3.8+
* Add level 2 processing options `purchase_order_number`, `tax_amount`, and `tax_exempt` to `Transaction.submit_for_settlement`
* Add level 3 processing options `discount_amount`, `shipping_amount`, `ships_from_postal_code`, `line_items` to `Transaction.submit_for_settlement`

## 3.58.0
* Add support for managing Apple Pay domains (thanks @ethier #117)
* Fix error when running against Python 3.8 (thanks @felixonmars #114)
* Add `ProcessorDoesNotSupportMotoForCardType` to validation errors
* Add Graphql ID to `CreditCardVerification`, `Customer`, `Dispute`, and `Transaction`

## 3.57.1
* Set correct version for PyPi

## 3.57.0
* Forward `processor_comments` to `forwarded_comments`
* Add Venmo 'TokenIssuance' gateway rejection reason
* Add `AmountNotSupportedByProcessor` to validation error

## 3.56.0
* Add PayPalHere details
* Add `networkResponseCode` and `networkResponseText` to transactions and verifications
* Add `cavv`, `xid`, `ds_transaction_id`, `eci_flag`, and `three_d_secure_version`, to `three_d_secure_info`
* Add `three_d_secure_info` to credit_card_verification
* Add `GraphQLClient` to `BraintreeGateway` class

## 3.55.0
* Add `captureId` field to local_payment_details
* Add `refundId` field to local_payment_details
* Add `debugId` field to local_payment_details
* Add `transactionFeeAmount` field to local_payment_details
* Add `transactionFeeCurrencyIsoCode` field to local_payment_details
* Add `refundFromTransactionFeeAmount` field to local_payment_details
* Add `refundFromTransactionFeeCurrencyIsoCode` field to local_payment_details
* Add `ds_transaction_id` and `three_d_secure_version` to 3DS pass thru fields
* Add `payer_info` field to payment_method_nonce details
* Add more specific timeout errors: (#105 thanks @bhargavrpatel)
* Add `braintree.exceptions.http.timeout_error.ConnectTimeoutError` (child class of TimeoutError)
* Add `braintree.exceptions.http.timeout_error.ReadTimeoutError` (child class of TimeoutError)
* Add `room_tax` support for transaction sale
* Add `no_show` support for transaction sale
* Add `advanced_deposit` support for transaction sale
* Add `fire_safe` support for transaction sale
* Add `property_phone` support for transaction sale
* Add `additional_charges` support for transaction sale
* Add `PostalCodeIsRequiredForCardBrandAndProcessor` to validation errors
* Fix issue where not found error could choke on `None` values (#109)

## 3.54.0
* Add `payment_method_nonce` field to `LocalPaymentCompleted` webhook
* Add `transaction` field to `LocalPaymentCompleted` webhook
* Add `LocalPaymentDetails` to transactions

## 3.53.0
* Add `refund_from_transaction_fee_amount` field to paypal_details
* Add `refund_from_transaction_fee_currency_iso_code` field to paypal_details
* Add `revoked_at` field to paypal_account
* Add support for `PaymentMethodRevokedByCustomer` webhook

## 3.52.0
* Deprecate `GrantedPaymentInstrumentUpdate` and add `GrantorUpdatedGrantedPaymentMethod` and `RecipientUpdatedGrantedPaymentMethod`
* Add account_type support for transaction sale, verification, and payment_method create/update

## 3.51.0
* Add Hiper card type support
* Add Hipercard card type support
* Add `bin` to `PaymentMethodNonceDetails`
* Clarify support for Python versions 3.6.x and 3.7.x
* Add Error indicating pdf uploads too long for dispute evidence.
* Add `GrantedPaymentMethodRevoked` webhook response objects

## 3.50.0
* Add `fraud_service_provider` field to `risk_data`
* Add `authorization_expires_at` to `Transaction`
* Remove invalid transaction tests
* Allow PayPal payment ID and payer ID to be passed during transaction create
* Add `travel_flight` support to industry-specific data
* Add `processor_response_type` to `Transaction`, `AuthorizationAdjustment`, and `CreditCardVerification`.

## 3.49.0
* Add new field `network_transaction_id` in transaction response.
* Add `external_vault` option to transaction sale.
* Add `LocalPaymentCompleted` webhook.
* Add `processor_response_type` to `Transaction`, `AuthorizationAdjustment`, and `CreditCardVerification`.

## 3.48.0
* Add ID to Transaction in SubscriptionChargedSuccessfully test webhook (#99, thanks @bjackson)
* Fix dispute results in transactions not showing the correct status sometimes
* Add Elo card type support

## 3.47.0
* Add processor respone code and processor response text to authorization adjustments subfield in transaction response.
* Add support for Samsung Pay

## 3.46.0
* Allow payee ID to be passed in options params for transaction create
* Add `merchant_id` alias to ConnectedMerchantStatusTransitioned and ConnectedMerchantPayPalStatusChanged Auth webhooks

## 3.45.0
* Add support for US Bank Account verifications API

## 3.44.0
* Add Dispute error ValidEvidenceRequiredToFinalize

## 3.43.0
* Add `oauth_access_revocation` to `WebhookNotification`s
* Add support for `customer_id`, `disbursement_date` and `history_event_effective_date` in DisputeSearch
* Remove `sepa_mandate_type` and `sepa_mandate_acceptance_location` params from `ClientToken`
* Add support for VCR compelling evidence dispute representment

## 3.42.0
* Add support for `association_filter_id` in `Customer#find`

## 3.41.0
* Deprecated `LineItem/DiscountAmountMustBeGreaterThanZero` error in favor of `DiscountAmountCannotBeNegative`
* Deprecated `LineItem/UnitTaxAmountMustBeGreaterThanZero` error in favor of `UnitTaxAmountCannotBeNegative`
* Add support for `tax_amount` field on transaction `line_items`
* Add support for `source_merchant_id` on webhooks
* Add `find_all` static method to `TransactionLineItem` class
* Add support for `profile_id` in Transaction#create options for VenmoAccounts

## 3.40.0
* Add level 3 fields to Transactions:
  * discount_amount
  * shipping_amount
  * ships_from_postal_code
* Add support for transaction line items
* Add support for tagged evidence in DisputeGateway#add_text_evidence (Beta release)
* Update https certificate bundle

## 3.39.1
* Fix spec to expect PayPal transactions to move to settling rather than settled
* Fix AchMandate.acceptedAt attribute parsing
* Fix regression for `http_strategy.http_do`

## 3.39.0
* Add support for upgrading a PayPal future payment refresh token to a billing agreement
* Fix braintree.Dispute.search to take a list of search criteria
* Add logic to remove deprecation warnings for encodestring and decodestring when used with python 3 (#92)
* Fix spec to expect PayPal transaction to settle immediately after successful capture
* Add GrantedPaymentInstrumentUpdate webhook support
* Add ability to create a transaction from a shared nonce
* Add `options` -> `paypal` -> `shipping` for creating & updating customers as well as creating payment methods
* Do not convert to Decimal if amount is None in AuthorizationAdjustement (#70)
* Add `device_data_captured` field to `risk_data`
* Add `bin_data` to `payment_method_nonce`

## 3.38.0
* Add iDEAL webhook support
* Add AuthorizationAdjustment class and `authorization_adjustments` to Transaction
* Coinbase is no longer a supported payment method. `PaymentMethodNoLongerSupported` will be returned for Coinbase operations
* Add facilitated details to Transaction if present
* Add `submit_for_settlement` option to `Subscription.retry_charge`
* Add `options` -> `paypal` -> `description` for creating and updating subscriptions
* Add Braintree.Dispute.find
* Add braintree.Dispute.accept
* Add braintree.Dispute.add_file_evidence
* Add braintree.Dispute.add_text_evidence
* Add braintree.Dispute.finalize
* Add braintree.Dispute.find
* Add braintree.Dispute.remove_evidence
* Add braintree.Dispute.search
* Add braintree.DocumentUpload

## 3.37.2
* Fix a bug where a null value for `amount` in `CreditCardVerification` would result in a `ValueError`
* Add docstrings for AttributeGetter and Search. Thanks @sharma7n!
* Add support for additional PayPal options when vaulting a PayPal Order

## 3.37.1
* Add gzip support
* Fix a bug in CreditCardVerification where `amount` and `currency_iso_code` were always expected

## 3.37.0
* Fix a regression where `util/datetime_parser.py` was missing
* Add support for Visa Checkout
* Improve setup.py
* Verification response includes amount and currency iso code
* Add support for payee_email with paypal intent=order
* Add support for skip_avs & skip_cvs

## 3.36.0
* Add ConnectedMerchantStatusTransitioned and ConnectedMerchantPayPalStatusChanged Auth webhooks

## 3.35.0
* Add LICENSE metadata. Thanks graingert.
* Allow custom verification amount on payment method updates.
* Fix a bug where `merchant_account.all` would attempt to fetch too many pages of merchant accounts

##  3.34.0
* Stop sending account_description field from us bank accounts
* Add functionality to list all merchant accounts for a merchant with `merchant_account.all`

## 3.33.0
* Add option `skip_advanced_fraud_check` for transaction flows

## 3.32.0
* Update UsBank tests to use legal routing numbers
* Allow setting a custom verification amount in `PaymentMethod` options
* Allow setting processor specific fields for transactions and verifications

## 3.31.0
* Fix `UsBankAccount` support for `Customer`s
* Added handling for unicode parameters. (Thanks @mgalgs)
* Raise `ConfigurationError` for empty string credentials
* Update `Grant` api to support options dictionary

## 3.30.0
* Add 'UsBankAccount' payment method

## 3.29.2
* Update links in docstrings
* Remove Python 3.x-incompatible branch check
* Remove references to SubMerchantAccount API

## 3.29.1
* Improve error handling around server timeouts

## 3.29.0
* Allow 'default_payment_method' option in Customer
* Allow 'transaction_source' option in Transaction Sale

## 3.28.0
* Expose resource collection ids
* Add order id to refund
* Enable 3DS pass thru

## 3.27.0
* Add method of revoking OAuth access tokens

## 3.26.1
* Correct issue with setup.py

## 3.26.0
* Add Transaction `update_details`
* Support for Too Many Requests response codes
* Add SubMerchantAccount object with associate objects
* Allow more parameters to be sent on SubMerchantAccount create
* Add SubMerchantAccount update
* Handle validation errors for SubMerchantAccount create / update

## 3.25.0
* Add AccountUpdaterDailyReport webhook parsing

## 3.24.0
* Add Verification#create
* Add options to `submit_for_settlement` transaction flows
* Update https certificate bundle
* Support environment settings with strings

## 3.23.0
* Add better defaults to client token generation when using an access token by consolidating client token defaults into ClientTokenGateway
* Add PaymentMethodGateway#revoke

## 3.22.0
* Add VenmoAccount
* Add support for Set Transaction Context supplementary data.

## 3.21.0
* Add transaction to subscription successfully charged webhook
* Add new ProcessorDoesNotSupportAuths error
* Add support for partial settlement transactions
* Add constants for dispute kind
* Preserve backtrace when not wrapping HTTP exceptions
* Add date_opened and date_won to dispute webhooks
* Add support for searching transactions from oauth app
* Support AMEX express checkout

## 3.20.0
* add source\_description to android pay and apple pay
* add new android pay test nonces
* add support for amex rewards transactions
* add billing\_agreement\_id to paypalaccount

## 3.19.0
* Add new test payment method nonces
* Allow passing description on PayPal transactions

## 3.18.0
* Fix oauth authentication
* Fix python 3 syntax

## 3.17.0
* Add oauth support

## 3.16.0
* Add support for Android Pay

## 3.15.0
* Validate webhook challenge payload

## 3.14.0
* Add 3DS server side fields

## 3.13.0
* Add attribute to customer
* Add coinbase constant
* Add European test nonce

## 3.12.0
* Add support for new SEPA workflow

## 3.11.1
* Fix test failures in Python 3.3+

## 3.11.0
* Accept additional params in PaymentMethod.create()

## 3.10.0
* Add 3D Secure transaction fields
* Add ability to create nonce from vaulted payment methods

## 3.9.0
* Support Coinbase accounts
* Surface Apple Pay payment instrument name in responses
* Expose subscription status events
* Support SEPA bank accounts for customer
* Improve documentation

## 3.8.0
* Add error code constants
* Allow PayPal parameters to be sent in options.paypal

## 3.7.0
* Add risk_data to Transaction and Verification with Kount decision and id
* Add verification_amount an option when creating a credit card
* Add TravelCruise industry type to Transaction
* Add room_rate to Lodging industry type
* Add CreditCard#verification as the latest verification on that credit card
* Add ApplePay support to all endpoints that may return ApplePayCard objects
* Align WebhookTesting with other client libraries

## 3.6.0
* Allow descriptor to be passed in Funding Details options params for Merchant Account create and update.

## 3.5.0
* Add additional_processor_response to transaction

## 3.4.1
* Allow payee_email to be passed in options params for Transaction create

## 3.4.0

* Added paypal specific fields to transaction calls
* Added SettlementPending, SettlementDeclined transaction statuses

## 3.3.0

* Add Descriptor url support
* Fix client token version type

## 3.2.0

* Support credit card options and billing address in PaymentMethod.create
* Add PaymentMethod.update
* Add associated subscriptions to PayPalAccount
* Test refactoring and cleanup

## 3.1.1

* Add support for v.zero SDKs

## 3.0.0

* Drop Python 2.5 support
* Remove use_unsafe_ssl option
* Remove httplib strategy and pycurl strategy
* Add Python 3.3+ support

## 2.29.1

* Make webhook parsing more robust with newlines
* Add messages to InvalidSignature exceptions

## 2.29.0

* Include Dispute information on Transaction
* Search for Transactions disputed on a certain date

## 2.28.0

* Disbursement Webhooks

## 2.27.0

* Fix using instantiated Configuration objects without first calling Configuration.configure
* Accept billing_address_id on transaction create
* Expose current_billing_cycle on addons and discounts

## 2.26.0

* Merchant account find API

## 2.25.0

* Merchant account update API
* Merchant account create API v2

## 2.24.1
* Update configuration URLs

## 2.24.0
* Add partnership support
* Add partner configuration

## 2.23.1
* Add configuration option for custom HTTP strategies

## 2.23.0
* Adds hold_in_escrow method
* Add error codes for verification not supported error
* Add company_name and tax_id to merchant account create
* Adds cancel_release methods
* Adds release_from_escrow functionality
* Adds owner_phone to merchant account signature.
* Adds merchant account phone error code.

## 2.22.0
* Adds device data to transactions, customers, and credit cards.

## 2.21.0
* Adds disbursement details to transactions.
* Adds image_url to transactions.

## 2.20.0

* Support requests >= 1.0
* Add new validation errors and rename old ones

## 2.19.0

* Adds channel field to transactions.

## 2.18.0

* Add additional card types for card type indicators

## 2.17.0

* Adds verification search

## 2.16.0

* Additional card information, such as prepaid, debit, commercial, Durbin regulated, healthcare, and payroll, are returned on credit card responses
* Allows transactions to be specified as recurring

## 2.15.0

* Adds prepaid attribute to credit cards (possible values of: Yes, No, Unknown)

## 2.14.2

* Add settling transaction status to transaction search

## 2.14.1

* Adds new package braintree.util.http_stategy to setup.py

## 2.14.0

* Removes relative imports for python 3.0 (thanks [MichaelBlume](https://github.com/MichaelBlume))
* Adds webhook gateways for parsing, verifying, and testing incoming notifications
* Allow specifying the http strategy to use (PycURL, httplib, requests)

## 2.13.0

* Adds search for duplicate credit cards given a payment method token
* Adds flag to fail saving credit card to vault if card is duplicate

## 2.12.3

* Exposes plan_id on transactions

## 2.12.2

* Added error code for invalid purchase order number
* Fixed zip_safe=False error when building (GitHub issue #17)

## 2.12.1

* Added error message for merchant accounts that do not support refunds

## 2.12.0

* Added ability to retrieve all Plans, AddOns, and Discounts
* Added Transaction cloning

## 2.11.0

* Added SettlementBatchSummary

## 2.10.1

* Enabled gzip encoding for HTTP requests
* Fixed handling of long integers when generating xml (thanks [glencoates](https://github.com/glencoates))
* Added new error code

## 2.10.0

* Added subscription_details to Transaction
* Added flag to store in vault only when a transaction is successful
* Added new error code

## 2.9.1

* Added improvements to unicode handling.

## 2.9.0

* Added a new transaction state, AuthorizationExpired.
* Enabled searching by authorization_expired_at.

## 2.8.0

* Added next_billing_date and transaction_id to subscription search
* Added address_country_name to customer search
* Added new error codes

## 2.7.0

* Added Customer search
* Added dynamic descriptors to Subscriptions and Transactions
* Added level 2 fields to Transactions:
  * tax_amount
  * tax_exempt
  * purchase_order_number

## 2.6.1

* Added billing_address_id to allowed parameters for credit cards create and update
* Allow searching on subscriptions that are currently in a trial period using in_trial_period

## 2.6.0

* Added ability to perform multiple partial refunds on Transactions
* Deprecated Transaction refund_id in favor of refund_ids
* Added revert_subscription_on_proration_failure flag to Subscription update that specifies how a Subscription should react to a failed proration charge
* Deprecated Subscription next_bill_amount in favor of next_billing_period_amount
* Added pycurl dependency in place of M2Crypto for better cross-platform compatibility
* Added new fields to Subscription:
  * balance
  * paid_through_date
  * next_billing_period_amount

## 2.5.0

* Added AddOns/Discounts
* Enhanced Subscription search
* Enhanced Transaction search
* Added constants for CreditCardVerification statuses
* Added Expired and Pending statuses to Subscription
* Allowed prorate_charges to be specified on Subscription update
* Allowed argument lists and literal lists when searching for Subscriptions and Transactions
* Added AddOn/Discount details to Transactions that were created from a Subscription
* All Braintree exceptions now inherit from BraintreeError superclass
* Removed 13 digit Visa Sandbox Credit Card number and replaced it with a 16 digit Visa
* Made gateway operations threadsafe when using multiple configurations
* Added new fields to Subscription:
  * billing_day_of_month
  * days_past_due
  * first_billing_date
  * never_expires
  * number_of_billing_cycles

## 2.4.1

* Added support for M2Crypto version 0.20.1, which is the default for Ubuntu Lucid (thanks [foresto](https://github.com/foresto))

## 2.4.0

* Added unified message to ErrorResult
* Added ability to specify country using country_name, country_code_alpha2, country_code_alpha3, or country_code_numeric (see [ISO_3166-1](https://en.wikipedia.org/wiki/ISO_3166-1))
* Renamed Subscription retryCharge to retry_charge
* Added gateway_rejection_reason to Transaction and Verification
* Allow searching with date objects (in addition to datetime)
* When creating a Subscription, return failed transaction on the ErrorResult if the initial transaction is not successful

## 2.3.0

* Added unified TransparentRedirect url and confirm methods and deprecated old methods
* Added methods to CreditCard to allow searching on expiring and expired credit cards
* Allow credit card verification against a specified merchant account
* Added all method on Customer to retrieve all customers
* Added ability to update a customer, credit card, and billing address in one request
* Allow updating the payment method token on a subscription
* Added methods to navigate between a Transaction and its refund (in both directions)

## 2.2.1

* Use isinstance instead of type to cater to inheritance (thanks [danielgtaylor](https://github.com/danielgtaylor))

## 2.2.0

* Prevent race condition when pulling back collection results -- search results represent the state of the data at the time the query was run
* Rename ResourceCollection's approximate_size to maximum_size because items that no longer match the query will not be returned in the result set
* Correctly handle HTTP error 426 (Upgrade Required) -- the error code is returned when your client library version is no longer compatible with the gateway

## 2.1.0

* Added transaction advanced search
* Added ability to partially refund transactions
* Added ability to manually retry past-due subscriptions
* Added new transaction error codes
* Allow merchant account to be specified when creating transactions
* Allow creating a transaction with a vault customer and new credit card
* Allow existing billing address to be updated when updating credit card

## 2.0.0

* Updated is_success on transaction results to return false on declined transactions
* Search results now return a generator and will automatically paginate data
* Allow passing cardholder_name when creating transactions

## 1.2.0

* Renamed ValidationErrorCollection#all to deep_errors and made it a property
* Added the ability to make a credit card the default card for a customer
* Updated Quick Start in README.md to show a workflow with error checking

## 1.1.0

* Added subscription search
* Return associated subscriptions when finding credit cards
* Raise down for maintenance error instead of forged query string error on 503 responses
* Updated SSL CA file

## 1.0.0

* Initial release
