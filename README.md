# Braintree Python Client Library

The Braintree library provides integration access to the Braintree Gateway.

## Dependencies

* Python 2.6, 2.7, 3.3, 3.4, or 3.5
* [requests](http://docs.python-requests.org/en/latest/)

## Upgrading from 2.x.x to 3.x.x

On Python 2.6 or 2.7 with default settings / requests:

No changes are required to upgrade to version 3.

On Python 2.6 or 2.7 with pycurl, httplib, or use_unsafe_ssl = True:

Install requests and test that you are able to connect to the Sandbox
environment with version 3 and without specifying an HTTP strategy.
The use_unsafe_ssl parameter will be ignored.

On Python 2.5:

Python 2.5 isn't supported by version 3 of the library.
Most code that runs on 2.5 will work unmodified on Python 2.6.
After making sure your code works on Python 2.6, follow the
instructions above for upgrading from pycurl / httplib to requests.

## Documentation

 * [Official documentation](https://developers.braintreepayments.com/ios+python/start/hello-server)

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
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement": True
        }
    })

    if result.is_success:
        print("success!: " + result.transaction.id)
    elif result.transaction:
        print("Error processing transaction:")
        print("  code: " + result.transaction.processor_response_code)
        print("  text: " + result.transaction.processor_response_text)
    else:
        for error in result.errors.deep_errors:
            print("attribute: " + error.attribute)
            print("  code: " + error.code)
            print("  message: " + error.message)

## Testing

Our friends at [Venmo](https://venmo.com) have [an open source library](https://github.com/venmo/btnamespace) designed to simplify testing of applications using this library.

The unit specs can be run by anyone on any system, but the integration specs are meant to be run against a local development server of our gateway code. These integration specs are not meant for public consumption and will likely fail if run on your system. To run unit tests use rake(`rake test:unit`) or nose(`nosetests tests/unit`).

## Open Source Attribution

A list of open source projects that help power Braintree can be found [here](https://www.braintreepayments.com/developers/open-source).

## License

See the LICENSE file.
