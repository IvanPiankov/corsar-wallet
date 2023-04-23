class NotUniqCatrgoryName(Exception):
    error_type: str = "NotUniqCatrgoryName"
    msg: str = "Not unique category name"


class CategoryNotFound(Exception):
    error_type: str = "AccountNotFound"
    msg: str = "Account not found"
