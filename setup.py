import braintree
from distutils.core import setup
setup(
    name="braintree",
    version=braintree.version.Version,
    description="Braintree Python Library",
    author="Braintree",
    author_email="support@getbraintree.com",
    url="http://www.braintreepaymentsolutions.com/gateway/python",
    packages=["braintree", "braintree.exceptions", "braintree.util"],
    package_data={"braintree": ["ssl/*"]},
    install_requires=[],
    tests_require=["nose==0.11.3"]
)
