from decimal import Decimal
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

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts Router"])


def new_account_service() -> AccountsService:
    return inject.instance(AccountsService)


NewAccountsService = Annotated[AccountsService, Depends(new_account_service)]
CurrentUser = Annotated[UserInternal, Depends(get_current_user)]


@accounts_router.get(
    "",
    summary="Get user accounts",
    response_model=list[AccountOut],
    description="Need header with token: ```Authorization: Bearer {token}```",
)
async def get_user_accounts(current_user: CurrentUser, service: NewAccountsService):
    user_accounts = await service.get_user_accounts(current_user.user_id)
    print(jsonable_encoder(user_accounts))
    return jsonable_encoder(user_accounts)


@accounts_router.post(
    "",
    summary="Create user account",
    response_model=AccountOut,
    description="Need header with token: ```Authorization: Bearer {token}```",
)
async def create_user_wallet(account_in: AccountIn, current_user: CurrentUser, service: NewAccountsService):
    user_account = await service.create_account(current_user.user_id, account_in)
    return jsonable_encoder(user_account)


@accounts_router.get(
    "/{account_id}",
    summary="Get user account",
    response_model=AccountOut,
    description="Need header with token: ```Authorization: Bearer {token}```",
)
async def get_user_account(account_id: UUID, current_user: CurrentUser, service: NewAccountsService):
    user_account = await service.get_account_by_id(current_user.user_id, account_id)
    return jsonable_encoder(user_account)


@accounts_router.put(
    "/{account_id}",
    summary="Update user account",
    response_model=AccountOut,
    description="Need header with token: ```Authorization: Bearer {token}```",
)
async def update_user_currency(
    account_id: UUID, account_in: AccountIn, current_user: CurrentUser, service: NewAccountsService
):
    update_user_account = await service.update_user_account(current_user.user_id, account_id, account_in)
    return jsonable_encoder(update_user_account)


@accounts_router.delete(
    "/{account_id}",
    summary="Delete current account",
    response_model=None,
    description="Need header with token: ```Authorization: Bearer {token}```",
)
async def delete_user(account_id: UUID, current_user: CurrentUser, service: NewAccountsService):
    await service.delete_user_account(account_id)
    return ORJSONResponse({"status": "ok"})
