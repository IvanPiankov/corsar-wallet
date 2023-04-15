import logging
from typing import Annotated
from uuid import UUID

import inject
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse

from models.accounts import AccountIn, AccountOut
from models.auth import UserInternal
from services.account_service import AccountsService
from services.user_service import get_current_user
from utils.exception import InternalException, WalletHttpException
from utils.exceptions.accounts_exception import AccountNotFound, NotUniqAccountName
from utils.status_code_message_mapper import ERROR_EXAMPLE_RESPONSE

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts Router"])


def new_account_service() -> AccountsService:
    return inject.instance(AccountsService)


NewAccountsService = Annotated[AccountsService, Depends(new_account_service)]
CurrentUser = Annotated[UserInternal, Depends(get_current_user)]


@accounts_router.get(
    "", summary="Get user accounts", response_model=list[AccountOut], responses={401: ERROR_EXAMPLE_RESPONSE}
)
async def get_user_accounts(current_user: CurrentUser, service: NewAccountsService):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    user_accounts = await service.get_user_accounts(current_user.user_id)
    return jsonable_encoder(user_accounts)


@accounts_router.post(
    "",
    summary="Create user account",
    response_model=AccountOut,
    responses={401: ERROR_EXAMPLE_RESPONSE, 400: ERROR_EXAMPLE_RESPONSE},
)
async def create_user_wallet(account_in: AccountIn, current_user: CurrentUser, service: NewAccountsService):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    try:
        user_account = await service.create_account(current_user.user_id, account_in)
        return jsonable_encoder(user_account)
    except NotUniqAccountName as e:
        logging.warning(f"Not unique account name - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)


@accounts_router.get(
    "/{account_id}",
    summary="Get user account",
    response_model=AccountOut,
    responses={401: ERROR_EXAMPLE_RESPONSE, 400: ERROR_EXAMPLE_RESPONSE},
)
async def get_user_account(account_id: UUID, current_user: CurrentUser, service: NewAccountsService):
    """
    Need header with token: ```Authorization: Bearer {token}```
    """
    try:
        user_account = await service.get_account_by_id(current_user.user_id, account_id)
        return jsonable_encoder(user_account)
    except AccountNotFound as e:
        logging.warning(f"account error - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)


@accounts_router.put(
    "/{account_id}",
    summary="Update user account",
    response_model=AccountOut,
    responses={401: ERROR_EXAMPLE_RESPONSE, 400: ERROR_EXAMPLE_RESPONSE, 500: ERROR_EXAMPLE_RESPONSE},
)
async def update_user_currency(
    account_id: UUID, account_in: AccountIn, current_user: CurrentUser, service: NewAccountsService
):
    """Need header with token: ```Authorization: Bearer {token}```"""
    try:
        update_user_account = await service.update_user_account(current_user.user_id, account_id, account_in)
        return jsonable_encoder(update_user_account)
    except (AccountNotFound, NotUniqAccountName) as e:
        logging.warning(f"account error - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=400)
    except InternalException as e:
        logging.warning(f"internal error - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=500)


@accounts_router.delete(
    "/{account_id}",
    summary="Delete current account",
    response_model=None,
    responses={
        200: {
            "content": {"application/json": {"example": {"status": "ok"}}},
        },
        401: ERROR_EXAMPLE_RESPONSE,
        500: ERROR_EXAMPLE_RESPONSE,
    },
)
async def delete_user(account_id: UUID, current_user: CurrentUser, service: NewAccountsService):
    """Need header with token: ```Authorization: Bearer {token}```"""
    try:
        await service.delete_user_account(account_id)
        return ORJSONResponse({"status": "ok"})
    except InternalException as e:
        logging.warning(f"internal - {e.error_type}")
        raise WalletHttpException(msg=e.msg, error_type=e.error_type, status_code=500)
