from utils.custom_exception import CustomException
from fastapi import status


class UserNotFound(CustomException):
    error_type: str = "UserNotFound"
    status_code: int = status.HTTP_400_BAD_REQUEST


class NotUniqLogin(CustomException):
    error_type: str = "NotUniqLogin"
    status_code: int = status.HTTP_400_BAD_REQUEST
    msg: str = "User with this login exist"


class NotUniqEmail(CustomException):
    error_type: str = "NotUniqEmail"
    status_code: int = status.HTTP_400_BAD_REQUEST
    msg: str = "User with this email exist"


class InvalidPassword(CustomException):
    error_type: str = "InvalidPassword"
    status_code: int = status.HTTP_400_BAD_REQUEST
