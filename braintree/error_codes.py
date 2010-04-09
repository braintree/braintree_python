class ErrorCodes(object):
    """
    A set of constants representing validation errors.  Validation error messages can change, but the codes will not.
    See the source for a list of all errors codes.

    Codes can be used to check for specific validation errors::

        result = Transaction.sale({})
        assert(result.is_success == False)
        assert(result.errors.for_object("transaction").on("amount")[0].code == ErrorCodes.Transaction.AmountIsRequired)
    """

    class Address(object):
        CannotBeBlank = "81801"
        CompanyIsTooLong = "81802"
        CountryNameIsNotAccepted = "91803"
        ExtedAddressIsTooLong = "81804"
        FirstNameIsTooLong = "81805"
        LastNameIsTooLong = "81806"
        LocalityIsTooLong = "81807"
        PostalCodeIsRequired = "81808"
        PostalCodeIsTooLong = "81809"
        RegionIsTooLong = "81810"
        StreetAddressIsRequired = "81811"
        StreetAddressIsTooLong = "81812"

    class CreditCard(object):
        BillingAddressConflict = "91701"
        BillingAddressIdIsInvalid = "91702"
        CardholderNameIsTooLong = "81723"
        CreditCardTypeIsNotAccepted = "81703"
        CustomerIdIsRequired = "91704"
        CustomerIdIsInvalid = "91705"
        CvvIsRequired = "81706"
        CvvIsInvalid = "81707"
        ExpirationDateConflict = "91708"
        ExpirationDateIsRequired = "81709"
        ExpirationDateIsInvalid = "81710"
        ExpirationDateYearIsInvalid = "81711"
        ExpirationMonthIsInvalid = "81712"
        ExpirationYearIsInvalid = "81713"
        NumberIsRequired = "81714"
        NumberIsInvalid = "81715"
        NumberHasInvalidLength = "81716"
        NumberMustBeTestNumber = "81717"
        TokenInvalid = "91718"
        TokenIsInUse = "91719"
        TokenIsTooLong = "91720"
        TokenIsNotAllowed = "91721"
        TokenIsRequired = "91722"

    class Customer(object):
        CompanyisTooLong = "81601"
        CustomFieldIsInvalid = "91602"
        CustomFieldIsTooLong = "81603"
        EmailIsInvalid = "81604"
        EmailIsTooLong = "81605"
        EmailIsRequired = "81606"
        FaxIsTooLong = "81607"
        FirstNameIsTooLong = "81608"
        IdIsInUse = "91609"
        IdIsInvaild = "91610"
        IdIsNotAllowed = "91611"
        IdIsTooLong = "91612"
        LastNameIsTooLong = "81613"
        PhoneIsTooLong = "81614"
        WebsiteIsTooLong = "81615"
        WebsiteIsInvalid = "81616"

    class Subscription(object):
        CannotEditCanceledSubscription = "81901"
        IdIsInUse = "81902"
        MerchantAccountIdIsInvalid = "91901"
        PriceCannotBeBlank = "81903"
        PriceFormatIsInvalid = "81904"
        StatusIsCanceled = "81905"
        TokenFormatIsInvalid = "81906"
        TrialDurationFormatIsInvalid = "81907"
        TrialDurationIsRequired = "81908"
        TrialDurationUnitIsInvalid = "81909"

    class Transaction(object):
        AmountCannotBeNegative = "81501"
        AmountIsRequired = "81502"
        AmountIsInvalid = "81503"
        AmountIsTooLarge = "81528"
        CannotBeVoided = "91504"
        CannotRefundCredit = "91505"
        CannotRefundUnlessSettled = "91506"
        CannotSubmitForSettlement = "91507"
        CreditCardIsRequired = "91508"
        CustomerDefaultPaymentMethodCardTypeIsNotAccepted = "81509"
        CustomFieldIsInvalid = "91526"
        CustomerIdIsInvalid = "91510"
        CustomerDoesNotHaveCreditCard = "91511"
        HasAlreadyBeenRefunded = "91512"
        MerchantAccountNameIsInvalid = "91513"
        MerchantAccountIsSusped = "91514"
        OrderIdIsTooLong = "91501"
        PaymentMethodConflict = "91515"
        PaymentMethodDoesNotBelongToCustomer = "91516"
        PaymentMethodTokenCardTypeIsNotAccepted = "91517"
        PaymentMethodTokenIsInvalid = "91518"
        RefundAmountIsTooLarge = "91521"
        SettlementAmountIsTooLarge = "91522"
        TypeIsInvalid = "91523"
        TypeIsRequired = "91524"

        class Options(object):
            VaultIsDisabled = "91525"

