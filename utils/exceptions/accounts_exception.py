class NotUniqAccountName(Exception):
    error_type: str = "NotUniqAccountName"
    msg: str = "Not unique account name"


class AccountNotFound(Exception):
    error_type: str = "AccountNotFound"
    msg: str = "Account not found"
