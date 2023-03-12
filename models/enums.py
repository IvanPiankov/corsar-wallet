from enum import Enum


class AccountTypes(str, Enum):
    CASH = "cash"
    CARD = "card"
    SAVINGS_ACCOUNT = "savings_account"
    DEPOSIT_ACCOUNT = "deposit_account"

