import traceback

from tests.test_helper import *
from braintree.exceptions.http.timeout_error import *
from braintree.attribute_getter import AttributeGetter
from unittest.mock import patch

class TestHttp(unittest.TestCase):
    def test_raise_exception_from_request_timeout(self):
        with self.assertRaises(RequestTimeoutError):
            Http.raise_exception_from_status(408)

    def test_raise_exception_from_status_for_upgrade_required(self):
        with self.assertRaises(UpgradeRequiredError):
            Http.raise_exception_from_status(426)

    def test_raise_exception_from_too_many_requests(self):
        with self.assertRaises(TooManyRequestsError):
            Http.raise_exception_from_status(429)

    def test_raise_exception_from_service_unavailable(self):
        with self.assertRaises(ServiceUnavailableError):
            Http.raise_exception_from_status(503)

    def test_raise_exception_from_gateway_timeout(self):
        with self.assertRaises(GatewayTimeoutError):
            Http.raise_exception_from_status(504)

    def test_header_includes_gzip_accept_encoding(self):
        config = AttributeGetter({
                "base_url": (lambda: ""),
                "has_access_token": (lambda: False),
                "has_client_credentials": (lambda: False),
                "public_key": "",
                "private_key": ""})
        headers = Http(config, "fake_environment")._Http__headers(Http.ContentType.Xml)
        self.assertTrue('Accept-Encoding' in headers)
        self.assertEqual('gzip', headers["Accept-Encoding"])

    def test_backtrace_preserved_when_not_wrapping_exceptions(self):
        class Error(Exception):
            pass
        def raise_error(*_):
            raise Error
        http_strategy = AttributeGetter({"http_do": raise_error})
        config = AttributeGetter({
                "base_url": (lambda: ""),
                "has_access_token": (lambda: False),
                "has_client_credentials": (lambda: False),
                "http_strategy": (lambda: http_strategy),
                "public_key": "",
                "private_key": "",
                "wrap_http_exceptions": False})

        try:
            Http(config, "fake_environment").post("/example/path/to/reach")
        except Error:
            _, _, tb = sys.exc_info()
            self.assertEqual('raise_error', traceback.extract_tb(tb)[-1][2])

    def test_request_body_returns_string_for_post(self):
        def test_http_do_strategy(http_verb, path, headers, request_body):
            self.assertTrue(isinstance(request_body, str))
            self.assertEqual("<method>post</method>", request_body)
            return (200, "")

        http = self.setup_http_strategy(test_http_do_strategy)
        http.post("/some_path", {"method": "post"})

    def test_request_body_returns_string_for_delete(self):
        def test_http_do_strategy(http_verb, path, headers, request_body):
            self.assertTrue(isinstance(request_body, str))
            return (200, "")

        http = self.setup_http_strategy(test_http_do_strategy)
        http.delete("/some_path")

    def test_request_body_returns_string_for_get(self):
        def test_http_do_strategy(http_verb, path, headers, request_body):
            self.assertTrue(isinstance(request_body, str))
            return (200, "")

        http = self.setup_http_strategy(test_http_do_strategy)
        http.get("/some_path")

    def test_request_body_returns_string_for_put(self):
        def test_http_do_strategy(http_verb, path, headers, request_body):
            self.assertTrue(isinstance(request_body, str))
            self.assertEqual("<method>put</method>", request_body)
            return (200, "")

        http = self.setup_http_strategy(test_http_do_strategy)
        http.put("/some_path", {"method": "put"})

    def test_request_body_returns_string_for_post_multipart_when_no_files(self):
        params = {"method": "post_multipart"}
        def test_http_do_strategy(http_verb, path, headers, request_body):
            self.assertEqual(params, request_body)
            return (200, "")

        http = self.setup_http_strategy(test_http_do_strategy)
        http.post_multipart("/some_path", None, params)

    def test_request_body_returns_tuple_for_post_multipart_when_files(self):
        params = {"method": "post_multipart"}
        def test_http_do_strategy(http_verb, path, headers, request_body):
            self.assertEqual(params, request_body[0])
            self.assertEqual("files", request_body[1])
            return (200, "")

        http = self.setup_http_strategy(test_http_do_strategy)
        http.post_multipart("/some_path", "files", params)

    def setup_http_strategy(self, http_do):
        config = AttributeGetter({
                "base_url": (lambda: ""),
                "has_access_token": (lambda: False),
                "has_client_credentials": (lambda: False),
                "http_strategy": (lambda: AttributeGetter({"http_do": http_do})),
                "public_key": "",
                "private_key": "",
                "wrap_http_exceptions": False})

        return Http(config, "fake_environment")

    def test_raise_read_timeout_error(self):
        def test_http_do_strategy(http_verb, path, headers, request_body):
            return (200, "")

        with self.assertRaises(ReadTimeoutError):
            http = self.setup_http_strategy(test_http_do_strategy)
            http.handle_exception(requests.exceptions.ReadTimeout())

    def test_raise_connect_timeout_error(self):
        def test_http_do_strategy(http_verb, path, headers, request_body):
            return (200, "")

        with self.assertRaises(ConnectTimeoutError):
            http = self.setup_http_strategy(test_http_do_strategy)
            http.handle_exception(requests.exceptions.ConnectTimeout())

    def test_request_urls_retain_dots(self):
        with patch('requests.Session.send') as send:
            send.return_value.status_code = 200
            config = Configuration(
                Environment.Development,
                "integration_merchant_id",
                public_key="integration_public_key",
                private_key="integration_private_key",
                wrap_http_exceptions=True
            )
            http = config.http()
            http.get("/../../customers/")

            prepared_request = send.call_args[0][0]
            request_url = prepared_request.url
            self.assertTrue(request_url.endswith("/../../customers/"))

    def test_sessions_close_after_request(self):
        with patch('requests.Session.send') as send, patch('requests.Session.close') as close:
            send.return_value.status_code = 200
            config = Configuration(
                Environment.Development,
                "integration_merchant_id",
                public_key="integration_public_key",
                private_key="integration_private_key",
                wrap_http_exceptions=True
            )
            http = config.http()
            http.get("/../../customers/")

            self.assertTrue(close.called)
