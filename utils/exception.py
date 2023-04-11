from typing import Any, Dict, Optional

from fastapi import HTTPException


class WalletHttpException(HTTPException):
    def __init__(
        self, status_code: int, error_type: str, msg: str, detail: Any = None, headers: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(status_code, detail, headers)
        self.error_type = error_type
        self.msg = msg


class InternalException(Exception):
    error_type: str = "internal"
    msg: str = "Internal exception"
