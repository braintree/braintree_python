# Braintree Python Client Library

The Braintree library provides integration access to the Braintree Gateway.

## Dependencies

* [requests](http://docs.python-requests.org/en/latest/) or [PycURL](http://pycurl.sourceforge.net/)

_Note:_ Although discouraged, the dependency on PycURL / requests can be bypassed during development or for deployment on servers where they are impossible to use via:

    # Allow unsafe SSL, removes dependency on PycURL in dev environments
    braintree.Configuration.use_unsafe_ssl = True

## Documentation

 * [Official documentation](https://www.braintreepayments.com/docs/python)

## Quick Start Example

    import braintree

    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        "your_merchant_id",
        "your_public_key",
        "your_private_key"
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


## Open Source Attribution

A list of open source projects that help power Braintree can be found [here](https://www.braintreepayments.com/developers/open-source).

## License

See the LICENSE file.
