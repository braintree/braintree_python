3.34.0
------

-  Stop sending account\_description field from us bank accounts
-  Add functionality to list all merchant accounts for a merchant with
   ``merchantAcount.all``

3.33.0
------

-  Add option ``skip_advanced_fraud_check`` for transaction flows

3.32.0
------

-  Update UsBank tests to use legal routing numbers
-  Allow setting a custom verification amount in ``PaymentMethod``
   options
-  Allow setting processor specific fields for transactions and
   verifications

3.31.0
------

-  Fix ``UsBankAccount`` support for ``Customer``\ s
-  Added handling for unicode parameters. (Thanks @mgalgs)
-  Raise ``ConfigurationError`` for empty string credentials
-  Update ``Grant`` api to support options dictionary

3.30.0
------

-  Add 'UsBankAccount' payment method

3.29.2
------

-  Update links in docstrings
-  Remove Python 3.x-incompatible branch check
-  Remove references to SubMerchantAccount API

3.29.1
------

-  Improve error handling around server timeouts

3.29.0
------

-  Allow 'default\_payment\_method' option in Customer

3.28.0
------

-  Expose resource collection ids
-  Add order id to refund
-  Enable 3DS pass thru

3.27.0
------

-  Add method of revoking OAuth access tokens

3.26.1
------

-  Correct issue with setup.py

3.26.0
------

-  Add Transaction ``update_details``
-  Support for Too Many Requests response codes
-  Add SubMerchantAccount object with associate objects
-  Allow more parameters to be sent on SubMerchantAccount create
-  Add SubMerchantAccount update
-  Handle validation errors for SubMerchantAccount create / update

3.25.0
------

-  Add AccountUpdaterDailyReport webhook parsing

3.24.0
------

-  Add Verification#create
-  Add options to ``submit_for_settlement`` transaction flows
-  Update https certificate bundle
-  Support environment settings with strings

3.23.0
------

-  Add better defaults to client token generation when using an access
   token by consolidating client token defaults into ClientTokenGateway
-  Add PaymentMethodGateway#revoke

3.22.0
------

-  Add VenmoAccount
-  Add support for Set Transaction Context supplementary data.

3.21.0
------

-  Add transaction to subscription successfully charged webhook
-  Add new ProcessorDoesNotSupportAuths error
-  Add support for partial settlement transactions
-  Add constants for dispute kind
-  Preserve backtrace when not wrapping HTTP exceptions
-  Add date\_opened and date\_won to dispute webhooks
-  Add support for searching transactions from oauth app
-  Support AMEX express checkout

3.20.0
------

-  add source\_description to android pay and apple pay
-  add new android pay test nonces
-  add support for amex rewards transactions
-  add billing\_agreement\_id to paypalaccount

3.19.0
------

-  Add new test payment method nonces
-  Allow passing description on PayPal transactions

3.18.0
------

-  Fix oauth authentication
-  Fix python 3 syntax

3.17.0
------

-  Add oauth support

3.16.0
------

-  Add support for Android Pay

3.15.0
------

-  Validate webhook challenge payload

3.14.0
------

-  Add 3DS server side fields

3.13.0
------

-  Add attribute to customer
-  Add coinbase constant
-  Add European test nonce

3.12.0
------

-  Add support for new SEPA workflow

3.11.1
------

-  Fix test failures in Python 3.3+

3.11.0
------

-  Accept additional params in PaymentMethod.create()

3.10.0
------

-  Add 3D Secure transaction fields
-  Add ability to create nonce from vaulted payment methods

3.9.0
-----

-  Support Coinbase accounts
-  Surface Apple Pay payment instrument name in responses
-  Expose subscription status events
-  Support SEPA bank accounts for customer
-  Improve documentation

3.8.0
-----

-  Add error code constants
-  Allow PayPal parameters to be sent in options.paypal

3.7.0
-----

-  Add risk\_data to Transaction and Verification with Kount decision
   and id
-  Add verification\_amount an option when creating a credit card
-  Add TravelCruise industry type to Transaction
-  Add room\_rate to Lodging industry type
-  Add CreditCard#verification as the latest verification on that credit
   card
-  Add ApplePay support to all endpoints that may return ApplePayCard
   objects
-  Align WebhookTesting with other client libraries

3.6.0
-----

-  Allow descriptor to be passed in Funding Details options params for
   Merchant Account create and update.

3.5.0
-----

-  Add additional\_processor\_response to transaction

