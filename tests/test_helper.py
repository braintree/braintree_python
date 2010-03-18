import unittest
import urllib
import httplib
from braintree.configuration import Configuration
from braintree.environment import Environment
from braintree.transparent_redirect import TransparentRedirect

Configuration.environment = Environment.DEVELOPMENT
Configuration.merchant_id = "integration_merchant_id"
Configuration.public_key = "integration_public_key"
Configuration.private_key = "integration_private_key"

class TestHelper(object):
    @staticmethod
    def create_via_tr(params, tr_data, url):
        params = TestHelper.flatten_dictionary(params)
        params["tr_data"] = TransparentRedirect.tr_data(tr_data, "http://example.com/path/to/something?foo=bar")
        form_data = urllib.urlencode(params)

        if Configuration.is_ssl():
            connection_type = httplib.HTTPSConnection
        else:
            connection_type = httplib.HTTPConnection

        conn = connection_type(Configuration.server_and_port())
        conn.request(
            "POST",
            url,
            form_data,
            TestHelper.__headers()
        )
        response = conn.getresponse()
        query_string = response.getheader('location').split("?", 1)[1]
        conn.close()
        return query_string

    @staticmethod
    def flatten_dictionary(params, parent=None):
        data = {}
        for key, val in params.iteritems():
            full_key = parent + "[" + key + "]" if parent else key
            if type(val) == dict:
                data.update(TestHelper.flatten_dictionary(val, full_key))
            else:
                data[full_key] = val
        return data

    @staticmethod
    def __headers():
        return {
            "Accept": "application/xml",
            "Content-type": "application/x-www-form-urlencoded",
        }

