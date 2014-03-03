import re
from setuptools import setup, dist
VERSIONFILE="braintree/version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    name="braintree",
    version=verstr,
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
        "six>=1.5.2",
    ],
    zip_safe=False
)
