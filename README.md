# Braintree Python Client Library

The Braintree library provides integration access to the Braintree Gateway.

## Dependencies

* [M2Crypto](http://chandlerproject.org/bin/view/Projects/MeTooCrypto)

## Quick Start Example

    import braintree

    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        "the_merchant_id",
        "the_public_key",
        "the_private_key"
        )

    result = braintree.Transaction.sale({
        "amount": "100.00",
        "credit_card": {
            "number": "4111111111111111",
            "expiration_date": "05/2012"
            }
        })

    print result.transaction.id
    print result.transaction.status

## License

See the LICENSE file.
