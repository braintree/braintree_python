class Configuration(object):
    """
    A class representing the configuration of your Braintree account.
    You must call configure before any other Braintree operations. ::

        braintree.Configuration.configure(
            braintree.Environment.SANDBOX,
            "the_merchant_id",
            "the_public_key",
            "the_private_key"
        )

    By default, every request to the Braintree servers verifies the SSL connection
    using the `M2Crypto <http://chandlerproject.org/bin/view/Projects/MeTooCrypto>`_
    library.  This ensures valid encryption of data and prevents man-in-the-middle attacks.

    If you are in an environment where you absolutely cannot load `M2Crypto <http://chandlerproject.org/bin/view/Projects/MeTooCrypto>`_, you
    can turn off SSL Verification by setting::

        Configuration.use_unsafe_ssl = True

    This is highly discouraged, however, since it leaves you susceptible to
    man-in-the-middle attacks.

    If you are using Google App Engine, you must use unsafe ssl [1]_::

        The proxy the URL Fetch service uses cannot authenticate the host it
        is contacting. Because there is no certificate trust chain, the proxy
        accepts all certificates, including self-signed certificates. The
        proxy server cannot detect "man in the middle" attacks between App
        Engine and the remote host when using HTTPS.

.. [1] `URL Fetch Python API Overview <http://code.google.com/appengine/docs/python/urlfetch/overview.html>`_
    """
    @staticmethod
    def configure(environment, merchant_id, public_key, private_key):
        Configuration.environment = environment
        Configuration.merchant_id = merchant_id
        Configuration.public_key = public_key
        Configuration.private_key = private_key
        Configuration.use_unsafe_ssl = False

    @staticmethod
    def base_merchant_path():
        return "/merchants/" + Configuration.merchant_id

    @staticmethod
    def base_merchant_url():
        return Configuration.environment.protocol + Configuration.environment.server_and_port + Configuration.base_merchant_path()
