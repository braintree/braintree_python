import braintree
from braintree.resource import Resource
from braintree.configuration import Configuration

class PayPalPaymentResource(Resource):
    @staticmethod
    def update(request):
        return Configuration.gateway().paypal_payment_resource.update(request)

    @staticmethod
    def update_signature():
        amount_breakdown = [
            "discount",
            "handling",
            "insurance",
            "item_total",
            "shipping",
            "shipping_discount",
            "tax_total"
        ]
        
        line_item = [
            "commodity_code",
            "description",
            "discount_amount",
            "image_url",
            "kind",
            "name",
            "product_code",
            "quantity",
            "tax_amount",
            "total_amount",
            "unit_amount",
            "unit_of_measure", 
            "unit_tax_amount",
            "upc_code",
            "upc_type",
            "url",
        ]

        shipping_request = [
            "company",
            "country_name",
            "country_code_alpha2",
            "country_code_alpha3",
            "country_code_numeric",
            "extended_address",
            "first_name",
            {
                "international_phone": [
                    "country_code",
                    "national_number"
                ]
            },
            "last_name",
            "locality",
            "postal_code",
            "region",
            "street_address"
        ]

        shipping_option = [
            "amount",
            "id",
            "label",
            "selected",
            "type"
        ]

        signature = [
            {
                "paypal_payment_resource": [
                    "amount",
                    { 
                        "amount_breakdown": amount_breakdown
                    },
                    "currency_iso_code",
                    "custom_field",
                    "description",
                    {
                        "line_items": line_item
                    },
                    "order_id",
                    "payee_email",
                    "payment_method_nonce",
                    {
                        "shipping": shipping_request
                    },
                    {
                        "shipping_options": shipping_option
                    }
                ]
            }
        ]
        return signature

    def __init__(self, gateway, attributes):
        Resource.__init__(self, gateway, attributes)