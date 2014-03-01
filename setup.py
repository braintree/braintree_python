import braintree
from setuptools import setup
setup(
    name="braintree",
    version=braintree.version.Version,
    description="Braintree Python Library",
    author="Braintree",
    author_email="support@braintreepayments.com",
    url="https://www.braintreepayments.com/docs/python",
    packages=[
        "braintree",
        "braintree.exceptions",
        "braintree.merchant_account",
        "braintree.util",
        "braintree.test"],
    package_data={"braintree": ["ssl/*"]},
    install_requires=[
        "requests>=0.11.1,<3.0",
        "six",
    ],
    zip_safe=False
)
