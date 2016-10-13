from setuptools import setup

with open('README.rst', 'r') as fp:
    long_description = fp.read()

setup(
    name="braintree",
    version="3.29.2",
    description="Braintree Python Library",
    long_description=long_description,
    author="Braintree",
    author_email="support@braintreepayments.com",
    url="https://developers.braintreepayments.com/python/sdk/server/overview",
    packages=[
        "braintree",
        "braintree.exceptions",
        "braintree.exceptions.http",
        "braintree.merchant_account",
        "braintree.util",
        "braintree.test"
    ],
    package_data={"braintree": ["ssl/*"]},
    install_requires=["requests>=0.11.1,<3.0"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ]
)
