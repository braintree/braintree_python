try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="braintree",
    version="3.34.0",
    description="Braintree Python Library",
    long_description="""
    For more information see our `documentation <https://developers.braintreepayments.com/python/sdk/server/overview>`_
    or the `Github repo <https://github.com/braintree/braintree_python>`_.
    """,
    author="Braintree",
    author_email="support@braintreepayments.com",
    url="https://developers.braintreepayments.com/python/sdk/server/overview",
    packages=["braintree", "braintree.exceptions", "braintree.exceptions.http", "braintree.merchant_account", "braintree.util", "braintree.test"],
    package_data={"braintree": ["ssl/*"]},
    install_requires=["requests>=0.11.1,<3.0"],
    zip_safe=False,
    license="MIT",
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ]
)
