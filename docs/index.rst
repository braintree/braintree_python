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
   transaction

Validations
-----------

.. toctree::
   :maxdepth: 2

   error_codes
   error_result

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

   not_found_error

Indices
-------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
