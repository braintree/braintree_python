from tests.test_helper import *

class TestHttp(unittest.TestCase):
    def test_successful_connection_to_good_ssl_server(self):
        http = Http("qa-master.braintreegateway.com:443", True, "braintree/ssl/valicert_ca.crt")
        http.get("/customers")

    def test_bad_ssl_certificate_raises_error(self):
        try:
            self.__start_ssl_server()
            http = Http("localhost:7443", True, "braintree/ssl/valicert_ca.crt")
            http.get("/")
            self.assertTrue(False)
        except ssl.SSLError as e:
            self.assertTrue(re.search("certificate verify failed", e.strerror))
        finally:
            self.__stop_ssl_server()

    def __start_ssl_server(self):
        subprocess.Popen(["tests/script/httpsd.rb", "/tmp/python_httpsd.pid"]).wait()

    def __stop_ssl_server(self):
        pid = open('/tmp/python_httpsd.pid').read()
        os.kill(int(pid), signal.SIGINT)