3.4.1
-----

-  Allow payee\_email to be passed in options params for Transaction
   create

3.4.0
-----

-  Added paypal specific fields to transaction calls
-  Added SettlementPending, SettlementDeclined transaction statuses

3.3.0
-----

-  Add Descriptor url support
-  Fix client token version type

3.2.0
-----

-  Support credit card options and billing address in
   PaymentMethod.create
-  Add PaymentMethod.update
-  Add associated subscriptions to PayPalAccount
-  Test refactoring and cleanup

3.1.1
-----

-  Add support for v.zero SDKs

3.0.0
-----

-  Drop Python 2.5 support
-  Remove use\_unsafe\_ssl option
-  Remove httplib strategy and pycurl strategy
-  Add Python 3.3+ support

2.29.1
------

-  Make webhook parsing more robust with newlines
-  Add messages to InvalidSignature exceptions

2.29.0
------

-  Include Dispute information on Transaction
-  Search for Transactions disputed on a certain date

2.28.0
------

-  Disbursement Webhooks

2.27.0
------

-  Fix using instantiated Configuration objects without first calling
   Configuration.configure
-  Accept billing\_address\_id on transaction create
-  Expose current\_billing\_cycle on addons and discounts

2.26.0
------

-  Merchant account find API

2.25.0
------

-  Merchant account update API
-  Merchant account create API v2

2.24.1
------

-  Update configuration URLs

2.24.0
------

-  Add partnership support
-  Add partner configuration

2.23.1
------

-  Add configuration option for custom HTTP strategies

2.23.0
------

-  Adds hold\_in\_escrow method
-  Add error codes for verification not supported error
-  Add company\_name and tax\_id to merchant account create
-  Adds cancel\_release methods
-  Adds release\_from\_escrow functionality
-  Adds owner\_phone to merchant account signature.
-  Adds merchant account phone error code.

2.22.0
------

-  Adds device data to transactions, customers, and credit cards.

2.21.0
------

-  Adds disbursement details to transactions.
-  Adds image\_url to transactions.

2.20.0
------

-  Support requests >= 1.0
-  Add new validation errors and rename old ones

2.19.0
------

-  Adds channel field to transactions.

2.18.0
------

-  Add additional card types for card type indicators

2.17.0
------

-  Adds verification search

2.16.0
------

-  Additional card information, such as prepaid, debit, commercial,
   Durbin regulated, healthcare, and payroll, are returned on credit
   card responses
-  Allows transactions to be specified as recurring

2.15.0
------

-  Adds prepaid attribute to credit cards (possible values of: Yes, No,
   Unknown)

2.14.2
------

-  Add settling transaction status to transaction search

2.14.1
------

-  Adds new package braintree.util.http\_stategy to setup.py

2.14.0
------

-  Removes relative imports for python 3.0 (thanks
   `MichaelBlume <https://github.com/MichaelBlume>`__)
-  Adds webhook gateways for parsing, verifying, and testing incoming
   notifications
-  Allow specifying the http strategy to use (PycURL, httplib, requests)

2.13.0
------

-  Adds search for duplicate credit cards given a payment method token
-  Adds flag to fail saving credit card to vault if card is duplicate

2.12.3
------

-  Exposes plan\_id on transactions

2.12.2
------

