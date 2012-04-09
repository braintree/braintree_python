import httplib
import braintree

class PycurlStrategy(object):
    def __init__(self, config, environment):
        self.config = config
        self.environment = environment

    def http_do(self, http_verb, path, headers, request_body):
        if self.environment.is_ssl:
            self.__verify_ssl()
            conn = httplib.HTTPSConnection(self.environment.server, self.environment.port)
        else:
            conn = httplib.HTTPConnection(self.environment.server, self.environment.port)

        conn.request(http_verb, path, request_body, headers)
        response = conn.getresponse()
        status = response.status
        response_body = response.read()
        conn.close()
        return [status, response_body]

    def __verify_ssl(self):
        if braintree.configuration.Configuration.use_unsafe_ssl: return

        try:
            import pycurl
        except ImportError, e:
            print "Cannot load PycURL.  Please refer to Braintree documentation."
            print """
If you are in an environment where you absolutely cannot load PycURL
(such as Google App Engine), you can turn off SSL Verification by setting:

    Configuration.use_unsafe_ssl = True

This is highly discouraged, however, since it leaves you susceptible to
man-in-the-middle attacks."""
            raise e

        curl = pycurl.Curl()
        # see http://curl.haxx.se/libcurl/c/curl_easy_setopt.html for info on these options
        curl.setopt(pycurl.CAINFO, self.environment.ssl_certificate)
        curl.setopt(pycurl.ENCODING, 'gzip')
        curl.setopt(pycurl.SSL_VERIFYPEER, 1)
        curl.setopt(pycurl.SSL_VERIFYHOST, 2)
        curl.setopt(pycurl.NOBODY, 1)
        curl.setopt(pycurl.NOSIGNAL, 1)
        curl.setopt(pycurl.URL, self.environment.protocol + self.environment.server_and_port)
        curl.perform()
