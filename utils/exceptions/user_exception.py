class UserNotFound(Exception):
    error_type: str = "UserNotFound"
    msg: str = "Not found user"


class NotUniqLogin(Exception):
    error_type: str = "NotUniqLogin"
    msg: str = "User with this login exist"


class NotUniqEmail(Exception):
    error_type: str = "NotUniqEmail"
    msg: str = "User with this email exist"


class InvalidPassword(Exception):
    error_type: str = "InvalidPassword"
    msg: str = "Not valid password/login"
