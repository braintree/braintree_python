import unittest
import urllib
import httplib
from braintree.configuration import Configuration
from braintree.environment import Environment
from braintree.transparent_redirect import TransparentRedirect

Configuration.configure(
    Environment.DEVELOPMENT,
    "integration_merchant_id",
    "integration_public_key",
    "integration_private_key"
)

class TestHelper(object):
    @staticmethod
    def create_via_tr(params, tr_data, url):
        params = TransparentRedirect.flatten_dictionary(params)
        params["tr_data"] = TransparentRedirect.tr_data(tr_data, "http://example.com/path/to/something?foo=bar")
        form_data = urllib.urlencode(params)

        if Configuration.environment.is_ssl:
            connection_type = httplib.HTTPSConnection
        else:
            connection_type = httplib.HTTPConnection

        conn = connection_type(Configuration.environment.server_and_port)
        conn.request("POST", url, form_data, TestHelper.__headers())
        response = conn.getresponse()
        query_string = response.getheader('location').split("?", 1)[1]
        conn.close()
        return query_string

    @staticmethod
    def __headers():
        return {
            "Accept": "application/xml",
            "Content-type": "application/x-www-form-urlencoded",
        }

