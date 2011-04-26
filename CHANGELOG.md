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

* Added support for M2Crypto version 0.20.1, which is the default for Ubuntu Lucid (thanks [foresto](http://github.com/foresto))

## 2.4.0

* Added unified message to ErrorResult
* Added ability to specify country using country_name, country_code_alpha2, country_code_alpha3, or country_code_numeric (see [ISO_3166-1](http://en.wikipedia.org/wiki/ISO_3166-1))
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

* Use isinstance instead of type to cater to inheritance (thanks [danielgtaylor](http://github.com/danielgtaylor))

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
