from distutils.core import setup
setup(
    name="braintree-python",
    version="1.0.0",
    description="Braintree Python Library",
    author="Braintree",
    author_email="support@getbraintree.com",
    url="http://www.braintreepaymentsolutions.com/gateway/python",
    packages=["braintree", "braintree.exceptions", "braintree.util"],
    package_data={"braintree": ["ssl/*"]},
    requires=["M2Crypto"]
)
