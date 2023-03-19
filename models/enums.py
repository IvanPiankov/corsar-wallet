from enum import Enum


class AccountTypes(str, Enum):
    CASH = "cash"
    CARD = "card"
    SAVINGS_ACCOUNT = "savings_account"
    DEPOSIT_ACCOUNT = "deposit_account"


class Currency(str, Enum):
    USD = "USD"
    RUB = "RUB"
    EUR = "EUR"
