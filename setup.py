from distutils.core import setup
setup(
    name="braintree",
    version="3.3.0",
    description="Braintree Python Library",
    author="Braintree",
    author_email="support@braintreepayments.com",
    url="https://www.braintreepayments.com/docs/python",
    packages=["braintree", "braintree.exceptions", "braintree.exceptions.http", "braintree.merchant_account", "braintree.util", "braintree.test"],
    package_data={"braintree": ["ssl/*"]},
    install_requires=["requests>=0.11.1,<3.0"],
    zip_safe=False
)
