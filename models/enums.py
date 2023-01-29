from enum import Enum


class WalletTypes(Enum, str):
    CASH = "cash"
    CARD = "card"
    SAVINGS_ACCOUNT = "savings_account"
    DEPOSIT_ACCOUNT = "deposit_account"