-  Added error code for invalid purchase order number
-  Fixed zip\_safe=False error when building (GitHub issue #17)

2.12.1
------

-  Added error message for merchant accounts that do not support refunds

2.12.0
------

-  Added ability to retrieve all Plans, AddOns, and Discounts
-  Added Transaction cloning

2.11.0
------

-  Added SettlementBatchSummary

2.10.1
------

-  Enabled gzip encoding for HTTP requests
-  Fixed handling of long integers when generating xml (thanks
   `glencoates <http://github.com/glencoates>`__)
-  Added new error code

2.10.0
------

-  Added subscription\_details to Transaction
-  Added flag to store in vault only when a transaction is successful
-  Added new error code

2.9.1
-----

-  Added improvements to unicode handling.

2.9.0
-----

-  Added a new transaction state, AuthorizationExpired.
-  Enabled searching by authorization\_expired\_at.

2.8.0
-----

-  Added next\_billing\_date and transaction\_id to subscription search
-  Added address\_country\_name to customer search
-  Added new error codes

2.7.0
-----

-  Added Customer search
-  Added dynamic descriptors to Subscriptions and Transactions
-  Added level 2 fields to Transactions:
-  tax\_amount
-  tax\_exempt
-  purchase\_order\_number

2.6.1
-----

-  Added billing\_address\_id to allowed parameters for credit cards
   create and update
-  Allow searching on subscriptions that are currently in a trial period
   using in\_trial\_period

2.6.0
-----

-  Added ability to perform multiple partial refunds on Transactions
-  Deprecated Transaction refund\_id in favor of refund\_ids
-  Added revert\_subscription\_on\_proration\_failure flag to
   Subscription update that specifies how a Subscription should react to
   a failed proration charge
-  Deprecated Subscription next\_bill\_amount in favor of
   next\_billing\_period\_amount
-  Added pycurl dependency in place of M2Crypto for better
   cross-platform compatibility
-  Added new fields to Subscription:
-  balance
-  paid\_through\_date
-  next\_billing\_period\_amount

2.5.0
-----

-  Added AddOns/Discounts
-  Enhanced Subscription search
-  Enhanced Transaction search
-  Added constants for CreditCardVerification statuses
-  Added Expired and Pending statuses to Subscription
-  Allowed prorate\_charges to be specified on Subscription update
-  Allowed argument lists and literal lists when searching for
   Subscriptions and Transactions
-  Added AddOn/Discount details to Transactions that were created from a
   Subscription
-  All Braintree exceptions now inherit from BraintreeError superclass
-  Removed 13 digit Visa Sandbox Credit Card number and replaced it with
   a 16 digit Visa
-  Made gateway operations threadsafe when using multiple configurations
-  Added new fields to Subscription:
-  billing\_day\_of\_month
-  days\_past\_due
-  first\_billing\_date
-  never\_expires
-  number\_of\_billing\_cycles

2.4.1
-----

-  Added support for M2Crypto version 0.20.1, which is the default for
   Ubuntu Lucid (thanks `foresto <http://github.com/foresto>`__)

2.4.0
-----

-  Added unified message to ErrorResult
-  Added ability to specify country using country\_name,
   country\_code\_alpha2, country\_code\_alpha3, or
   country\_code\_numeric (see
   `ISO\_3166-1 <http://en.wikipedia.org/wiki/ISO_3166-1>`__)
-  Renamed Subscription retryCharge to retry\_charge
-  Added gateway\_rejection\_reason to Transaction and Verification
-  Allow searching with date objects (in addition to datetime)
-  When creating a Subscription, return failed transaction on the
   ErrorResult if the initial transaction is not successful

2.3.0
-----

-  Added unified TransparentRedirect url and confirm methods and
   deprecated old methods
-  Added methods to CreditCard to allow searching on expiring and
   expired credit cards
-  Allow credit card verification against a specified merchant account
-  Added all method on Customer to retrieve all customers
-  Added ability to update a customer, credit card, and billing address
   in one request
-  Allow updating the payment method token on a subscription
-  Added methods to navigate between a Transaction and its refund (in
   both directions)

2.2.1
-----

-  Use isinstance instead of type to cater to inheritance (thanks
   `danielgtaylor <http://github.com/danielgtaylor>`__)

2.2.0
-----

-  Prevent race condition when pulling back collection results -- search
   results represent the state of the data at the time the query was run
-  Rename ResourceCollection's approximate\_size to maximum\_size
   because items that no longer match the query will not be returned in
   the result set
-  Correctly handle HTTP error 426 (Upgrade Required) -- the error code
   is returned when your client library version is no longer compatible
   with the gateway

2.1.0
-----

-  Added transaction advanced search
-  Added ability to partially refund transactions
-  Added ability to manually retry past-due subscriptions
-  Added new transaction error codes
-  Allow merchant account to be specified when creating transactions
-  Allow creating a transaction with a vault customer and new credit
   card
-  Allow existing billing address to be updated when updating credit
   card

2.0.0
-----

-  Updated is\_success on transaction results to return false on
   declined transactions
-  Search results now return a generator and will automatically paginate
   data
-  Allow passing cardholder\_name when creating transactions

1.2.0
-----

-  Renamed ValidationErrorCollection#all to deep\_errors and made it a
   property
-  Added the ability to make a credit card the default card for a
   customer
-  Updated Quick Start in README.md to show a workflow with error
   checking

1.1.0
-----

-  Added subscription search
-  Return associated subscriptions when finding credit cards
-  Raise down for maintenance error instead of forged query string error
   on 503 responses
-  Updated SSL CA file

1.0.0
-----

-  Initial release
