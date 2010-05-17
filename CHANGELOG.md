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
