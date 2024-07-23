from braintree.attribute_getter import AttributeGetter
from warnings import warn

class PackageDetails(AttributeGetter):
    """
    A class representing the package tracking information of a transaction.

    An example of package details including all available fields::

        result = braintree.PackageDetails.create({
            "id": "my_id",
            "carrier": "a_carrier",
            "tracking_number": "my_tracking_number",
            "paypal_tracking_id": "my_paypal_tracking_id",
            "paypal_tracker_id": "my_paypal_tracker_id",
        })

    """
    detail_list = [
        "id",
        "carrier",
        "tracking_number",
        # NEXT_MAJOR_VERSION remove paypal_tracking_id
        "paypal_tracking_id",
        "paypal_tracker_id",
    ]

    def __init__(self, attributes):
        AttributeGetter.__init__(self, attributes)
