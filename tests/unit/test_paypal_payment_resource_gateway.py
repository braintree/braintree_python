import unittest
from braintree.paypal_payment_resource_gateway import PayPalPaymentResourceGateway
from braintree.paypal_payment_resource import PayPalPaymentResource
from braintree.resource import Resource
from unittest.mock import patch, MagicMock
from decimal import Decimal
from braintree.util.xml_util import XmlUtil
class TestPayPalPaymentResourceGateway(unittest.TestCase):
    def setUp(self):
        self.gateway = MagicMock()
        self.gateway.config = MagicMock()
        self.gateway.config.base_merchant_path.return_value = "/merchant_path"
        self.gateway.config.http = MagicMock()

        self.paypal_payment_resource_gateway = PayPalPaymentResourceGateway(self.gateway)

    @patch.object(Resource, 'verify_keys')
    def test_update_calls_put_with_correct_params(self, mock_verify_keys):
        nonce = "123"
        line_item = {
            "description": "Shoes",
            "image_url": "https://example.com/products/23434/pic.png",
            "kind": "debit",
            "name": "Name #1",
            "product_code": "23434",
            "quantity": Decimal("1"),
            "total_amount": Decimal("45.00"),
            "unit_amount": Decimal("45.00"),
            "unit_tax_amount": Decimal("10.00"),
            "url": "https://example.com/products/23434"
        }


        request = {
            "paypal_payment_resource": {
                "amount": Decimal("55.00"),
                "amount_breakdown": {
                    "discount": Decimal("15.00"),
                    "handling": Decimal("0.00"),
                    "insurance": Decimal("5.00"),
                    "item_total": Decimal("45.00"),
                    "shipping": Decimal("10.00"),
                    "shipping_discount": Decimal("0.00"),
                    "tax_total": Decimal("10.00")
                },
                "currency_iso_code": "USD",
                "custom_field": "0437",
                "description": "This is a test",
                "line_items": [line_item],
                "order_id": "order-123456789",
                "payee_email": "bt_buyer_us@paypal.com",
                "payment_method_nonce": nonce,
                "shipping": {
                    "first_name": "John",
                    "last_name": "Doe",
                    "street_address": "123 Division Street",
                    "extended_address": "Apt. #1",
                    "locality": "Chicago",
                    "region": "IL",
                    "postal_code": "60618",
                    "country_name": "United States",
                    "country_code_alpha2": "US",
                    "country_code_alpha3": "USA",
                    "country_code_numeric": "484",
                    "international_phone": {
                        "country_code": "1",
                        "national_number": "4081111111"
                    }
                },
                "shipping_options": [{
                    "amount": Decimal("10.00"),
                    "id": "option1",
                    "label": "fast",
                    "selected": True,
                    "type": "SHIPPING"  
                }]
            }
        }
        try:
            self.paypal_payment_resource_gateway.update(request)
        except:
            pass

        self.gateway.config.http().put.assert_called_once_with(
            "/merchant_path/paypal/payment_resource",  
            request
        )
        mock_verify_keys.assert_called_once_with(request, PayPalPaymentResource.update_signature())

    def test_update_signature_returns_correct_signature(self):
        expected_signature = [ 
            {
                "paypal_payment_resource": [
                    "amount",
                    {
                        "amount_breakdown": [
                            "discount",
                            "handling",
                            "insurance",
                            "item_total",
                            "shipping",
                            "shipping_discount",
                            "tax_total"
                            ]
                    },
                    "currency_iso_code",
                    "custom_field",
                    "description",
                    {
                        "line_items": [
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
                    },
                    "order_id",
                    "payee_email",
                    "payment_method_nonce",
                    {
                        "shipping": [
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
                    },
                    {
                        "shipping_options": [
                            "amount",
                            "id",
                            "label",
                            "selected",
                            "type"
                        ]
                    }
                ]
            }
        ]

        self.assertEqual(PayPalPaymentResource.update_signature(), expected_signature)
