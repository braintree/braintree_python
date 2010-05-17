# Braintree Python Client Library

The Braintree library provides integration access to the Braintree Gateway.

## Dependencies

* [M2Crypto](http://chandlerproject.org/bin/view/Projects/MeTooCrypto)

_Note:_ Although discouraged, the dependency on M2Crypto can be bypassed during development or for deployment on servers where it is impossible to use via:

    # Allow unsafe SSL, removes dependency on M2Crypto in dev environments
    braintree.Configuration.use_unsafe_ssl = True

## Documentation

Full module documentation generated from the docs directory above can be found here:

 * [Official documentation](http://www.braintreepaymentsolutions.com/gateway/python/docs/index.html)

## Quick Start Example

    import braintree

    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        "the_merchant_id",
        "the_public_key",
        "the_private_key"
    )

    result = braintree.Transaction.sale({
        "amount": "1000.00",
        "credit_card": {
            "number": "4111111111111111",
            "expiration_date": "05/2012"
        }
    })

    if result.is_success:
        print "success!: " + result.transaction.id
    elif result.transaction:
        print "Error processing transaction:"
        print "  code: " + result.transaction.processor_response_code
        print "  text: " + result.transaction.processor_response_text
    else:
        for error in result.errors.deep_errors:
            print "attribute: " + error.attribute
            print "  code: " + error.code
            print "  message: " + error.message

## License

See the LICENSE file.
