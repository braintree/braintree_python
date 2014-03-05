from __future__ import with_statement
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('braintree/version.py') as f:
    exec(f.read())

setup(
    name="braintree",
    version=__version__,
    description="Braintree Python Library",
    author="Braintree",
    author_email="support@braintreepayments.com",
    url="https://www.braintreepayments.com/docs/python",
    packages=["braintree", "braintree.exceptions", "braintree.merchant_account", "braintree.util", "braintree.test", "braintree.util.http_strategy"],
    package_data={"braintree": ["ssl/*"]},
    install_requires=["requests>=0.11.1,<3.0"],
    zip_safe=False
)
