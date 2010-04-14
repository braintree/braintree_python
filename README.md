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

    if result.is_success:
        if result.transaction.status == braintree.Transaction.Status.Authorized:
            print "success!: " + result.transaction.id
        else:
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
