.. Braintree documentation master file, created by
   sphinx-quickstart on Mon Mar 29 14:46:55 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Braintree Python Client Library
=====================================

The Braintree library provides integration access to the Braintree Gateway.

Quick Start
-----------

::

    import braintree

    braintree.Configuration.configure(
        braintree.Environment.Sandbox,
        "the_merchant_id",
        "the_public_key",
        "the_private_key"
    )

    result = braintree.Transaction.sale({
        "amount": "100.00",
        "credit_card": {
            "number": "4111111111111111",
            "expiration_date": "05/2012"
        }
    })

    print result.transaction.id
    print result.transaction.status

Resources
---------

.. toctree::
   :maxdepth: 2

   address
   credit_card
   customer
   paged_collection
   subscription
   transaction

Validations
-----------

.. toctree::
   :maxdepth: 2

   error_codes
   error_result
   successful_result
   validation_error
   validation_error_collection

Configuration
-------------

.. toctree::
   :maxdepth: 2

   configuration
   environment

Exceptions
----------

.. toctree::
   :maxdepth: 2

   exceptions/authentication_error
   exceptions/authorization_error
   exceptions/down_for_maintenance_error
   exceptions/forged_query_string_error
   exceptions/not_found_error
   exceptions/server_error
   exceptions/unexpected_error

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
