from fastapi import status


class CustomException(Exception):
    error_type: str = ""
    msg: str = ""
    status_code: int = status.HTTP_400_BAD_REQUEST


class InternalException(CustomException):
    error_type: str = "internal"
    msg: str = "Internal exception"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
