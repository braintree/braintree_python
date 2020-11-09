# Braintree Python library

The Braintree Python library provides integration access to the Braintree Gateway.

## TLS 1.2 required
> **The Payment Card Industry (PCI) Council has [mandated](https://blog.pcisecuritystandards.org/migrating-from-ssl-and-early-tls) that early versions of TLS be retired from service.  All organizations that handle credit card information are required to comply with this standard. As part of this obligation, Braintree has updated its services to require TLS 1.2 for all HTTPS connections. Braintrees require HTTP/1.1 for all connections. Please see our [technical documentation](https://github.com/paypal/tls-update) for more information.**

## Dependencies

* [requests](http://docs.python-requests.org/en/latest/)

The Braintree Python SDK is tested against Python versions 3.5.3 and 3.8.0.

_The Python core development community has released [End-of-Life branches](https://devguide.python.org/devcycle/#end-of-life-branches) for Python versions 2.7 - 3.4, and are no longer receiving [security updates](https://devguide.python.org/#branchstatus). As a result, Braintree no longer supports these versions of Python._

## Versions

Braintree employs a deprecation policy for our SDKs. For more information on the statuses of an SDK check our [developer docs](http://developers.braintreepayments.com/reference/general/server-sdk-deprecation-policy).

| Major version number | Status | Released | Deprecated | Unsupported |
| -------------------- | ------ | -------- | ---------- | ----------- |
| 4.x.x | Active | March 2020 | TBA | TBA |
| 3.x.x | Inactive | June 2014 | March 2022 | March 2023 |

## Documentation

 * [Official documentation](https://developers.braintreepayments.com/ios+python/start/hello-server)

Updating from an Inactive, Deprecated, or Unsupported version of this SDK? Check our [Migration Guide](https://developers.braintreepayments.com/reference/general/server-sdk-migration-guide/python) for tips.

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
   pip3 install -r dev_requirements.txt
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
