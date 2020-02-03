# Braintree Python library

The Braintree Python library provides integration access to the Braintree Gateway.

## Please Note
> **The Payment Card Industry (PCI) Council has [mandated](https://blog.pcisecuritystandards.org/migrating-from-ssl-and-early-tls) that early versions of TLS be retired from service.  All organizations that handle credit card information are required to comply with this standard. As part of this obligation, Braintree is updating its services to require TLS 1.2 for all HTTPS connections. Braintree will also require HTTP/1.1 for all connections. Please see our [technical documentation](https://github.com/paypal/tls-update) for more information.**

## Dependencies

* [requests](http://docs.python-requests.org/en/latest/)

The Braintree Python SDK is tested against Python versions 2.7.9, 3.3.5 and 3.8.0.

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

```python
import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox
        merchant_id="your_merchant_id",
        public_key="your_public_key",
        private_key="your_private_key",
    )
)

result = gateway.transaction.sale({
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
```

## Developing

1. Create a [virtualenv](https://virtualenv.pypa.io/) called `venv`:

   ```
   virtualenv venv
   ```

2. Start the virtualenv:

   ```
   source venv/bin/activate
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

## Developing (Docker)

The `Makefile` and `Dockerfile` will build an image containing the dependencies and drop you to a terminal where you can run tests.

```
make
```

## Testing

Our friends at [Venmo](https://venmo.com) have [an open source library](https://github.com/venmo/btnamespace) designed to simplify testing of applications using this library.

If you wish to run the tests, make sure you are set up for development (see instructions above). The unit specs can be run by anyone on any system, but the integration specs are meant to be run against a local development server of our gateway code. These integration specs are not meant for public consumption and will likely fail if run on your system. To run unit tests use rake (`rake test:unit`) or nose (`nosetests tests/unit`).

## License

See the [LICENSE](LICENSE) file for more info.
