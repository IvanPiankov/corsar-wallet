import logging
from typing import Annotated

import inject
from fastapi import APIRouter, Body, Depends
from fastapi.encoders import jsonable_encoder

from models.auth import UserInternal
from models.enums import Currency
from services.user_service import UserService, get_current_user
from utils.exception import InternalException, WalletHttpException
from utils.status_code_message_mapper import ERROR_EXAMPLE_RESPONSE

user_router = APIRouter(prefix="/user", tags=["User Router"])
CurrentUser = Annotated[UserInternal, Depends(get_current_user)]


def new_user_service() -> UserService:
    return inject.instance(UserService)


@user_router.get("", summary="Get user", response_model=UserInternal, responses={401: ERROR_EXAMPLE_RESPONSE})
async def get_user(current_user: CurrentUser):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    return jsonable_encoder(current_user)


@user_router.put(
    "",
    summary="Update user currency",
    response_model=UserInternal,
    responses={401: ERROR_EXAMPLE_RESPONSE, 500: ERROR_EXAMPLE_RESPONSE},
)
async def update_user_currency(
    current_user: CurrentUser,
    wallet_currency: Currency = Body(
        ..., embed=True, title="Currency", description="Now work only this currency: `USD`, `RUB`, `EUR`"
    ),
    service: UserService = Depends(new_user_service),
):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    try:
        update_user_data = await service.update_user_currency(current_user, wallet_currency)
        return jsonable_encoder(update_user_data)
    except InternalException as e:
        logging.warning(f"internal - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=500)


@user_router.delete(
    "",
    summary="Delete current user",
    responses={
        200: {
            "content": {"application/json": {"example": {"status": "ok"}}},
        },
        401: ERROR_EXAMPLE_RESPONSE,
        500: ERROR_EXAMPLE_RESPONSE,
    },
)
async def delete_user(current_user: CurrentUser, service: UserService = Depends(new_user_service)):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    try:
        await service.delete_user(current_user.user_id)
        return jsonable_encoder({"status": "ok"})
    except InternalException as e:
        logging.warning(f"internal - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=500)
