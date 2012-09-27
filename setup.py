import braintree
from distutils.core import setup
setup(
    name="braintree",
    version=braintree.version.Version,
    description="Braintree Python Library",
    author="Braintree",
    author_email="support@braintreepayments.com",
    url="https://www.braintreepayments.com/docs/python",
    packages=["braintree", "braintree.exceptions", "braintree.util", "braintree.test", "braintree.util.http_strategy"],
    package_data={"braintree": ["ssl/*"]},
    install_requires=["requests>=0.11.1,<1.0"],
    zip_safe=False
)
