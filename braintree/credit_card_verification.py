from braintree.attribute_getter import AttributeGetter

class CreditCardVerification(AttributeGetter):

    class Status(object):
        """
        Constants representing transaction statuses. Available statuses are:

        * braintree.CreditCardVerification.Status.Failed
        * braintree.CreditCardVerification.Status.GatewayRejected
        * braintree.CreditCardVerification.Status.ProcessorDeclined
        * braintree.CreditCardVerification.Status.Unrecognized
        * braintree.CreditCardVerification.Status.Verified
        """

        Failed                 = "failed"
        GatewayRejected        = "gateway_rejected"
        ProcessorDeclined      = "processor_declined"
        Unrecognized           = "unrecognized"
        Verified               = "verified"

    def __init__(self, gateway, attributes):
        AttributeGetter.__init__(self, attributes)
        if "processor_response_code" not in attributes:
            self.processor_response_code = None
        if "processor_response_text" not in attributes:
            self.processor_response_text = None
