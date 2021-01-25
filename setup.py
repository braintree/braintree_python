try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

long_description = """
        The Braintree Python SDK provides integration access to the Braintree Gateway.

        1. https://github.com/braintree/braintree_python - README and Samples
        2. https://developers.braintreepayments.com/python/sdk/server/overview - API Reference
      """

setup(
    name="braintree",
    version="4.6.0",
    description="Braintree Python Library",
    long_description=long_description,
    author="Braintree",
    author_email="support@braintreepayments.com",
    url="https://developers.braintreepayments.com/python/sdk/server/overview",
    packages=["braintree", "braintree.dispute_details", "braintree.exceptions", "braintree.exceptions.http", "braintree.merchant_account", "braintree.util", "braintree.test"],
    package_data={"braintree": ["ssl/*"]},
    install_requires=["requests>=0.11.1,<3.0"],
    zip_safe=False,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ]
)
