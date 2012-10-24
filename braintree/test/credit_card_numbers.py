class CreditCardNumbers(object):
    class CardTypeIndicators(object):
        Commercial = "4111111111131010"
        DurbinRegulated = "4111161010101010"
        Debit = "4117101010101010"
        Healthcare = "4111111510101010"
        Payroll  = "4111111114101010"
        Prepaid = "4111111111111210"

        No  = "4111111111310101"
        Unknown = "4111111111112101"

    class FailsSandboxVerification(object):
        AmEx       = "378734493671000"
        Discover   = "6011000990139424"
        MasterCard = "5105105105105100"
        Visa       = "4000111111111115"
