import braintree
import unittest
import os
from braintree.test.nonces import Nonces
from tests.test_helper import *



class TestPayPalPaymentResourceIntegration(unittest.TestCase):

    def test_update_paypal_payment_resource(self):

        nonce = TestHelper.nonce_for_paypal_order_payment()
        request = {}

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

        result = PayPalPaymentResource.update(request)

        assert result.is_success
        new_nonce = result.payment_method_nonce
        assert new_nonce is not None
        assert new_nonce.nonce is not None

