import httplib
import os
import random
import re
import unittest
import urllib
from braintree import *
from braintree.exceptions import *
from braintree.util import *
from datetime import date
from datetime import datetime
from decimal import Decimal
from M2Crypto import SSL
from nose.tools import raises

Configuration.configure(
    Environment.DEVELOPMENT,
    "integration_merchant_id",
    "integration_public_key",
    "integration_private_key"
)

class TestHelper(object):
    @staticmethod
    def simulate_tr_form_post(post_params, url):
        form_data = urllib.urlencode(post_params)
        conn = httplib.HTTPConnection(Configuration.environment.server_and_port)
        conn.request("POST", url, form_data, TestHelper.__headers())
        response = conn.getresponse()
        query_string = response.getheader("location").split("?", 1)[1]
        conn.close()
        return query_string

    @staticmethod
    def __headers():
        return {
            "Accept": "application/xml",
            "Content-type": "application/x-www-form-urlencoded",
        }

