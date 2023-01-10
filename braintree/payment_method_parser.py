import braintree
from braintree.apple_pay_card import ApplePayCard
from braintree.credit_card import CreditCard
from braintree.payment_method import PaymentMethod
from braintree.paypal_account import PayPalAccount
from braintree.europe_bank_account import EuropeBankAccount
from braintree.android_pay_card import AndroidPayCard
from braintree.amex_express_checkout_card import AmexExpressCheckoutCard
from braintree.venmo_account import VenmoAccount
from braintree.us_bank_account import UsBankAccount
from braintree.visa_checkout_card import VisaCheckoutCard
from braintree.masterpass_card import MasterpassCard
from braintree.sepa_direct_debit_account import SepaDirectDebitAccount
from braintree.samsung_pay_card import SamsungPayCard
from braintree.unknown_payment_method import UnknownPaymentMethod

def parse_payment_method(gateway, attributes):
    if "paypal_account" in attributes:
        return PayPalAccount(gateway, attributes["paypal_account"])
    elif "credit_card" in attributes:
        return CreditCard(gateway, attributes["credit_card"])
    elif "europe_bank_account" in attributes:
        return EuropeBankAccount(gateway, attributes["europe_bank_account"])
    elif "apple_pay_card" in attributes:
        return ApplePayCard(gateway, attributes["apple_pay_card"])
    elif "android_pay_card" in attributes:
        return AndroidPayCard(gateway, attributes["android_pay_card"])
    # NEXT_MAJOR_VERSION remove amex express checkout
    elif "amex_express_checkout_card" in attributes:
        return AmexExpressCheckoutCard(gateway, attributes["amex_express_checkout_card"])
    elif "sepa_debit_account" in attributes:
        return SepaDirectDebitAccount(gateway, attributes["sepa_debit_account"])
    elif "venmo_account" in attributes:
        return VenmoAccount(gateway, attributes["venmo_account"])
    elif "us_bank_account" in attributes:
        return UsBankAccount(gateway, attributes["us_bank_account"])
    elif "visa_checkout_card" in attributes:
        return VisaCheckoutCard(gateway, attributes["visa_checkout_card"])
    # NEXT_MAJOR_VERSION remove masterpass
    elif "masterpass_card" in attributes:
        return MasterpassCard(gateway, attributes["masterpass_card"])
    elif "samsung_pay_card" in attributes:
        return SamsungPayCard(gateway, attributes["samsung_pay_card"])
    else:
        name = list(attributes)[0]
        return UnknownPaymentMethod(gateway, attributes[name])
