
# Braintree Python Library

The Braintree Python library provides integration access to the Braintree Gateway.

## TLS 1.2 Required

> **The Payment Card Industry (PCI) Council has [mandated](https://blog.pcisecuritystandards.org/migrating-from-ssl-and-early-tls) that early versions of TLS be retired from service.  
> All organizations that handle credit card information are required to comply with this standard. As part of this obligation, Braintree has updated its services to require TLS 1.2 for all HTTPS connections.  
> Braintree requires HTTP/1.1 for all connections. Please see our [technical documentation](https://github.com/paypal/tls-update) for more information.**

## Prerequisites

Make sure you have the following prerequisites installed before proceeding:

- Python 3.5.3 or higher (tested up to 3.12.0)
- [requests](http://docs.python-requests.org/en/latest/)

_Note: Python versions 2.7 - 3.4 have reached their [End-of-Life](https://devguide.python.org/devcycle/#end-of-life-branches) and are no longer supported._

## Installation Steps

### Option 1: Manual Installation

To manually install the Braintree Python SDK, download the repository and follow the instructions in the [Documentation](https://developer.paypal.com/braintree/docs/start/hello-server/python).

### Option 2: Using Package Manager

Install via pip:

```bash
pip install braintree
```

### Verification

To verify the successful installation, create a simple script to check the version:

```python
import braintree
print(braintree.__version__)
```

## Version History

Braintree employs a deprecation policy for our SDKs. For more information, check our [developer docs](https://developer.paypal.com/braintree/docs/reference/general/server-sdk-deprecation-policy).

| Major Version Number | Status    | Released    | Deprecated | Unsupported |
|-----------------------|-----------|-------------|------------|-------------|
| 4.x.x                | Active    | March 2020  | TBA        | TBA         |
| 3.x.x                | Inactive  | June 2014   | March 2022 | March 2023  |

## Quick Start Example

```python
import braintree

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        environment=braintree.Environment.Sandbox,
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

## External Documentation
- For additional information, please visit [Official documentation](https://developer.paypal.com/braintree/docs/start/hello-server/python)
- Updating from an Inactive, Deprecated, or Unsupported version of this SDK? Check our [Migration Guide](https://developer.paypal.com/braintree/docs/reference/general/server-sdk-migration-guide/python) for tips.

## Developing

1. Create a virtual environment called `venv`:

   ```bash
   virtualenv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip3 install -r dev_requirements.txt
   ```

## Developing (Docker)

Use the `Makefile` and `Dockerfile` to build an image containing dependencies and drop into a terminal where you can run tests.

```bash
make
```

## Testing

The unit tests can be run on any system. Use the following commands:

- Run unit tests:

   ```bash
   rake test:unit
   ```

- Alternatively, use Python's unittest:

   ```bash
   python3 -m unittest discover tests/unit
   ```

Integration tests require a local development server of the gateway code and are not meant for public use.

## License

See the [LICENSE](LICENSE) file for more information.
