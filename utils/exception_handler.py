from urllib.request import Request

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from utils.exception import WalletHttpException


def set_custom_exception(app: FastAPI) -> None:
    @app.exception_handler(WalletHttpException)
    async def custom_exception(request: Request, exc: WalletHttpException) -> ORJSONResponse:
        return ORJSONResponse(
            {"detail": [{"loc": [], "msg": exc.msg, "type": exc.error_type}]}, status_code=exc.status_code
        )
