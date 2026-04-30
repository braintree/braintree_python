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

    def test_sessions_reused_across_requests_within_idle_timeout(self):
        with patch('requests.Session') as MockSession, \
             patch('braintree.util.http.time.monotonic', side_effect=[0.0, 30.0]):
            MockSession.return_value.send.return_value.status_code = 200
            MockSession.return_value.send.return_value.text = ""
            config = Configuration(
                Environment.Development,
                "integration_merchant_id",
                public_key="integration_public_key",
                private_key="integration_private_key",
                wrap_http_exceptions=True
            )
            http = config.http()

            http.get("/../../customers/")
            http.get("/../../transactions/")

            self.assertEqual(MockSession.call_count, 1)

    def test_session_recreated_after_idle_timeout(self):
        with patch('requests.Session') as MockSession, \
             patch('braintree.util.http.time.monotonic', side_effect=[0.0, 61.0]):
            MockSession.return_value.send.return_value.status_code = 200
            MockSession.return_value.send.return_value.text = ""
            config = Configuration(
                Environment.Development,
                "integration_merchant_id",
                public_key="integration_public_key",
                private_key="integration_private_key",
                wrap_http_exceptions=True
            )
            http = config.http()

            http.get("/../../customers/")
            http.get("/../../transactions/")

            self.assertEqual(MockSession.call_count, 2)

    def test_max_connection_idle_seconds_is_configurable(self):
        with patch('requests.Session') as MockSession, \
             patch('braintree.util.http.time.monotonic', side_effect=[0.0, 11.0]):
            MockSession.return_value.send.return_value.status_code = 200
            MockSession.return_value.send.return_value.text = ""
            config = Configuration(
                Environment.Development,
                "integration_merchant_id",
                public_key="integration_public_key",
                private_key="integration_private_key",
                wrap_http_exceptions=True,
                max_connection_idle_seconds=10
            )
            http = config.http()

            http.get("/../../customers/")
            http.get("/../../transactions/")

            self.assertEqual(MockSession.call_count, 2)

    def test_sessions_are_thread_local(self):
        import threading

        with patch('requests.Session.send') as send:
            send.return_value.status_code = 200
            send.return_value.text = ""
            config = Configuration(
                Environment.Development,
                "integration_merchant_id",
                public_key="integration_public_key",
                private_key="integration_private_key",
                wrap_http_exceptions=True
            )
            http = config.http()

            sessions = {}

            def make_request(thread_id):
                http.get("/../../customers/")
                sessions[thread_id] = http._get_session()

            threads = []
            for i in range(3):
                t = threading.Thread(target=make_request, args=(i,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

            self.assertEqual(len(sessions), 3)
            session_ids = [id(s) for s in sessions.values()]
            self.assertEqual(len(session_ids), len(set(session_ids)))

    def test_close_method_closes_session(self):
        with patch('requests.Session.send') as send:
            send.return_value.status_code = 200
            send.return_value.text = ""
            config = Configuration(
                Environment.Development,
                "integration_merchant_id",
                public_key="integration_public_key",
                private_key="integration_private_key",
                wrap_http_exceptions=True
            )
            http = config.http()

            http.get("/../../customers/")
            session = http._get_session()
            self.assertIsNotNone(session)

            with patch.object(session, 'close') as close:
                http.close()
                self.assertTrue(close.called)

            self.assertFalse(hasattr(http._thread_local, 'session'))

            http.get("/../../transactions/")
            new_session = http._get_session()
            self.assertIsNotNone(new_session)
            self.assertIsNot(session, new_session)
