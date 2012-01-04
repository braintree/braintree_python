import braintree
from distutils.core import setup
setup(
    name="braintree",
    version=braintree.version.Version,
    description="Braintree Python Library",
    author="Braintree",
    author_email="support@getbraintree.com",
    url="http://www.braintreepayments.com/docs/python",
    packages=["braintree", "braintree.exceptions", "braintree.util"],
    package_data={"braintree": ["ssl/*"]},
    install_requires=["pycurl==7.19.0"],
    tests_require=["pycurl==7.19.0", "nose==0.11.3"],
    zip_safe=False
)
